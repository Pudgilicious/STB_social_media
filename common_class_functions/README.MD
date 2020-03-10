## This folder is to house common utility functions and classes in R or Python

### get_dist_sim.py
Import, and run the following:
```
get_final_dfs(path_to_text, path_to_excel, train_size=None, annotated_size=None, categories=None, word_count_limit=5)
```
- `path_to_text` is path to GloVe output file vectors.txt.
- `path_to_excel` is path to annotated excel file.
- `train_size` is size of training set (first x rows of excel) Defaults to 400.
- `annotated_size` is size of annotated set (first y rows of excel), defaults to 500. Test set is therefore `annotated_size - train_size` (or y - x).
- `categories` can be specified. Defaults to all unique categories identified from excel.
- keywords with count less than `word_count_limit` will automatically be ignored. Defaults to 5.

Returns a tuple of 4 dataframes, each with the following structure:
| TEXT | 1 | 2 | ... | CLOSEST | PREDICTION |
|---------|----------|----------|----------|---------|---------------------------------|
| husband | 4.014806 | 4.218744 | ... | 6 | Family/Children family/ Friends |
