import datasets
import pandas as pd

tasks_mapping = pd.read_json('https://raw.githubusercontent.com/sileod/metaeval/main/metaeval.json',orient='index')

def load_and_align(dataset_name,tasks_mapping=tasks_mapping):
  if dataset_name not in tasks_mapping.index:
    return None
  x=tasks_mapping.loc[dataset_name]
  splits_mapping={'dev_r1':'validation',
  'test':'test',
  'test_matched':"test",
  'test_r1':"test",
  'train':"train",
  'train_r1':'train',
  'validation':'validation',
  'validation_matched':'validation'}

  if dataset_name=='stance':
    stance =[ datasets.load_dataset('tweet_eval',x) for x in ['stance_abortion', 'stance_atheism', 'stance_climate', 'stance_feminist', 'stance_hillary']]
    dataset=datasets.DatasetDict({k: datasets.concatenate_datasets([x[k] for x in stance]) for k in ['train','validation','test']})
  else:
    dataset=datasets.load_dataset(*x.task_tuple)

  # align columns 

  columns = set(sum(list(dataset.column_names.values()), []))

  if 'sentence1' not in columns:
    dataset=dataset.rename_column(x.text_fields[0],'sentence1')

  if len(x.text_fields)>1 and 'sentence2' not in columns:
    dataset=dataset.rename_column(x.text_fields[1],'sentence2')

  if 'label' not in columns:
    dataset=dataset.rename_column(x.label_fields[0],'label')

  for c in set(sum(list(dataset.column_names.values()), [])):
    if c not in ['sentence1','sentence2','label']:
      dataset=dataset.remove_columns(c)

  columns = set(sum(list(dataset.column_names.values()), []))
  if 'sentence1' in columns and 'sentence2' not in columns:
    dataset=dataset.rename_column('sentence1','sentence')

  # align splits

  for k in list(dataset):
    if k not in splits_mapping.values():
      if k in splits_mapping:
        dataset[splits_mapping[k]]= dataset[k]
      del dataset[k]

  for k in list(dataset):
    if -1 in set(dataset[k]['label'][:10]):
      del dataset[k]

  if 'train' not in dataset:
    return None

  if 'validation' in dataset and 'test' not in dataset:
    validation_test = dataset['validation'].train_test_split(0.5, seed=0)
    dataset['validation'] = validation_test['train']
    dataset['test']=validation_test['test']
    
  if 'test' in dataset and 'validation' not in dataset:
    validation_test = dataset['test'].train_test_split(0.5, seed=0)
    dataset['validation'] = validation_test['train']
    dataset['test']=validation_test['test']
    
  if 'validation' not in dataset and 'test' not in dataset:
    train_val_test = dataset["train"].train_test_split(seed=0)
    val_test = train_val_test["test"].train_test_split(0.5, seed=0)
    dataset["train"] = train_val_test["train"]
    dataset["validation"] = val_test["train"]
    dataset["test"] = val_test["test"]
  return dataset
