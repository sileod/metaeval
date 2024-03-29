# MetaEval

MetaEval Collection of tasks for meta-learning and extreme multitask learning. We gather a large collection of classification tasks (single sentence or sentence pair) and align their format for convenient multi-task learning.
We derive a standard train/validation/split for all datasets (when no test set is available, we use half of the validation set), and map all label/text keys. 

A MetaEval dataset has a train/validation/test splits, a `label` key, and text keys that are either `sentence` or `[sentence1,entence2]`

`pip install metaeval`
or
`pip install git+https://github.com/sileod/metaeval.git`


## Listing available english tasks

```python
from metaeval import tasks_mapping, load_and_align
tasks_mapping.head(3)
```

returns

|             | task_tuple                         | text_fields            | label_fields   | split_keys                      |   num_labels |
|:------------|:-----------------------------------|:-----------------------|:---------------|:--------------------------------|-------------:|
| health_fact | ['health_fact', 'default']         | ['claim', 'main_text'] | ['label']      | ['test', 'train', 'validation'] |            4 |
| commonsense | ['metaeval/ethics', 'commonsense'] | ['text']               | ['label']      | ['test', 'train', 'validation'] |            2 |
| deontology  | ['metaeval/ethics', 'deontology']  | ['text']               | ['label']      | ['test', 'train', 'validation'] |            2 |


## Loading dataset with unified format
```python
dataset = load_and_align('health_fact')
```
returns a huggingface dataset with a unified format
```python
DatasetDict({
    train: Dataset({
        features: ['sentence1', 'sentence2', 'label'],
        num_rows: 9832
    })
    test: Dataset({
        features: ['sentence1', 'sentence2', 'label'],
        num_rows: 1235
    })
    validation: Dataset({
        features: ['sentence1', 'sentence2', 'label'],
        num_rows: 1225
    })
})
```

All datasets can then be used interchangeably with standard code that can handle `sentence` or `sentence1,sentence2` text keys.


## Citation
```bibtex
@inproceedings{sileo2021analysis,
      title={Analysis and Prediction of NLP Models Via Task Embeddings}, 
      author={Damien Sileo and Marie-Francine Moens},
      booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
      year={2022},
}
```
