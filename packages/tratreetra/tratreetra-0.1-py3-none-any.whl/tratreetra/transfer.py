""" Syntactic transfer heuristics are implemented here """
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Set, Tuple

from conllu import TokenList
from conllu import parse
from sacrebleu.tokenizers.tokenizer_13a import Tokenizer13a
from tqdm import tqdm

from .base import AbstractWordAligner, AbstractLemmatizerUPosTagger, AbstractDependencyParser
from .universal_tags import UPOS
from .utils_algo import alignment2max_matching


@lru_cache(maxsize=1024)
def n2u(v: str) -> str:
    """ `None` to underscore """
    return "_" if v is None else v


def _analyze_lrl(lrl_tokenized_text: List[str],
                 lrl_analyzer: AbstractLemmatizerUPosTagger) -> List[Tuple[str, Set[UPOS]]]:
    """
        Provides lemmas and PoS sets for each token in a target (less-resourced) language sentence
    :param lrl_tokenized_text: tokenized sentence
    :param lrl_analyzer: morphological analyzer for a LRL
    :return: a list of pairs (lemma, frozenset(PoS))
    """
    return [(lemma, frozenset(pos))
            for (lemma, pos)
            in list(lrl_analyzer._analyze_internal(lrl_tokenized_text))]


def _transfer_annotations(lrl_sentences: List[List[str]],
                          rrl_ud_sentences: List[TokenList],
                          alignments_both: Dict[str, List[Dict[int, List[int]]]],
                          lrl_lemmatizer: AbstractLemmatizerUPosTagger) -> List[TokenList]:
    """ A place where all heuristics live """
    lrl_final_ud_annotations = []
    alignments_lrl2rrl, alignments_rrl2lrl = alignments_both["lrl2rrl"], alignments_both["rrl2lrl"]

    for lrl_tokens, rrl_ud, alignment, rev_alignment in zip(lrl_sentences,
                                                            rrl_ud_sentences,
                                                            alignments_lrl2rrl,
                                                            alignments_rrl2lrl):

        morpho_lrl: List[Tuple[str, Set[UPOS]]] = _analyze_lrl(lrl_tokens, lrl_lemmatizer)
        lemmata_lrl: List[str] = [l for l, _ in morpho_lrl]
        pos_sets_lrl: List[Set[UPOS]] = [p for _, p in morpho_lrl]

        # FINDING ROOT AND WHERE IT POINTS TO FORCE ITS PRESENCE

        rrl_root_id, rrl_root_pos = None, None
        alignment = defaultdict(list, alignment)
        rrl_head: Dict[int, List[int]] = defaultdict(list)
        rrl_ud: TokenList = rrl_ud

        for rrl_token in rrl_ud:
            rrl_head[int(rrl_token["head"]) - 1].append(rrl_token["id"] - 1)

            if rrl_token["deprel"].lower() == "root":
                rrl_root_id = rrl_token["id"] - 1
                rrl_root_pos = rrl_token["upos"]
                break

        # Root must remain in alignment at all costs
        #  if there is just one match, we remove all other alignments
        #  to ensure the successful marriage of the root
        if rrl_root_id not in rev_alignment:

            # we have problems here: root was not matched to anything
            for lrl_idx, lrl_pos in reversed(list(enumerate(pos_sets_lrl))):
                if rrl_root_pos in lrl_pos:
                    alignment[lrl_idx] = [rrl_root_id]
                    rev_alignment[rrl_root_id] = [lrl_idx]

            if rrl_root_id not in rev_alignment:
                for lrl_idx, lrl_pos in reversed(list(enumerate(pos_sets_lrl))):
                    if "VERB" in lrl_pos:
                        alignment[lrl_idx] = [rrl_root_id]
                        rev_alignment[rrl_root_id] = [lrl_idx]

            if rrl_root_id not in rev_alignment:
                for lrl_idx, lrl_pos in reversed(list(enumerate(pos_sets_lrl))):
                    if "NOUN" in lrl_pos:
                        alignment[lrl_idx] = [rrl_root_id]
                        rev_alignment[rrl_root_id] = [lrl_idx]

            # When there are no matching PoS, no NOUNS, no VERBs,
            #   we cannot guess anymore; just making the first word a root ¯\_(ツ)_/¯
            if rrl_root_id not in rev_alignment:
                alignment[0] = [rrl_root_id]
                rev_alignment[rrl_root_id] = [0]

        # preserving the single root match forcibly
        if len(rev_alignment[rrl_root_id]) == 1:
            matched = rev_alignment[rrl_root_id][0]
            alignment[matched] = [rrl_root_id]
        else:
            # selecting somehow
            _, selected_id = \
                sorted([(abs(lrlid - rrl_root_id), lrlid)
                        for lrlid in rev_alignment[rrl_root_id]])[0]
            alignment[selected_id] = [rrl_root_id]

        # FILTERING MATCHES BY POS TAGS WHERE POSSIBLE

        alignment_filtered = {}

        for lrl_id, rrl_ids in alignment.items():
            if len(pos_sets_lrl[lrl_id]) == 1 and len(rrl_ids) > 1:
                filtered_tis = []
                for ti in rrl_ids:
                    if rrl_ud[ti]["upos"] == next(iter(pos_sets_lrl[lrl_id])):
                        filtered_tis.append(ti)
                if len(filtered_tis) > 0:
                    alignment_filtered[lrl_id] = filtered_tis
                else:
                    alignment_filtered[lrl_id] = alignment[lrl_id]
            else:
                alignment_filtered[lrl_id] = alignment[lrl_id]

        alignment = alignment_filtered

        # MAX BIPARTITE GRAPH MATCHING TO MAKE ALIGNMENT ONE-TO-ONE

        max_match_lrl2rrl = alignment2max_matching(alignment,
                                                   len(lrl_tokens),
                                                   len(rrl_ud))
        max_match_rrl2lrl = {v: k for k, v, in max_match_lrl2rrl.items()}

        lrl_sentence_annotations = [{} for _ in lrl_tokens]

        # yes, zero-indexed
        for lrl_id in range(0, len(lrl_tokens)):
            if lrl_id not in max_match_lrl2rrl:
                lrl_sentence_annotations[lrl_id] = {
                    "form": lrl_tokens[lrl_id],
                    "lemma": lemmata_lrl[lrl_id],
                    "head": None,
                    "misc": "NotAligned"
                }
            else:
                rrl_id = max_match_lrl2rrl[lrl_id]
                rrl_token = rrl_ud[rrl_id]

                lrl_sentence_annotations[lrl_id] = {
                    "form": lrl_tokens[lrl_id],
                    "lemma": lemmata_lrl[lrl_id],
                    "upos": rrl_token["upos"],
                    "xpos": rrl_token.get("xpos", "_"),
                    "feats": rrl_token.get("feats", "_"),
                    # to be updated later
                    "head": None,
                    "deprel": rrl_token["deprel"],
                    "deps": rrl_token.get("deps", "_"),
                    "misc": rrl_token.get("misc", "_"),
                    # custom thing, used and removed later
                    "rrl_head": rrl_token.get("head", "_")
                }

        # Finally updating head references
        for lrl_id, annotation in enumerate(lrl_sentence_annotations):

            if "rrl_head" in annotation and annotation["rrl_head"] != "_":
                rrl_head = annotation["rrl_head"] - 1
                if annotation["deprel"].lower() == "root":
                    annotation["head"] = 0
                elif rrl_head in max_match_rrl2lrl:
                    annotation["head"] = max_match_rrl2lrl[rrl_head] + 1

            if annotation["head"] is None:
                if rrl_root_id in max_match_rrl2lrl:
                    annotation["head"] = max_match_rrl2lrl[rrl_root_id] + 1

        lrl_final_ud_annotations.append(TokenList(lrl_sentence_annotations))

    return lrl_final_ud_annotations


