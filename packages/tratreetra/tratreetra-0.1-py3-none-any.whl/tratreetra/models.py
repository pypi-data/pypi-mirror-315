"""
    Note that for using these model wrappers,
    certain libraries' versions are recommended:

        numpy==2.0.2
        torch==2.3.1+cpu
        simalign>=0.4
        sentencepiece>=0.2.0
        spacy_udpipe>=1.0.0
        apertium>=0.2.4
        apertium-streamparser>=5.0.2
        apertium2ud>=0.0.7
"""
import functools
import logging
from typing import List, Tuple, Set, Dict, Iterable

import apertium
import spacy_stanza
import stanza
from apertium import Analyzer
from apertium2ud.convert import a2ud
from conllu import Token, TokenList
from simalign import SentenceAligner
from spacy import Language
from spacy.tokens import Doc
from streamparser import LexicalUnit

from .base import AbstractLemmatizerUPosTagger, UPOS, AbstractDependencyParser, AbstractWordAligner


class SimAlign(AbstractWordAligner):

    def __init__(self,
                 base_model: str = "xlmr",
                 token_type: str = "bpe",
                 matching_method: str = "m"):
        super(SimAlign, self).__init__()
        self._base_model: str = base_model
        self._token_type: str = token_type
        self._matching_method: str = matching_method
        logging.debug(f"Loading the [{self._base_model}] model")
        self._aligner: SentenceAligner = SentenceAligner(model=self._base_model,
                                                         token_type=self._token_type,
                                                         matching_methods=self._matching_method)

    def align(self,
              src_sentence: List[str],
              tgt_sentence: List[str]) -> List[Tuple[int, int]]:
        alignments: Dict[str, List[Tuple[int, int]]] = (
            self._aligner.get_word_aligns(src_sentence, tgt_sentence))
        for matching_method in alignments:
            return list(alignments[matching_method])

    def __str__(self):
        return f"SimAlign({self._base_model}, {self._token_type}, {self._matching_method})"


class ApertiumAnalyzer(AbstractLemmatizerUPosTagger):
    # todo: if there are better ways to deal with such
    #       things in Apertium, please email me
    _special_characters: List[str] = list("/^$<>*{}\\@#+~")
    _replacements: List[str] = ["shashchar", "capchar", "dollarchar", "lesschar", "morechar",
                                "astchar", "curlyleftchar", "curlyrightchar", "backslashchar",
                                "atchar", "hashchar", "pluschar", "tildechar"]
    assert len(_special_characters) == len(_replacements)
    _spchar2code: Dict[str, str] = dict(zip(_special_characters, _replacements))
    _code2spchar: Dict[str, str] = {co: ch for ch, co in zip(_special_characters, _replacements)}

    def __init__(self,
                 lang: str = "kir",
                 already_installed: bool = True,
                 strategy: str = "first"):

        super(ApertiumAnalyzer, self).__init__()

        if not already_installed:
            apertium.installer.install_module(lang)

        self._lang: str = lang
        self._analyzer: Analyzer = Analyzer(lang)
        self._strategy: str = strategy

    @staticmethod
    @functools.cache
    def _s(token: str) -> str:
        """ Stripping away the garbage """
        return token.strip("*").strip("]").strip("[")

    @staticmethod
    @functools.cache
    def _lu2lemma_and_morph(lu: LexicalUnit,
                            strategy: str) -> Tuple[str, Tuple[List[str], List[str]]]:

        if strategy == "first":

            AA = ApertiumAnalyzer

            # extracting the lemma and relevant analysis results
            if len(lu.readings) > 0:
                base_form: List[str] = [AA._s(r.baseform) for r in lu.readings[0]][:1]
                base_form: List[str] = [
                    b if b not in AA._code2spchar else AA._code2spchar[b]
                    for b in base_form]
                morph: List[str] = [t for r in lu.readings[0] for t in r.tags]
                lemma: str = AA._s(("".join(base_form)).lower())
                return lemma, a2ud(morph)

            return "", ([], [])

        raise NotImplementedError(f"Strategy '{strategy}' not supported.")

    def analyze(self, tokenized_sentence: List[str]) -> Iterable[Tuple[str, Set[UPOS]]]:

        # yes, very, very inefficient
        text: str = " ".join(tokenized_sentence)

        # hacks to deal with characters important for `apertium-kir`
        for spc in ApertiumAnalyzer._spchar2code:
            text: str = text.replace(spc, f" {ApertiumAnalyzer._spchar2code[spc]} ")

        # hack to work with '-'
        for token in text.split(" "):
            if "-" in token:
                tokens = token.replace("-", " - ").replace("  ", " ").split(" ")
            else:
                tokens = [token]

            # We apply analyzer to each token without morphological
            #   disambiguation; this could be improved, of course!
            for current_token in tokens:
                if not current_token.strip():
                    continue
                lus: List[LexicalUnit] = self._analyzer.analyze(current_token)
                for lexical_unit in lus:
                    lemma, (pos, feats) = (
                        ApertiumAnalyzer._lu2lemma_and_morph(lexical_unit, self._strategy))
                    pos: List[UPOS] = [UPOS(tag) for tag in pos]
                    yield lemma, frozenset(pos)

    def __str__(self):
        return f"Apertium({self._lang}, {self._strategy})"


class SpacyStanzaParser(AbstractDependencyParser):

    def __init__(self, lang: str = "tr", use_gpu: bool = False, already_installed: bool = False):
        super(SpacyStanzaParser, self).__init__()
        self._lang: str = lang
        if not already_installed:
            logging.debug(f"Downloading Stanza model for [{self._lang}]")
            stanza.download(self._lang)
        logging.debug(f"Loading pipeline [{self._lang}]")
        self._pipeline: Language = spacy_stanza.load_pipeline(name=self._lang, use_gpu=use_gpu)

    def depparse(self, tokenized_text: List[str]) -> str:

        doc: Doc = self._pipeline((" ".join(tokenized_text)).strip())
        token_list: List[Token] = []

        for token in doc:
            idx: int = token.i
            conllu_line = {"id": idx + 1,
                           "form": token.text,
                           "lemma": token.lemma_,
                           "upos": token.pos_,
                           "xpos": "_",
                           "feats": "_",
                           "head": token.head.i + 1 if str(token.dep_).lower() != "root" else 0,
                           "deprel": token.dep_,
                           "deps": "_",
                           "misc": "_"}

            token_list.append(Token(conllu_line))

        return TokenList(tokens=token_list).serialize()
