from ReviewExtraction import fetch_reddit_data, review
from TextProcessing import t_ex
from SentimentAnalysis import senti_process
from Summary import senti_summary
from GenAI import genai

def process_reviews_thread(url,a):
        senti_counts=[0,0,0]
        try:
            reddit=fetch_reddit_data(a)
            for i in reddit:
                text=t_ex(i)
                reddit_senti=senti_process(text,senti_counts)
            print(reddit_senti)
            d = review(url)
            for i in d:
                s=''
                for j in i:  
                    s+=j
                c=t_ex(s)
                drugs_senti=senti_process(c,senti_counts)
            print(drugs_senti)
            tex = ''
            for i in range(0,len(d),7):
                for j in d[i]:
                    tex += j
            summary=senti_summary(tex)
            r=[]
            r.append(drugs_senti)
            r.append(summary)
            return r

        except:
            tex=a
            summary_list=[]
            for i in range(10):
                prompt_list=[]
                prompt=f"""Instructions:
                        1. if the data is valid drug name analyze the provided data to understand the context of the medicine  else it should give "no medicine found".
                        2. Generate realistic user reviews that reflect typical experiences with the medicine.
                        3. Ensure the reviews cover various aspects, including overall sentiment, key strengths, weaknesses, and common experiences.
                        4. Write the reviews in a way that they sound authentic and represent different perspectives.
                        5. ensure that the response does not have any special characters
                        6. instead of index numbers of the reviews replace it with * symbol

                        ### Data:
                        {tex}

                        ### Generated User Reviews List:

                            reviews
                        """
                syn_review=genai(prompt)
                prompt_list.append(syn_review)
                summary_list.append(prompt_list)
            # print(summary_list)
            for i in summary_list:
                s=''
                for j in i:  
                    s+=j
                c=t_ex(s)
                except_senti=senti_process(c,senti_counts)
            print(except_senti)
            exe_tex=''
            for i in summary_list:
                for j in i:
                    exe_tex+=j
            r=[]
            r.append(except_senti)
            r.append(senti_summary(exe_tex))
            return r