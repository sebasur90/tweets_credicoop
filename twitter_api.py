from os import access
import tweepy
#import configparser
#from tokens import tokens
import pandas as pd
from pysentimiento.preprocessing import preprocess_tweet
from pysentimiento import create_analyzer
import sys


class Twittter_Api:
    def __init__(self) -> None:
        #self.api_key=tokens['API Key']
        #self.api_key_secret=tokens['API Key Secret']
        self.bearer_token = sys.argv[1]
        #self.access_token=tokens['Access Token']
        #self.access_token_secret=tokens['Access Token Secret']
        self.client = tweepy.Client(bearer_token=self.bearer_token)
        self.query = """credicoop -is:retweet OR bancocredicoop -is:retweet OR tarjetacabal -is:retweet OR tarjeta cabal -is:retweet OR banco credicoop -is:retweet OR 
        @credicoop -is:retweet OR @bancocredicoop -is:retweet OR @tarjetacabal -is:retweet OR @tarjeta cabal -is:retweet OR @banco credicoop -is:retweet OR
        #credicoop -is:retweet OR #bancocredicoop -is:retweet OR #tarjetacabal -is:retweet OR #tarjeta cabal -is:retweet OR #banco credicoop -is:retweet OR 
        @CarlosHeller -is:retweet"""

    def busca_tweets(self):
        response = self.client.search_recent_tweets(max_results=100, query=self.query, tweet_fields=['created_at'], expansions=[
                                                    'author_id'], user_fields=['description', 'public_metrics', 'verified', 'location'])
        users = {u['id']: u for u in response.includes['users']}
        datos = pd.DataFrame(columns=['author_id', 'name', 'username', 'created_at', 'text', 'description',
                             'verified', 'followers_count', 'following_count', 'tweet_count', 'listed_count', 'location'])
        contador = 1
        for tweet in response.data:
            if users[tweet.author_id]:
                contador += 1
                user = users[tweet.author_id]
                df_tweet = pd.DataFrame([[tweet.author_id,
                                        user.name,
                                        user.username,
                                        tweet.created_at,
                                        tweet.text,
                                        user.description,
                                        user.public_metrics['followers_count'],
                                        user.public_metrics['following_count'],
                                        user.public_metrics['tweet_count'],
                                        user.public_metrics['listed_count'],
                                        user.verified,
                                        user.location]],
                                        columns=['author_id', 'name', 'username', 'created_at', 'text', 'description', 'verified', 'followers_count', 'following_count', 'tweet_count', 'listed_count', 'location'])
                print(f"Recopilando tweet {contador} --> {tweet.text}")
                datos = pd.concat([datos, df_tweet], ignore_index=True)

        return datos

    def agrega_sentimientos(self, tweets):
        analyzer_sentiment = create_analyzer(task="sentiment", lang="es")
        analyzer_emotion = create_analyzer(task="emotion", lang="es")
        hate_speech_analyzer = create_analyzer(task="hate_speech", lang="es")
        datos_pysentimiento = pd.DataFrame(columns=['sentiment', 'negativos', 'neutros', 'positivos', 'emotion', 'joy', 'sadness', 'surprise', 'anger', 'disgust', 'fear',
                                                    'hate_speech', 'hateful', 'targeted', 'aggressive'])
        for textos in tweets.text:
            preprocessed_text = preprocess_tweet(textos)
            prediccion_sentimiento = analyzer_sentiment.predict(
                preprocessed_text)
            prediccion_emocion = analyzer_emotion.predict(preprocessed_text)
            prediccion_odio = hate_speech_analyzer.predict(preprocessed_text)

            df_txt = pd.DataFrame([[prediccion_sentimiento.output,
                                    prediccion_sentimiento.probas['NEG'],
                                    prediccion_sentimiento.probas['NEU'],
                                    prediccion_sentimiento.probas['POS'],

                                    prediccion_emocion.output,
                                    prediccion_emocion.probas['joy'],
                                    prediccion_emocion.probas['sadness'],
                                    prediccion_emocion.probas['surprise'],
                                    prediccion_emocion.probas['anger'],
                                    prediccion_emocion.probas['disgust'],
                                    prediccion_emocion.probas['fear'],

                                    prediccion_odio.output,
                                    prediccion_odio.probas['hateful'],
                                    prediccion_odio.probas['targeted'],
                                    prediccion_odio.probas['aggressive']
                                    ]],
                                  columns=['sentiment', 'negativos', 'neutros', 'positivos', 'emotion', 'joy', 'sadness', 'surprise', 'anger', 'disgust', 'fear',
                                           'hate_speech', 'hateful', 'targeted', 'aggressive'])

            datos_pysentimiento = pd.concat(
                [datos_pysentimiento, df_txt], ignore_index=True)
        return datos_pysentimiento

    def apila_tweets_con_sentimientos(self, tweets, datos_pysentimiento):
        dataframe_final = pd.concat([tweets, datos_pysentimiento], axis=1)
        try:
            tweets_historicos = pd.read_csv("tweets_historicos/tweets.csv")
            datos = pd.concat(
                [tweets_historicos, dataframe_final], ignore_index=True)
            datos = datos.drop_duplicates(subset=['text'])
            datos.to_csv(f"tweets_historicos/tweets.csv", index=False)

        except:
            dataframe_final.to_csv(
                f"tweets_historicos/tweets.csv", index=False)

    def trabaja_fechas(self, datos):
        datos['created_at'] = pd.to_datetime(datos.created_at, utc=True)
        datos['dia'] = datos['created_at'].map(lambda x: x.day)
        datos['mes'] = datos['created_at'].map(lambda x: x.month)
        datos['ano'] = datos['created_at'].map(lambda x: x.year)
        datos['hora'] = datos['created_at'].map(lambda x: x.hour)
        datos['weekofyear'] = datos['created_at'].map(lambda x: x.weekofyear)
        datos['weekday'] = datos['created_at'].map(lambda x: x.weekday())
        datos['day_of_year'] = datos['created_at'].map(lambda x: x.day_of_year)
        return datos

    def run(self):
        tweets = self.busca_tweets()
        tweets_fecha = self.trabaja_fechas(tweets)
        datos_pysentimiento = self.agrega_sentimientos(tweets_fecha)
        self.apila_tweets_con_sentimientos(tweets, datos_pysentimiento)


if __name__ == '__main__':
    tweet_api = Twittter_Api()
    tweet_api.run()
