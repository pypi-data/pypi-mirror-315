# Costra

This is a tool for automatic evaluation of Czech sentence embeddings using Costra 1.1 dataset.

More information can be found in the following paper:

* Petra Barančíková and Ondřej Bojar: [*Costra 1.1: An Inquiry into Geometric Properties of
    Sentence Spaces*](https://doi.org/10.1007/978-3-030-58323-1_14). In:
    TSD 2020. Lecture Notes in Computer Science, vol 12284. Springer, Cham.

The presentation of the paper with the accompanying video can be found
  [here](https://www.tsdconference.org/tsd2020/hall/paper_html/1075-omakox.php).


## Installation

  ```bash
  $ pip install costra

  ```

## Usage
1. Get sentences from Costra:

```python
from costra import costra
CostraEvaluator = costra.CostraEvaluator()
sentences = CostraEvaluator.get_sentences()
```

2) Generate embeddings (example with SentenceTransformers):

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Seznam/retromae-small-cs")
embeddings = model.encode(sentences)
```

3) Evaluating the embeddings:

```python
results = CostraEvaluator.evaluate(embeddings)
```

4) Results have the following format, with `costra` being the overall score.

```python
{
    'basic': 0.063,
    'modality': 0.079,
    'time': 0.692,
    'style': 0.634,
    'generalization': 0.695,
    'opposite_meaning': 0.751,
    'costra': 0.486
}
```

For more detail about Costra categories, refer to the original paper.

## Citation

If you use the tool, please consider citing
[the following paper](https://doi.org/10.1007/978-3-030-58323-1_14):

```bib
@inproceedings{Costra,
  author    = {Petra Baran{\v{\c}}{\'{\i}}kov{\'{a}} and Ond{\v{\r}}ej Bojar},
  editor    = {Petr Sojka and Ivan Kope{\v{\c}}ek and Karel Pala and Ales Hor{\'{a}}k},
  title     = {Costra 1.1: An Inquiry into Geometric Properties of Sentence Spaces},
  booktitle = {Text, Speech, and Dialogue - 23rd International Conference, {TSD}
               2020, Brno, Czech Republic, September 8-11, 2020, Proceedings},
  series    = {Lecture Notes in Computer Science},
  volume    = {12284},
  pages     = {135--143},
  publisher = {Springer},
  year      = {2020},
  url       = {https://doi.org/10.1007/978-3-030-58323-1\_14},
  doi       = {10.1007/978-3-030-58323-1\_14},
}
```

## License

The data is distributed under the [Creative Commons 4.0 BY](https://creativecommons.org/licenses/by/4.0/).