def _post(s: str) -> List[str]:
    """ A small post-tokenization step required for the data in concern """
    return s.replace("-", " - ").replace("  ", " ").split(" ")


def transfer_annotations(raw_lrl_sentences: List[str],
                         raw_rrl_sentences: List[str],
                         rrl_parser: AbstractDependencyParser,
                         lrl2rrl_aligner: AbstractWordAligner,
                         lrl_morph_analyzer: AbstractLemmatizerUPosTagger) -> List[TokenList]:
    tokenizer = Tokenizer13a()
    rrl_sentences = [_post(tokenizer(l.strip())) for l in raw_rrl_sentences]
    lrl_sentences = [_post(tokenizer(l.strip())) for l in raw_lrl_sentences]
    assert len(rrl_sentences) == len(lrl_sentences), "Sentences number should be equal"

    parsed_rrl_sents = [parse(rrl_parser._depparse_internal(rrl_sentence))[0]
                        for rrl_sentence in rrl_sentences]

    # ugly but convenient
    weird_format_dict = {"lrl2rrl": [], "rrl2lrl": []}

    for lrl_s, rrl_s in tqdm(zip(lrl_sentences, rrl_sentences),
                             "sentences processed",
                             total=len(raw_lrl_sentences)):
        alignments = lrl2rrl_aligner._align_internal(lrl_s, rrl_s)
        l2r, r2l = defaultdict(list), defaultdict(list)

        for src, tgt in alignments:
            l2r[src].append(tgt)
            r2l[tgt].append(src)

        weird_format_dict["lrl2rrl"].append(dict(l2r))
        weird_format_dict["rrl2lrl"].append(dict(r2l))

    # Transfer UD annotations
    lrl_ud_annotations = _transfer_annotations(lrl_sentences,
                                               parsed_rrl_sents,
                                               weird_format_dict,
                                               lrl_morph_analyzer)

    return lrl_ud_annotations


if __name__ == "__main__":
    pass
