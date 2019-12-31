import pandas as pd


crawled_user_file = pd.read_csv('./output/user_data.csv')

all_user_file = pd.read_csv('./output/cleaned_data.csv')

users_crawled_list = list(crawled_user_file['uid'])
all_user_list = list(all_user_file['user_id'])

target_user_list = []
for uid in all_user_list:
    if uid not in users_crawled_list:
        target_user_list.append(uid)

dic = {'user_id': target_user_list}

print('New Users:', len(target_user_list))
df = pd.DataFrame(dic)

df.to_csv('./data/target_user.csv')


