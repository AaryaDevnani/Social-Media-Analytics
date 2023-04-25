# -*- coding: utf-8 -*-
"""SMA Pratical(final)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DRGrT_rFQkmw6qSmfM6lvC2HmvxfxH7n
"""

import pandas as pd
import seaborn as sns

df=pd.read_csv("/content/tweets.csv")

df.head()

df['content'].head()

"""##Pre-Processing"""

df['content']=df['content'].astype(str)

#remove links
df['content']=df['content'].str.replace('https?://\S+',' ',regex=True)

#lowercase
df['content']=df['content'].str.lower()

#remove special characters
df['content']=df['content'].str.replace('[^A-Za-z\s]+','',regex=True)

#remove numbers
df['content']=df['content'].str.replace('\d','',regex=True)

df['content'].head()

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

df['tk']=df['content'].apply(word_tokenize)

df['tk'].head()

from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words=set(stopwords.words('english'))

df['tk']=df['tk'].apply(lambda x:[word for word in x if word not in stop_words])

from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

lemmatizer=WordNetLemmatizer()

df['lm']=df['tk'].apply(lambda x:[lemmatizer.lemmatize(word) for word in x])

df['lm'].head()

"""#Topic Modelling(LDA)"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

df['lm'] = df['lm'].astype(str)

vectorizer = CountVectorizer(max_df = 0.95, min_df = 2, max_features = 1000)
x = vectorizer.fit_transform(df['lm'])

lda = LatentDirichletAllocation(n_components = 5, learning_method = 'online', random_state = 42)
lda.fit(x)

feature_names = vectorizer.get_feature_names_out()
for topic_id, topic in enumerate(lda.components_):
#   print(f"Topic {topic_id + 1} :\n")
  print("Topic id:-",topic_id+1)
  print(", ".join([feature_names[i] for i in (-topic).argsort()[:5]]))

"""#Sentiment"""

from textblob import TextBlob
import matplotlib.pyplot as plt

# Define a function to get sentiment labels
def get_sentiment_label(sentiment):
    if sentiment > 0.0:
        return 'positive'
    elif sentiment < 0.0:
        return 'negative'
    else:
        return 'neutral'

# Apply the sentiment analysis and label function to the DataFrame's text column
df['polarity'] = df['content'].apply(lambda x: TextBlob(x).sentiment.polarity)
df['sentiment_label'] = df['polarity'].apply(get_sentiment_label)

# Print the resulting DataFrame with sentiment labels
df.head()

positive_count= df['sentiment_label'].value_counts()['positive']
negative_count = df['sentiment_label'].value_counts()['negative']

labels = ['Positive', 'Negative']
values = [positive_count, negative_count]
plt.bar(labels, values)

# Add labels and title to the plot
plt.xlabel('Sentiment Labels')
plt.ylabel('Count')
plt.title('Sentiment Analysis Results')

# Show the plot
plt.show()

plt.pie(values,labels=labels,data=df,autopct='%1.1f%%')
plt.show()

"""#Visualization"""

#just an example if you want to sort some values in descending order values for something
top_10 = df.sort_values('number_of_likes', ascending=False)

#bar chart
plt.figure(figsize=(25,10))
sns.barplot(x='author',y='number_of_likes',data=df)
plt.show()

#scatter plot x& y should be numeric
plt.figure(figsize=(15,10))
sns.scatterplot(x='number_of_shares',y='number_of_likes',hue="author",data=df)
plt.show()

#pie chart
count=df['author'].value_counts()

#bar chart
plt.figure(figsize=(10,6))
plt.pie(count,labels=count.index,data=df,autopct='%1.1f%%')
plt.show()

# Select relevant columns
data = df[['number_of_likes', 'number_of_shares']]

# Calculate correlation matrix
corr = data.corr()

# Create heatmap
plt.figure(figsize=(8,5))
sns.heatmap(corr,annot=True)
plt.show()

from wordcloud import WordCloud

wc = WordCloud(background_color = "white", height = 800, width = 800)
text = "".join(df['content'])
cloud = wc.generate(text)
plt.imshow(cloud)
plt.axis('off')
plt.show()

"""##Trend Analysis"""

df1=pd.read_csv("/content/tweets.csv")

# Convert the 'date' column to a datetime data type
df1['date'] = pd.to_datetime(df1['date_time'])
df1['date'].head()

# Extract the year, month, day, and hour into separate columns
df1['week'] = df1['date'].dt.week
df1['day'] = df1['date'].dt.day
df1['year'] = df1['date'].dt.year
df1['month'] = df1['date'].dt.month

group = df1.groupby('year')['number_of_likes'].sum()

print(group)

# plot the time series
plt.plot(group.index, group.values)
plt.xlabel('year')
plt.ylabel('No. of likes')

group1 = df1.groupby('month')['number_of_likes'].sum()

# plot the time series
plt.plot(group1.index, group1.values)
plt.xlabel('month')
plt.ylabel('No. of likes')

"""#location analysis"""

country=df.groupby('country')['number_of_likes'].sum()

sns.barplot(x=country.index,y=country.values)

"""#hashtag analysis"""

df2=pd.read_csv("/content/Covid-19 Twitter Dataset (Apr-Jun 2020).csv")

df2.head()

import nltk 
nltk.download('punkt')
from nltk.tokenize import word_tokenize

df2['hashtags']=df2['hashtags'].astype(str)

df2['hashtags']=df2['hashtags'].str.lower()

df2['ht'] = df2['hashtags'].apply(word_tokenize)

from sklearn.feature_extraction.text import CountVectorizer

df2['ht']=df2['ht'].astype(str)

vectorizer = CountVectorizer(max_df = 0.95, min_df = 2, max_features = 1000)
x = vectorizer.fit_transform(df2['ht'])

df3 = pd.DataFrame(x.toarray(), columns = vectorizer.get_feature_names_out())

word_counts = df3.sum()

sorted = word_counts.sort_values(ascending = False).head(5)

sorted

import matplotlib.pyplot as plt
sns.barplot(x=sorted.index,y=sorted.values)
plt.show()

"""#Network graph"""

import networkx as nx

G = nx.Graph()

df['author'].unique()

author=df['author'].unique()

G.add_nodes_from(author)

for i in range(len(author)):
    for j in range(i+1, len(author)):
        author1 = author[i].strip()
        author2 = author[j].strip()
        G.add_edge(author1, author2)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', edge_color='gray', alpha=0.7)
plt.show()