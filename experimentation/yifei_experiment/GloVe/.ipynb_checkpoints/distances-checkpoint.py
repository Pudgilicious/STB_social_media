import numpy as np
import pandas as pd
import random

## Default arguments
path_to_text = './experimentation/yifei_experiment/GloVe/vectors.txt'
path_to_excel = './experimentation/yifei_experiment/GloVe/20200304_Aspects_Annotation.xlsx'
train_size = 400
annotated_size = 500
word_count_limit = 5

def get_final_dfs(  # Returns 4 DFs
    path_to_text,
    path_to_excel,
    train_size=None,
    annotated_size=None,
    categories=None,
    word_count_limit=5
):
    if train_size is None:
        train_size = 400
    if annotated_size is None:
        annotated_size = 500
        
    print("Reading .txt and .xlsx...")
    vectors_df, keywords_df = get_parsed_dfs(path_to_text, path_to_excel, word_count_limit)
    
    if categories is None:
        aspect_categories = get_aspect_categories(keywords_df)

    else:
        aspect_categories = categories    
    no_of_categories = len(aspect_categories)
    aspect_categories_numbered = dict(zip(range(1, no_of_categories+1), aspect_categories))
    
    matrix = get_matrix(vectors_df)
    centroids = get_centroids(keywords_df, matrix, aspect_categories, train_size)
    
    print("\nCalculating distances and similarities...")
    manhattan_distances, euclidean_distances, cos_sim, corr = get_distances(
        centroids, 
        matrix, 
        no_of_categories
    )
    manhattan_df = parse_to_df(manhattan_distances, vectors_df, no_of_categories)
    euclidean_df = parse_to_df(euclidean_distances, vectors_df, no_of_categories)
    cos_sim_df = parse_to_df(cos_sim, vectors_df, no_of_categories)
    corr_df = parse_to_df(corr, vectors_df, no_of_categories)
    
    def get_closest_index(row):
        dictionary = dict(zip(row, list(range(1, no_of_categories+1))))
        return dictionary[min(row)]

    def get_furthest_index(row):
        dictionary = dict(zip(row, list(range(1, no_of_categories+1))))
        return dictionary[max(row)]
    
    for df in [manhattan_df, euclidean_df]:
        df['CLOSEST'] = df.iloc[:, 1:no_of_categories+1].apply(
            get_closest_index, 
            axis=1
        )
        df['PREDICTION'] = [aspect_categories_numbered[x] for x in df['CLOSEST']]

    for df in [cos_sim_df, corr_df]:
        df['CLOSEST'] = df.iloc[:, 1:no_of_categories+1].apply(
            get_furthest_index, 
            axis=1
        )
        df['PREDICTION'] = [aspect_categories_numbered[x] for x in df['CLOSEST']]
    
    test_indices = get_test_indices(keywords_df, annotated_size, aspect_categories)
    
    for df in [manhattan_df, euclidean_df, cos_sim_df, corr_df]:
        get_accuracy(df, keywords_df, test_indices)
        
    return manhattan_df, euclidean_df, cos_sim_df, corr_df

def get_vectors_df(path_to_text): 
    vectors_df = pd.read_csv(path_to_text, delim_whitespace=True, header=None)
    parsed_col = []
    for keyword in list(vectors_df[0]):
        keyword = str(keyword)
        keyword = keyword.replace('_', ' ')
        parsed_col.append(keyword)
    vectors_df[0] = parsed_col
    vectors_df.columns = ['TEXT'] + list(range(1, vectors_df.shape[1]))
    return vectors_df

def get_keywords_df(path_to_excel, word_count_limit): 
    keywords_df = pd.read_excel(path_to_excel)
    keywords_df = keywords_df[keywords_df['count'] >= word_count_limit]
    parsed_col_2 = []
    for keyword in list(keywords_df['TEXT']):
        keyword = str(keyword)
        keyword = keyword.replace('â€™', "'")
        keyword = keyword.replace('ã©', 'é')
        parsed_col_2.append(keyword)
    keywords_df['TEXT'] = parsed_col_2
    keywords_df.drop_duplicates('TEXT', inplace=True) # There are duplicates after the .replace() functions
    return keywords_df

