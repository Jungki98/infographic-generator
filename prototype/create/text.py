import streamlit as st
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

api_key = st.secrets["openai"]["api_key"]

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