# Simple Syntactic Transfer Based on the Treebank Translation Method

## Intended use 

Given 
* the sentence in the language of interest (LRL, e.g. Kyrgyz),
* the translation of the sentence to the more resourced language (e.g. Turkish),
* the dependency parser (UD) for the more resourced language (e.g. Stanza-UD_BOUN-BERT),
* the alignment model of your liking (source language should be the language of interest),
* the morphological analyzer including PoS tags (Universal Tagset) for the language of interest (e.g. `apertium-kir`; note that it must not modify the tokenization),

generate a dependency tree for the sentence in the target language.

Clearly, it's far from perfect, but may still be useful to speed up the manual treebank annotation. Please see the paper for more details.

## Example

We have provided some bindings to the popular libraries in [tratreetra/models.py](tratreetra/models.py); the appropriate
versions of these libraries should be installed, please consult the respective docstrings.

The example code in [example/example.py](example/example.py) reproduces one of the results from the paper:

* `Stanza-IMST-charlm`
* `SimAlign-XLMR`
* `apertium-kir` (without morphological disambiguation)
* Translation via `ChatGPT4o`

Please see more details in the [example/README](example/README.md).

## How to cite

The paper is still in print, the preprint on arXiv will be made available soon.

Meanwhile, if you use our tool, we'll be grateful if you cite it as follows:

```bibtex
@article{atkn2025syntax,
    author = {Alekseev, Anton and Tillabaeva, Alina and Kabaeva, Gulnara Dzh. and Nikolenko, Sergey I.},
    title = {{Syntactic Transfer to Kyrgyz Using the Treebank Translation Method (in print)}},
    journal = {To appear in the Journal of Mathematical Sciences},
    publisher = {Springer},
    year = {2025}
}
```

## TODO 

* Thoughtful approach to data structures
* Profile the code
* Upload to pypi
* Tests
* Redesign logging here and in apertium2ud
