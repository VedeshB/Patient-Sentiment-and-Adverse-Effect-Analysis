from bs4 import BeautifulSoup
import requests
from GenAI import genai

def fetch_data_thread(url,a):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                result=soup.get_text()
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            #initial = "give only side effect details in bulletin points from data: " + result
            prompt = f"""
            Instructions:
                1. Extract and list only the side effects mentioned in the data provided.
                2. Ensure that the response should be categorized and contains only the names of the category name, such as "pain", "urinary problem", "digestive problem", "skin" etc.
                3. Do not include any other words, phrases, or explanations in the response.
                4. Each side effect should be unique. Do not list any repeated words or phrases.
                5. Exclude words that have the same or similar meanings (e.g., do not list both "fever" and "high temperature"—only include one).
                6. instead of index numbers of the reviews replace it with * symbol
                

            ## Data:
            {result}

            ### effects:
            """
            gen=genai(prompt)
            effect_list=[]
            list_effect=[]
            effect=''
            for i in gen:
                if i!='*':
                    effect+=i
                elif i=='*':
                    list_effect.append(effect)
                    effect_list.append(list_effect)
                    list_effect=[]
                    effect=''
            if effect:
                list_effect.append(effect)
                effect_list.append(list_effect)
            return effect_list
        except:
            drug=a
            prompt_drug=f"""Instructions:
                1. List all the known side effects associated with the given data if the data is valid drug name else it should give "no medicine found".
                2. Provide the side effects in a simple, clear format without any additional explanations or unrelated information.
                3. Ensure the list is comprehensive, including both common and rare side effects.
                4. Do not include any repeated words, similar words, or words with similar synonyms in the response. Each side effect should be unique.
                5. instead using numbers to represent index use * character


                ### Medicine:
                {drug}

                ### Side Effects:"""
            effects=genai(prompt_drug)
            effect_list=[]
            list_effect=[]
            effect=''
            for i in effects:
                if i!='*':
                    effect+=i
                elif i=='*':
                    list_effect.append(effect)
                    effect_list.append(list_effect)
                    list_effect=[]
                    effect=''
            if effect:
                list_effect.append(effect)
                effect_list.append(list_effect)
            return effect_list