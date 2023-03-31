import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    msgs = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': msgs, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    # df.head()
    # df.tail()
    users = []

    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
    df['user'] = users#
    df['message'] = messages
    #df['message'] = df['message'].apply(lambda x: re.sub(r'^<Media omitted>|^<.*>|^This message wad deleted|[\u2600-\u27FF]', '', x))
    df.drop(columns=['user_message'], inplace=True)
    # df.head()
    # df.tail()

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['date_num']=df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day_name']=df['date'].dt.day_name()

    df['DAY'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "_" + str('00'))
        elif hour == 0:
            period.append(str('00') + "_" + str(hour + 1))
        else:
            period.append(str(hour) + "_" + str(hour + 1))
    # period
    df['period'] = period
    return df