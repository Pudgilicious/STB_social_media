import pandas as pd
import csv


# Read in
file = pd.read_csv('weibo_data.csv')
file2 = pd.read_csv('user_data.csv')


# Clean, remove redundant
def remove_redundant(file, file_path, id):
    id_list = list()
    remove_list = list()

    for index, weibo in file.iterrows():
        if weibo[id] not in id_list:
            id_list.append(weibo[id])
        else:
            remove_list.append(index)
    file = file.drop(remove_list, axis=0)
    file.to_csv(file_path, encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)


remove_redundant(file, './output/cleaned_data.csv', 'weibo_url')

# Update target user
dic = {}
dic['user_id'] = list()

for index, row in file.iterrows():
    if row['verified']:
        if row['user_id'] not in dic['user_id']:
            if row['user_id'] not in file2['uid'].values:
                dic['user_id'].append(row['user_id'])
                # print(len(dic['user_id']))


# Output
df = pd.DataFrame(dic)
print('New Target user: ')
print(len(df))
df.to_csv('./data/target_verified_user.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
