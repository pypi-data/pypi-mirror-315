"""
    Abstract classes setting up the methods one should implement upon
    the creation of the custom syntactic transfer tool based on our code
"""
import logging
from abc import ABC, abstractmethod
from typing import List, Set, Tuple, Iterable

from .universal_tags import UPOS


class UsersProcessorException(ValueError):
    """ Custom tools break contracts """


class AbstractLemmatizerUPosTagger(ABC):
    """ Use this class to introduce your tagger """

    def _analyze_internal(self, tokenized_sentence: List[str]) -> List[Tuple[str, Set[UPOS]]]:
        """ Do not override this method """
        users_lemmas_tags = list(self.analyze(tokenized_sentence))
        if len(tokenized_sentence) != len(users_lemmas_tags):
            raise UsersProcessorException(f"Wrong number of tokens "
                                          f"received from PoS tagger: "
                                          f"expected {len(tokenized_sentence)}, "
                                          f"got {len(users_lemmas_tags)}. "
                                          f"Sentence: [{tokenized_sentence}]. "
                                          f"Analysis: [{users_lemmas_tags}].")
        return users_lemmas_tags

    @abstractmethod
    def analyze(self, tokenized_sentence: List[str]) -> Iterable[Tuple[str, Set[UPOS]]]:
        """
            Morphological analysis:
            1) must return the same number of items
            2) Provides a lemma and a set of likely UPOS tags
        :param tokenized_sentence: list of tokens for anaysis
        :return: a list of tuples, each contains a lemma and a set of likely UPOS tags
        """


class AbstractDependencyParser(ABC):

    def _depparse_internal(self, tokenized_text: List[str]) -> str:
        """ Do not override this method """
        parsed_sentence = self.depparse(tokenized_text)

        # quick check without full conllu conversion
        enumerated_lines = [l.strip() for l in parsed_sentence.split("\n")
                            if l.strip() and not l.strip().startswith("#")]
        if len(enumerated_lines) == 0:
            raise UsersProcessorException(f"Empty tree?")
        last_index = int(enumerated_lines[-1].split("\t")[0])
        if last_index < len(tokenized_text):
            logging.warning(f"Suspicious sentence length after parsing [{tokenized_text}]."
                            f"Expected [{len(tokenized_text)}], "
                            f"got [{last_index}].")
        return parsed_sentence

    @abstractmethod
    def depparse(self, tokenized_text: List[str]) -> str:
        """
            Syntax parsing, should return the UD tree
            AS A STRING IN CONLL-U FORMAT
            (this is far from being computationally efficient,
            however, allows to use any tool without forcing
            the user to convert to whatever format);
            we do realize that some parsers would rather work
            on raw sentences, feel free to detokenize the sentence
            in your implementation.
        :param tokenized_text: sequence of tokens making up the sentence of interest
        :return: connlu-formatted string
        """


class AbstractWordAligner(ABC):

    def _align_internal(self,
                        src_sentence: List[str],
                        tgt_sentence: List[str]) -> List[Tuple[int, int]]:

        alignment = self.align(src_sentence, tgt_sentence)
        src_len, tgt_len = len(src_sentence), len(tgt_sentence)

        for s, t in alignment:
            if not 0 <= s < src_len:
                raise UsersProcessorException(f"Index [{s}] occurred "
                                              f"in source sentence indices, "
                                              f"while it should be in [0, {src_len})")
            if not 0 <= t < tgt_len:
                raise UsersProcessorException(f"Index [{t}] occurred "
                                              f"in source sentence indices, "
                                              f"while it should be in [0, {tgt_len})")
        return alignment

    def align(self,
              src_sentence: List[str],
              tgt_sentence: List[str]) -> List[Tuple[int, int]]:
        """
        :param src_sentence: tokenized sentence in the source language
        :param tgt_sentence: tokenized sentence in the target language
        :return: a list of tuples (src_id, tgt_id), zero-indexed
        """
