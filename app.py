import re

import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import matplotlib.font_manager as mfm
import emoji
import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Whatsapp chat analyzer",
    layout="centered",
    initial_sidebar_state="auto",
    # page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/",
    page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f004.svg",
    menu_items={
        'Get Help': 'https://github.com/regnna',
        'Report a bug': 'https://github.com/regnna',
        'About': 'Regnna'
    }

)
st.sidebar.title("Whatsapp chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # st.text(type(bytes_data))
    str_data=bytes_data.decode("utf-8")
    # st.text(type(str_data))
    df=preprocessor.preprocess(str_data)
    # df['message'] = df['message'].apply(lambda x: re.sub(r'^<Media omitted>|^<.*>|^This message was deleted\n|[\u2600-\u27FF]', '', x))
    # df.drop(df[df['message'] ==''].index, inplace=True)
    df.dropna(subset=['message'], inplace=True)
    # st.dataframe(df)

    # fetching unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,num_words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1 , col2 , col3 , col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Medias")
            st.title(num_media)
        with col4:
            st.header("Link Counts")
            st.title(num_links)
        # timeline=['monthly timeline','daily timeline']
        # tml=st.selectbox("Select your timeline",timeline)
        #Monthly timeline
        # if tml=="monthly timeline":
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # else:
        # daily timeline
        st.title("daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(18,10))
        ax.plot(timeline['date_num'], timeline['message'], color="maroon")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title('Activity Map')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.title("Weakly Activity map")
        user_heatmap=helper.activity_hit_map(selected_user,df)
        fig,ax=plt.subplots(figsize=(24,12))
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #finding the busiest
        if selected_user=='Overall':
            st.title("Most busy users")
            p,da_df=helper.fetch_busy_user(df)
            # st.title(type(da_df))
            # da_df.drop("group notification",axis=0,inplace=True)
            try:
                x=p.drop('group notification')
                da_df=da_df.drop(da_df[da_df['name']=='group notification'].index)
            except:
                x=p
            # st.title(x)
            fig,ax=plt.subplots(figsize =(60, 50))
            col1,col2=st.columns(2)
            with col1:

                ax.bar(x.index,x.values,color='red')
                plt.xticks(fontsize=95,rotation='vertical')
                plt.yticks(fontsize=70)
                # # Remove x, y Ticks
                # ax.xaxis.set_ticks_position('none')
                # ax.yaxis.set_ticks_position('none')

                # Add padding between axes and labels
                ax.xaxis.set_tick_params(pad=5)
                ax.yaxis.set_tick_params(pad=10)
                st.pyplot(fig)
            with col2:
                st.dataframe(da_df)

        # most common word
        st.title("Most common Words")
        col1, col2 = st.columns(2)
        with col1:
            # st.header("Most common words")
        # df['message'] = df['message'].apply(lambda x: helper.remove_emoji(x))
        # df['message'] = df['message'].apply(lambda x: re.sub(r'^[\u2600-\u27FF]', '', x))
            gf,wordds = helper.word_usage(selected_user, df)
            for i in wordds:
                print(i,len(i))
            fig,ax=plt.subplots()
            ax.bar(gf[0],gf[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            # st.header("Most common words")
            gf.columns=['Word','Frequencies']
        # pf = gf.rename({'0':'word','1':'frequencies'},axis=1,inplace=True)
            st.dataframe(gf)


        #most used word chart

        #WordCloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        #
        ax.imshow(df_wc)
        st.pyplot(fig)

        # emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Max used Emojis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            emoji_df=emoji_df.head(9)
            # Set a font that supports emojis
            # emoji_font = plt.matplotlib.font_manager.FontProperties(fname='NotoColorEmoji-Regular.ttf')
            # plt.rcParams['font.family'] = 'Apple Color Emoji'
            fig,ax=plt.subplots()

            # Plot the pie chart
            ax.pie(emoji_df["Counts"], labels=emoji_df["Emojis"],autopct="%.2f")
            st.pyplot(fig)

# , textprops={'fontproperties': emoji_font}, textprops={'fontproperties': emoji_font}
