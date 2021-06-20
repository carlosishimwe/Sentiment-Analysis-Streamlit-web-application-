import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import base64

#title
st.title('Tweet Sentiment Analysis')
image = Image.open('254381.jpg')
st.image(image,use_column_width=True)



st.markdown(page_bg_img, unsafe_allow_html=True)
#markdown
st.markdown('This application is all about tweet sentiment analysis of airlines. We can analyse reviews of the passengers using this streamlit app.')
#sidebar
st.sidebar.title('Sentiment analysis of airlines')
# sidebar markdown 
st.sidebar.markdown("🛫We can analyse passengers review from this application.🛫")
#loading the data (the csv file is in the same folder)
#if the file is stored the copy the path and paste in read_csv method.


data=pd.read_csv('Tweets.csv')
#checkbox to show data 
if st.checkbox("Show Data"):
    st.write(data.head(50))
#subheader
st.sidebar.subheader('Tweets Analyser')

#radio buttons
tweets=st.sidebar.radio('Sentiment Type',('positive','negative','neutral'))
st.write(data.query('airline_sentiment==@tweets')[['text']].sample(1).iat[0,0])
st.write(data.query('airline_sentiment==@tweets')[['text']].sample(1).iat[0,0])
st.write(data.query('airline_sentiment==@tweets')[['text']].sample(1).iat[0,0])
#selectbox + visualisation
# An optional string to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content.
## Multiple widgets of the same type may not share the same key.
select=st.sidebar.selectbox('Visualisation Of Tweets',['Histogram','Pie Chart'],key=1)
sentiment=data['airline_sentiment'].value_counts()
sentiment=pd.DataFrame({'Sentiment':sentiment.index,'Tweets':sentiment.values})
st.markdown("###  Sentiment count")
if select == "Histogram":
        fig = px.bar(sentiment, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
        st.plotly_chart(fig)
else:
        fig = px.pie(sentiment, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

#slider
st.sidebar.markdown('Time & Location of tweets')
hr = st.sidebar.slider("Hour of the day", 0, 23)
data['Date'] = pd.to_datetime(data['tweet_created'])
hr_data = data[data['Date'].dt.hour == hr]


#multiselect
st.sidebar.subheader("Airline tweets by sentiment")
choice = st.sidebar.multiselect("Airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key = '0')  
if len(choice)>0:
    air_data=data[data.airline.isin(choice)]
    # facet_col = 'airline_sentiment'
    fig1 = px.histogram(air_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig1)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))

st.subheader('Word cloud for %s sentiment' % (word_sentiment))
df = data[data['airline_sentiment']==word_sentiment]
words = ' '.join(df['text'])
processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
plt.imshow(wordcloud)
plt.xticks([])
plt.yticks([])
st.pyplot()

