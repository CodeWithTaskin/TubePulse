import io
import os
import sys
import json
import pandas as pd
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from wordcloud import WordCloud
from from_root import from_root
from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils import pickler
from src.constants import *
from src.exception import MyException
from src.components.preprocessing.data_preprocessing import Preprocessing

class TubePulseEngine:
    def __init__(self):
        self.model = pickler(os.path.join(from_root(), "Model", "model.pkl"))
        self.preprocessing: Preprocessing = Preprocessing()
    
    def predict(self, comments: json) -> json:
        try:
            data = comments['comments']
            text = []
            timestamp = []
            for i in range(len(data)):
                text.append(data[i]['text'])
                timestamp.append(data[i]['timestamp'])

            df = pd.DataFrame(data)
            df = df.rename(columns={'text': 'Comment'})
            df = self.preprocessing.preprocess(df=df)

            tfidf: TfidfVectorizer = TfidfVectorizer(max_features=MAX_FEATURES)
            vector = tfidf.fit_transform(df['Comment'])

            prediction = self.model.predict(vector)

            result = pd.DataFrame(zip(text, prediction, timestamp), columns=['comment','sentiment','timestamp']).to_dict(orient='records')
            return result

        except Exception as e:
            raise MyException(e, sys) from e
        
    def pie_chart(self, sentiment_counts: json) -> io.BytesIO:
        try:
            count = sentiment_counts["sentiment_counts"]
            labels = ['Positive', 'Negative', 'Neutral']
            values = [count['1'], count['-1'], count['0']]
            colors = ['#2ca02c',"#ff0000",'#1f77b4' ]

            # Create figure
            fig = px.pie(
                values=values,
                names=labels,
                color_discrete_sequence=colors,

            )

            # Update layout and trace
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                plot_bgcolor='rgba(0,0,0,0)',
                title_x=0.5
            )
            fig.update_traces(textinfo='label+percent')

            # ✅ Save to a BytesIO buffer (in-memory)
            buffer = io.BytesIO()
            pio.write_image(fig, buffer, format="png", width=1000, height=800)

            # Rewind buffer so it's ready for reading or uploading
            buffer.seek(0)

            return buffer
        except Exception as e:
            raise MyException(e, sys) from e
        
    def word_cloud(self, comment: json) -> WordCloud:
        try:
            text = comment['comments']
            comment = ' '.join(text)
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment)

            # Plot and save to buffer
            buffer = io.BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.tight_layout(pad=0)

            # Save the matplotlib figure to buffer
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            return buffer
        except Exception as e:
            raise MyException(e, sys) from e
