""" An example script using the `tratreetra` package. """

from typing import List

from conllu import TokenList, Token

from tratreetra.base import (AbstractDependencyParser,
                             AbstractWordAligner,
                             AbstractLemmatizerUPosTagger)
from tratreetra.models import (ApertiumAnalyzer,
                               SimAlign,
                               SpacyStanzaParser)
from tratreetra.transfer import transfer_annotations, n2u

if __name__ == "__main__":

    output_file: str = "data/out.conllu"

    with open("data/chatgpt4o_test_sentences_turkish.txt", "r", encoding="utf-8") as rf:
        turk_sents_raw: List[str] = list(rf)

    with open("data/original_test_sentences_kyrgyz.txt", "r", encoding="utf-8") as rf:
        kyrg_sents_raw: List[str] = list(rf)

    turk_parser: AbstractDependencyParser = SpacyStanzaParser()
    kyrg2turk_aligner: AbstractWordAligner = SimAlign()
    kyrg_morph_analyzer: AbstractLemmatizerUPosTagger = ApertiumAnalyzer(already_installed=True)
    annotations: List[TokenList] = transfer_annotations(raw_lrl_sentences=kyrg_sents_raw,
                                                        raw_rrl_sentences=turk_sents_raw,
                                                        rrl_parser=turk_parser,
                                                        lrl2rrl_aligner=kyrg2turk_aligner,
                                                        lrl_morph_analyzer=kyrg_morph_analyzer)

    conllu_tokenlists: List[TokenList] = []

    for sent_id, annotations in enumerate(annotations):

        token_list: List[Token] = []

        for idx, token_data in enumerate(annotations):
            ud_data = token_data or {}
            token_list.append(Token(
                {
                    "id": idx + 1,
                    "form": n2u(ud_data.get("form", "_")),
                    "lemma": n2u(ud_data.get("lemma", "_")),
                    "upos": n2u(ud_data.get("upos", "_")),
                    "xpos": n2u(ud_data.get("xpos", "_")),
                    "feats": n2u(ud_data.get("feats", "_")),
                    "head": n2u(ud_data.get("head", "_")),
                    "deprel": n2u(ud_data.get("deprel", "_")),
                    "deps": n2u(ud_data.get("deps", "_")),
                    "misc": n2u(ud_data.get("misc", "_"))
                }
            ))

        conllu_tokenlists.append(TokenList(tokens=token_list))

    with open(output_file, "w", encoding="utf-8") as wf:
        for tok_list in conllu_tokenlists:
            wf.write(tok_list.serialize())
