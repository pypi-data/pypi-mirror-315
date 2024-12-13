# Attaparse : Thai Dependency Parser
`attaparse` is a Thai dependency parser trained using [stanza](https://github.com/stanfordnlp/stanza/tree/main). Attaparse uses [PhayaThaiBERT](https://huggingface.co/clicknext/phayathaibert) as a based model in training process. The model refer to **Stanza*P with no POS** model in [Thai Universal Dependency Treebank (TUD)](https://github.com/nlp-chula/TUD).

## Content
1. [Installation](#installation)
2. [Usage](#Usage)

## Installation
`attaparse` can be installed usig `pip`ː
```
pip install attaparse
```

## Usage
### Initalizing

```python
import attaparse
from attaparse import load_model, depparse

nlp = load_model()
```

```python
text = 'ฉันอยากกินข้าวที่แม่ทำ'

dep = depparse(text, nlp)
```

### Access the results

```python
print(f'\n{text}\n',*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in dep.sentences for word in sent.words], sep='\n')
```
- `.id` : the id of the word.
- `.head` : the head of the word.
- `.deprel` : the dependency relationship between the word and the head.



## Citation
If you use `attaparse` in your project or publication, please cite as follows:

*BibTex*

```
@article{Sriwirote-etal-2024-TUD,
  title={The Thai Universal Dependency Treebank},
  author={Panyut Sriwirote and Wei Qi Leong and 
  Charin Polpanumas and Santhawat Thanyawong  and 
  William Chandra Tjhi and Wirote Aroonmanakun and 
  Attapol T. Rutherford},
  journal={Transactions of the Association for Computational Linguistics},
  year={in press},
  publisher={MIT Press Direct}
}
```