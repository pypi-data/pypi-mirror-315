""" Code related to the algorithms on graphs we have employed in our study """
from typing import Dict, List

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching


def _alignment2matrix(src2tgt_dict: Dict[int, List[int]],
                      src_len: int,
                      tgt_len: int) -> csr_matrix:
    """ A helper function converting an alignment into a sparse matrix """
    pairs = [(key, val) for key in src2tgt_dict for val in src2tgt_dict[key]]
    rows, cols = zip(*pairs)
    res = coo_matrix((np.ones(len(pairs)), (rows, cols)), shape=(src_len, tgt_len))
    return res.tocsr()


def _max_bp_matching(sparsegraph_matrix: csr_matrix) -> Dict[int, int]:
    """ SciPy's Hopcroft-Karp's algorith to find a max. bipartite matching """
    matching = maximum_bipartite_matching(sparsegraph_matrix, perm_type='column')
    return {idx: int(value) for idx, value in enumerate(list(matching)) if value >= 0}


def alignment2max_matching(alignment: Dict[int, List[int]],
                           src_len: int,
                           tgt_len: int) -> Dict[int, int]:
    """
        A helper function that runs SciPy's Hopcroft-Karp algorithm implementation;
        max. bipartite matching saves us lots of trouble

    :param alignment: source IDs to target IDs (zero-indexed)
    :param src_len: length of the source sentence
    :param tgt_len: length of the target sentence
    :return: resulting one-to-one mapping as a dict {src_id: tgt_id}
    """
    return _max_bp_matching(_alignment2matrix(alignment, src_len, tgt_len))