def get_parsed_dfs(path_to_text, path_to_excel, word_count_limit):
    vectors_df = get_vectors_df(path_to_text)
    keywords_df = get_keywords_df(path_to_excel, word_count_limit=word_count_limit)
    joint_df = vectors_df.merge(keywords_df)
    vectors_df = joint_df.iloc[:, :vectors_df.shape[1]]
    keywords_df = joint_df.iloc[:, vectors_df.shape[1]:]
    return vectors_df, keywords_df

def get_matrix(vectors_df):
    return vectors_df.iloc[:, 1:].values

def get_centroid(matrix):
    return np.mean(matrix, axis=0)

def get_manhattan(a, b):
    return np.abs(a - b).sum()

def get_euclidean(a, b):
    return np.linalg.norm(a-b)

def get_cos_sim(a, b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_corr(a, b):
    return np.correlate(a, b)[0]

def get_aspect_categories(keywords_df):
    aspect_categories = list(set(keywords_df.ASPECT_CATEGORY_NAME))
    aspect_categories = [x for x in aspect_categories if x is not np.nan]
    aspect_categories.sort()
    return aspect_categories

def get_centroids(keywords_df, matrix, aspect_categories, train_size):
    df_train = keywords_df.iloc[:train_size, :]
    no_of_categories = len(aspect_categories)
    centroids = np.zeros((no_of_categories, 300))
    for i in range(no_of_categories):
        indices = df_train[df_train.ASPECT_CATEGORY_NAME == aspect_categories[i]].index
        print('{}: {}'.format(aspect_categories[i], len(indices)))
        centroids[i] = get_centroid(matrix[indices])
    print('\nCentroids found.')
    return centroids

def get_distances(centroids, matrix, no_of_categories):  # Returns tuple of 4 matrices
    manhattan_distances = np.zeros((matrix.shape[0], no_of_categories))
    euclidean_distances = np.zeros((matrix.shape[0], no_of_categories))
    cos_sim = np.zeros((matrix.shape[0], no_of_categories))
    corr = np.zeros((matrix.shape[0], no_of_categories))

    for i in range(matrix.shape[0]):
        for j in range(no_of_categories):
            manhattan_distances[i, j] = get_manhattan(matrix[i], centroids[j])

    for i in range(matrix.shape[0]):
        for j in range(no_of_categories):
            euclidean_distances[i, j] = get_euclidean(matrix[i], centroids[j])

    for i in range(matrix.shape[0]):
        for j in range(no_of_categories):
            cos_sim[i, j] = get_cos_sim(matrix[i], centroids[j])

    for i in range(matrix.shape[0]):
        for j in range(no_of_categories):
            corr[i, j] = get_corr(matrix[i], centroids[j])
                
    return manhattan_distances, euclidean_distances, cos_sim, corr

def parse_to_df(matrix, vectors_df, no_of_categories):
    final_df = pd.DataFrame(data=matrix)
    final_df['KEYWORD'] = vectors_df.TEXT
    cols = ['KEYWORD'] + [i for i in range(no_of_categories)]
    colnames = ['KEYWORD'] + [i for i in range(1, no_of_categories+1)]
    final_df = final_df.loc[:, cols]
    final_df.columns = colnames
    return final_df

def get_test_indices(df, annotated_size, aspect_categories):
    temp_df = df.iloc[train_size:annotated_size, :]
    return temp_df[temp_df.ASPECT_CATEGORY_NAME.isin(aspect_categories)].index

def get_accuracy(model, keywords_df, test_indices):
    sum = (model.PREDICTION[test_indices] == keywords_df.ASPECT_CATEGORY_NAME[test_indices]).sum()
    print("Accuracy: {}".format(sum/len(test_indices)))
    
if __name__ == "__main__":
    print('Using default arguments. To ')
    get_final_dfs(
        path_to_text,
        path_to_excel,
        train_size=None,
        annotated_size=None,
        word_count_limit=5
    )