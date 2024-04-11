from urlextract import URLExtract
import re
import pandas as pd
from collections import Counter
import emoji
from emoji import *
# from emoji import UNICODE_EMOJI
from wordcloud import WordCloud
extract = URLExtract()

import unicodedata

def is_emoji(word):
    for char in word:
        cat = unicodedata.category(char)
        if  cat.startswith('S') or cat.startswith('P') :
            return True
    return False


def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df['message'] = df['message'].apply(lambda x: re.sub(r'^<Media omitted>|^<.*>|^<deleted |[\u2600-\u27FF]', '', x))
    # print(df)
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    words = []
    me = 0
    num_messages = df.shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
        # if message=='<Media omitted>\n':
        #     me+=1
        words.extend(message.split())
    num_words = len(words)

    media = df[df['message'] == '<Media omitted>\n'].shape[0]
    return num_messages, num_words, media, len(links)


def fetch_busy_user(df):
    
    # Assuming 'df' is your DataFrame and 'column' is the column of interest
    df = df.drop(df[df['user'] =='group notification'].index)
    # print("df", df)
    x = df['user'].value_counts()
    top_7=x.head(7)
    # st.title(x)
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    # print(new_df,top_7)
    return top_7, new_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emo = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emo.columns = ["Emojis", "Counts"]

    # emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emo


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline


def activity_hit_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    # plt.figure(figsize=(20, 6))
    activity_heatmap=df.pivot_table(index="day_name", columns='period', values='message', aggfunc='count').fillna(0)
    activity_heatmap.index.rename('day name',inplace=True)
    new_columns = {
    '00_1': '12am-1am',
    '1_2': '1am-2am',
    '2_3': '2am-3am',
    '3_4': '3am-4am',
    '4_5': '4am-5am',
    '5_6': '5am-6am',
    '6_7': '6am-7am',
    '7_8': '7am-8am',
    '8_9': '8am-9am',
    '9_10': '9am-10am',
    '10_11': '10am-11am',
    '11_12': '11am-12pm',
    '12_13': '12pm-1pm',
    '13_14': '1pm-2pm',
    '14_15': '2pm-3pm',
    '15_16': '3pm-4pm',
    '16_17': '4pm-5pm',
    '17_18': '5pm-6pm',
    '18_19': '6pm-7pm',
    '19_20': '7pm-8pm',
    '20_21': '8pm-9pm',
    '21_22': '9pm-10pm',
    '22_23': '10pm-11pm',
    '23_00': '11pm-12am'
    }

    activity_heatmap.rename(columns=new_columns, inplace=True)

    # print(activity_heatmap)
    return activity_heatmap
    # plt.yticks(rotation='horizontal')
    # plt.show()

def daily_timeline(selecte_user,df):
    if selecte_user!='Overall':
        df=df[df['user']==selecte_user]
    daily_timeline = df.groupby("date_num").count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def word_usage(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    # temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    f = open('stopwords.txt', 'r')
    stopwords = f.read()
    pwords = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                word = word.strip()
                if word[0] != '@' and word[5:8] != '://' and word[4:7] != '://' and is_emoji(word)!=True  and word!='\s' :

                    pwords.append(word)
                    # print(word,len(word))
    gf = pd.DataFrame(Counter(pwords).most_common(20))
    gwords=Counter(pwords).most_common(20)

    # qf=pd.rename({'0':'word','1':'frequencies'},axis=1)
    return gf,gwords,
    # pd.DataFrame(temp(temp['message']=='This message deleted\n')
    # if selected_user == 'Overall':
    #
    #     num_messages=df.shape[0]
    #
    #     num_words=[]
    #     for message in df['message']:
    #         num_words.extend(message.split(" "))
    #     return num_messages,len(num_words)
    # else:
    #     indivi = df[df['user'] == selected_user]
    #     num_messages= df[df['user'] == selected_user].shape[0]
    #     num_word=[]
    #     # words=[]
    #     # for message in df['message']:
    #     #     if df['user']==selected_user:
    #     #         words.extend(message.split())
    #
    #     for message in indivi['message']:
    #         num_word.extend(message.split())
    #     return num_messages,len(num_word)
