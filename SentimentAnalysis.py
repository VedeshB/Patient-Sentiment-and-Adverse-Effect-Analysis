from textblob import TextBlob

def sentiment_analyze(a):
        for sen in a:
            s1=TextBlob(sen).sentiment.polarity
            s2=TextBlob(sen).sentiment.subjectivity
            return s1

def senti_process(data,senti_counts):
        a1=sentiment_analyze(data)
        if a1==0.0:
            senti_counts[1]+=1
        elif a1>=0.0:
            senti_counts[0]+=1
        elif a1<=-0.0:
            senti_counts[2]+=1
        return senti_counts