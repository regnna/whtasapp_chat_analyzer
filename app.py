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


# from IPython.display import display, HTML


st.set_page_config(
    page_title="Whatsapp chat analyzer",
    layout="centered",
    # initial_sidebar_state="auto",
    # page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/",
    page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f004.svg",
    menu_items={
        'Get Help': 'https://github.com/regnna',
        'Report a bug': 'https://github.com/regnna',
        'About': 'Regnna'
    }

)


st.markdown(
    f"""
         <style>
         .stApp {{
             background-image:
              url("https://images.unsplash.com/photo-1593067243214-b2e1be0aff8b?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: violet;'> Whatsapp chat Analyzer </h1>", unsafe_allow_html=True)

hide_st_style="""
                <style>
                #MainMenu {visibility:hidden;}
                header{visibility:hidden;}
                footer{visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)
#Add background image
import base64

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )



# st.sidebar.title("Whatsapp chat Analyzer")

uploaded_file = st.file_uploader("Choose a file")
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
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    if 'group notification' in user_list:
        user_list.remove('group notification')


    # user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.selectbox("Show analysis wrt",user_list)

    if st.button("Show Analysis"):
        num_messages,num_words,num_media,num_links=helper.fetch_stats(selected_user,df)
        # st.title("Top Statistics")
        st.markdown("<h2 style='text-align: center;'> Top Stats</h2>", unsafe_allow_html=True)

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
            
        col1,col2=st.columns(2,gap="medium")

        with col1:
            st.title("Monthly Timeline")
        with col2:
            st.title("Daily Timeline")
        col1,col2=st.columns(2,gap="medium")
        
        with col1:
            timeline = helper.monthly_timeline(selected_user, df)

            
            fig, ax = plt.subplots(figsize=(18,10))
            ax.plot(timeline['time'], timeline['message'], color="green")
            # plt.xticks(rotation='vertical')
            plt.xticks(fontsize=35,rotation='vertical')
            plt.yticks(fontsize=55)
            st.pyplot(fig)
        with col2:
            

            # st.title("Daily Timeline")
            timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(18,10))
            ax.plot(timeline['date_num'], timeline['message'], color="maroon")
            plt.xticks(fontsize=35,rotation='vertical')
            plt.yticks(fontsize=55)
            st.pyplot(fig)
        
        # else:
        # daily timeline
        


        # st.title('Activity Map')
        st.markdown("<h2 style='text-align: center;'> Activity Map</h2>", unsafe_allow_html=True)

        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
        with col2:
            st.header("Most busy week")
        
        col1,col2=st.columns(2)

        with col1:
            
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # st.title("Weakly Activity map")
        st.markdown("<h2 style='text-align: center;'>Weakly Activity map</h2>", unsafe_allow_html=True)

        user_heatmap=helper.activity_hit_map(selected_user,df)
        fig,ax=plt.subplots(figsize=(5,5))
        ax=sns.heatmap(user_heatmap)
        # ax.set_xticklabels([])
        st.pyplot(fig)
        #finding the busiest
        if selected_user=='Overall':
            # st.title("Most busy users")
            st.markdown("<h2 style='text-align: center;'>Most busy users</h2>", unsafe_allow_html=True)

            p,da_df=helper.fetch_busy_user(df)
            # print("P",p)
            # print("da_df",da_df)
            # st.title(type(da_df))
            # da_df.drop("group notification",axis=0,inplace=True)
            try:

                x=p.drop('group notification')
                da_df=da_df.drop(da_df[da_df['name']=='group notification'].index)
            except:
                x=p
            # st.title(x)
            col1,col2=st.columns(2)
            with col1:

                fig,ax=plt.subplots(figsize =(60, 50))
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
                st.dataframe(da_df,width=700)

        # most common word
       
        st.markdown("<h2 style='text-align: center;'>Most common Words</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            # st.header("Most common words")
        # df['message'] = df['message'].apply(lambda x: helper.remove_emoji(x))
        # df['message'] = df['message'].apply(lambda x: re.sub(r'^[\u2600-\u27FF]', '', x))
            gf,wordds = helper.word_usage(selected_user, df)

            # seaborn.countplot(y=gf[0],x=gf[1],data=)
            fig,ax=plt.subplots(figsize =(60, 50))
            ax.bar(gf[0],gf[1])
            plt.xticks(fontsize=95,rotation='vertical')
            plt.yticks(fontsize=70)

            st.pyplot(fig)

        with col2:
            # st.header("Most common words")
            gf.columns=['Word','Frequencies']
            st.dataframe(gf, width=700)
# Use CSS to create a dataframe with a specific column width
            # styles = [
            #     dict(selector="th", props=[("width", "100px")]),
            # ]
# gf.columns = ['Word', 'Frequencies']
            # gf_styled = gf.style.set_table_styles(styles)
            # display(gf_styled)

        # pf = gf.rename({'0':'word','1':'frequencies'},axis=1,inplace=True)
            # st.dataframe(gf)
           



        #most used word chart

        #WordCloud
        st.markdown("<h2 style='text-align: center;'>WordCloud</h2>", unsafe_allow_html=True)

        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        #
        ax.imshow(df_wc)
        st.pyplot(fig)

        # emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        
        st.markdown("<h2 style='text-align: center;'>Max used Emojis</h2>", unsafe_allow_html=True)


       

     



        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df,width=700)
        with col2:
            # emoji_df=emoji_df.head(9)
            # fig,ax=plt.subplots()

            # # Plot the pie chart
            # wedges, texts, autotexts = ax.pie(emoji_df["Counts"], autopct="%.2f")

            # for i, p in enumerate(wedges):
            #     x = p.get_bbox().get_points()[:,0]
            #     y = p.get_bbox().get_points()[1,1]
            #     offset_image(emoji_df["Emojis"].iloc[i], ax, x.mean(), y.mean(), zoom=0.08)

            # for i, (url, count) in enumerate(zip(emoji_urls, counts)):
            #     x = np.cos(np.pi/2 - 2*np.pi*i/len(counts))
            #     y = np.sin(np.pi/2 - 2*np.pi*i/len(counts))
            # put_image_on_pie(ax, url, (x, y), zoom=0.05)
            # st.pyplot(fig)
            emoji_df=emoji_df.head(9)
            fig,ax=plt.subplots()

            # Plot the pie chart
            ax.pie(emoji_df["Counts"], labels=emoji_df["Emojis"],autopct="%.2f")
            st.pyplot(fig)

# , textprops={'fontproperties': emoji_font}, textprops={'fontproperties': emoji_font}
