from GenAI import genai

def senti_summary(tex):
        prompt = f"""Instructions:
                            1. Read the provided data carefully.
                            2. Summarize all the reviews to create an easy-to-understand overview of the medicine.
                            3. Highlight the overall sentiment, key strengths, weaknesses, and common experiences mentioned in the reviews.
                            4. Ensure the summary is clear, informative, and helps users understand the medicine's effects and user experiences.
                            5. Structure the response so that each highlighted word (such as strengths, weaknesses, etc.) is followed by the summary in the next line.
                            6. Underline each key word (such as Overall Sentiment, Strengths, Weaknesses, and Common Experiences) to make them stand out like titles.
                            7. do not include any text like 'Here is the rewritten summary in the format you requested:' in the response

                        ### Data:
                        {tex}

                        Comprehensive Review Summary:

                        **Overall Sentiment:** 
                        [Summary of overall sentiment]

                        **Strengths:**  
                        [Summary of strengths]

                        **Weaknesses:** 
                        [Summary of weaknesses]

                        **Common Experiences:** 
                        [Summary of common experiences]

                        """
        fir=genai(prompt)
        main_list=[]
        list_review=[]
        review=''
        for i in fir:
            if i!='*':
                review+=i
            elif i=='*':
                list_review.append(review.strip("\n"))
                main_list.append(list_review)
                list_review=[]
                review=''
        if review:
            list_review.append(review)
            main_list.append(list_review)
        return main_list            