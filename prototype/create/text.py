import streamlit as st
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]

class Output(BaseModel):
    result: list = Field(description="Comma separated key information")

output_parser = PydanticOutputParser(pydantic_object=Output)

# Template 
prompt_template_text = PromptTemplate.from_template(
"""
text: {text}
You are an AI that extracts word. Please print out only important words from the {text} you enter. 
Elements can include title, date and time, application period, cost, location, details, etc. 
Return the result so that the word you believe to be the title is placed at the very beginning among the words in the sentence.
For the output form, output the words separately by comma, and output only in words and comma.
""",

examples = [{
            "text": "제목은 대동제 날짜는 5월30일 시간은 18시부터 장소는 대운동장",
            "result": ["대동제", "5월30일", "18시", "대운동장"]
        },
        {
            "text": "5월 20일 오후4시에 팔정도에서 불교박람회가 개최됩니다",
            "result": ["불교박람회", "5월20일", "오후4시", "팔정도"]
        },
        {
            "text": "코딩테스트가 6월5일 신공학관6122에서",
            "result": ["코딩테스트", "6월5일", "신공학관6122"]
        }]
)

llm = OpenAI(api_key=api_key)

def text_parser(input_text):
    prompt = prompt_template_text.format(text=input_text)
    response = llm(prompt)
    result_list = [item.strip() for item in response.split(',')]
    parsed_result = Output(result=result_list)
    return parsed_result.result

# category_AI
def sub_title(input_text):
    text_category_template = PromptTemplate.from_template(
    """
    You are the AI that chooses category. 
    Please print out the word that most closely relates to the category list from below. 
    You must only print out the spelling of that word.

    category list: ["일시", "장소", "기타", "세부사항", "준비물", "비용", "유의사항", "관련 문의"]

    If there is nothing appropriate in the category list, you can create and print your own top topics.

    텍스트: {text}
    """,
    example = [{
                "text": "6월 6일",
                "result": "일시"
            },
            {
                "text": "만해광장",
                "result": "장소"
            },]
    )
    llm = OpenAI(api_key=api_key,temperature=0)
    result = llm(text_category_template.format(text=input_text))
    subtext_category = result.strip()
    return subtext_category
