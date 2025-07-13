import re
import sys
import string
import pandas as pd

from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

from src.logging import logging
from src.exception import MyException

class Preprocessing:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        
    def remove_html_tags(self, text):
        try:
            pattern = re.compile('<.*?>')
            return pattern.sub(r'', text)
        except Exception as e:
            raise MyException(e, sys) from e
    
    def remove_url(self, text):
        try:
            pattern = re.compile(r'https?://\S+|www\.\S+')
            return pattern.sub(r'', text)
        except Exception as e:
            raise MyException(e, sys) from e
    
    def remove_punc(self, text):
        try:
            punc = string.punctuation
            for char in punc:
                text = text.replace(char,'')
            return text
        except Exception as e:
            raise MyException(e, sys) from e
    
    def remove_emoji(self, text):
        try:
            emoji_pattern = re.compile(
                "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE
            )
            return emoji_pattern.sub(r'', text)
        except Exception as e:
            raise MyException(e, sys) from e
    
    def remove_stopwords(self, text):
        try:
            new_text = []
            for word in text.split():
                if word.lower() not in stopwords.words('english'):
                    new_text.append(word)
            return ' '.join(new_text)
        except Exception as e:
            raise MyException(e, sys) from e
    
    def get_wordnet_pos(self,treebank_tag):
        try:
            if treebank_tag.startswith('J'):
                return wordnet.ADJ
            elif treebank_tag.startswith('V'):
                return wordnet.VERB
            elif treebank_tag.startswith('N'):
                return wordnet.NOUN
            elif treebank_tag.startswith('R'):
                return wordnet.ADV
            else:
                return wordnet.NOUN 
             
        except Exception as e:
            raise MyException(e, sys) from e

    def lemmatize_sentence(self,sentence):
        try:
            tokens = word_tokenize(sentence)
            tagged_tokens = pos_tag(tokens)

            lemmatized = [
                self.lemmatizer.lemmatize(word, self.get_wordnet_pos(pos_tag))
                for word, pos_tag in tagged_tokens
            ]
            return ' '.join(lemmatized)
        except Exception as e:
            raise MyException(e, sys) from e
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            
            logging.info('Data Preprocessing Started....')
            _df = df
            _df = _df.drop_duplicates()
            _df = _df.dropna()
            _df = _df.reset_index(drop=True)
            
            logging.info('Removing HTML tags....')
            _df['Comment'] = _df['Comment'].apply(self.remove_html_tags)
            
            logging.info('Removing URL....')
            _df['Comment'] = _df['Comment'].apply(self.remove_url)
            
            logging.info('Removing Punitions....')
            _df['Comment'] = _df['Comment'].apply(self.remove_punc)
            
            logging.info('Removing Emojis....')
            _df['Comment'] = _df['Comment'].apply(self.remove_emoji)
            
            logging.info('Removing StopWords....')
            _df['Comment'] = _df['Comment'].apply(self.remove_stopwords)
            
            logging.info('Appling Lemmatizing....')
            _df['Comment'] = _df['Comment'].apply(self.lemmatize_sentence)
            
            _df['Sentiment'] = _df['Sentiment'].replace(
                {
                    "positive" : 1,
                    "negative" : -1,
                    "neutral"  : 0
                }
            )
            
            return _df
        except Exception as e:
            raise MyException(e, sys) from e