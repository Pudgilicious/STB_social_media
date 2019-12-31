import pandas as pd
import twint

file1 = pd.read_csv('./twitter/tweets.csv')
file2 = pd.read_csv('./twitter/users_profile.csv')

#Reading in user names and the users that are already crawled
tweets_username = list(set(list(file1['user_name'])))
username_done = list(set(list(file2['username'])))

todo_username_list = []
for i in tweets_username:
    if i not in username_done:
        todo_username_list.append(i)

print('New users:', len(todo_username_list))

c = twint.Config()
c.Store_csv = True
c.Output = "./twitter/users_profile.csv"
for user in todo_username_list:
    c.Username = user
    twint.run.Lookup(c)



# c2 = twint.Config()
# c2.Output = 'users_tweets'
# c2.Store_csv = True
# c2.Location = True
# file3 = pd.read_csv('users_profile_cleaned.csv')
# list3 = list(set(list(file3['username'])))
# for user in list3:
#     c2.Username = user
#     twint.run.Search(c2)





