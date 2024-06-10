from sysmov import path
path.create_path()

import streamlit as st
from create import image as img_module
from create import text as txt
from create import templates as temp
import time
import random


# 로그인 상태 확인 및 초기화
if 'login_nickname' not in st.session_state:
    st.session_state['login_nickname'] = 'Unknown'

if 'login_successful' not in st.session_state:
    st.session_state['login_successful'] = False

login_nickname = st.session_state.login_nickname
login_successful = st.session_state.login_successful

def main():
    if login_successful:
        st.title('Infographic Generator :frame_with_picture:')
        st.write('Welcome! ' + login_nickname)
        st.text("<www.pexels.com> Background Photos provided by pexels")
        st.divider()

        if 'slides' not in st.session_state:
            st.session_state['slides'] = []

        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = {}
        
        options = st.selectbox("템플릿 컨셉",  ["따뜻하게", "시원하게", "화사하게", "단조롭게", "신비롭게", "직접 입력"])
        if options=="직접 입력":
            options = st.text_input("템플릿 컨셉 직접 입력")

        st.divider()
        inputform()

        #### GENERATE ####
        for i in range(len(st.session_state.slides)):
            slide = st.session_state.slides[i]

            #템플릿 선정
            overlay_image = None
            
            if slide['text']:

                #텍스트 할당
                input_text = slide['text']
                text_list = txt.text_parser(input_text)
                text = {'title': ' ', 
                        'subtext1': ' ', 
                        'subtext2': ' ', 
                        'subtext3': ' ', 
                        'subtext4': ' ', 
                        'subtext5': ' ',
                        'subtext6': ' ',
                        'subtext7': ' ',
                        'subtext8': ' ',
                        'subtext9': ' ',
                        'subtext10': ' ',
                        }
                keys = list(text.keys())
                for k, value in enumerate(text_list):
                    if k < len(keys):
                        text[keys[k]] = str(value)
                
                # title_split = [' ', ' ', ' ']
                # title_split = text['title'].split()
                # st.write(title_split)
                
                
                #Color Pallete
                colNumber = temp.colorNumber(options)

                #Template Slide 
                global first_temp
                
                if i==0:                                        ##첫번째 슬라이드 이미지
                    if st.session_state.num_inputs==1:  ##추가 한번만 했을때
                        overlay_image = get_content_image(text, colNumber)
                    else: 
                        index = random.randint(0, 6)
                        
                        if index == 0:
                            slide1 = temp.book1(title=text['title'], colorNumber=colNumber)
                            first_temp = "book"
                        elif index == 1:
                            slide1 = temp.note1(toptitle=text['title'], colorNumber=colNumber)
                            first_temp = "note"
                        elif index == 2:
                            slide1 = temp.post_it1(title1=text['title'], colorNumber=colNumber)
                            first_temp = "postit"
                        elif index == 3:
                            slide1 = temp.cover1(downtitle=text['title'], colorNumber=colNumber)
                            first_temp = " "
                        elif index == 4:
                            slide1 = temp.cover2(maintitle=text['title'], colorNumber=colNumber)
                            first_temp = " "
                        elif index == 5:
                            slide1 = temp.cover3(maintitle=text['title'], colorNumber=colNumber)
                            first_temp = " "
                        elif index == 6:
                            slide1 = temp.cover4(maintitle=text['title'], subtitle=text['subtext1'], colorNumber=colNumber)
                            first_temp = " "
                        overlay_image = slide1
                    
                else:   ##이미지 2 이상
                    if first_temp=="book":
                        if i==1:
                            overlay_image = temp.book2(title=text['title'], content1=text['subtext1'], content2 =text['subtext2'], content3 = text['subtext3'],colorNumber=colNumber)
                        else:
                            overlay_image = temp.book3(subtitle1=txt.sub_title(text['subtext1']), content1=text['subtext1'], subtitle2= txt.sub_title(text['subtext1']), content2=text['subtext2'], colorNumber=colNumber)
                        
                    elif first_temp == "note":
                        if i==1:
                            overlay_image = temp.note2(title=text['title'], cont11=(text['subtext1']), cont12=text['subtext2'], cont13=text['subtext3'], colorNumber=colNumber)
                        else:
                            overlay_image = temp.note3(title=text['title'], cont1=(text['subtext1']), cont2=text['subtext2'], colorNumber=colNumber)
                    
                    elif first_temp == "postit":
                        if i==1:
                            overlay_image = temp.post_it2(title=text['title'], subtitle1=txt.sub_title(text['subtext1']), content1=text['subtext1'], subtitle2=txt.sub_title(text['subtext2']), content2 = text['subtext2'], subtitle3 = txt.sub_title(text['subtext3']), content3 = text['subtext3'],colorNumber=colNumber)
                        elif i==2:
                            overlay_image = temp.post_it3(title = text['title'], subtitle1 = txt.sub_title(text['subtext1']), subtitle2 = txt.sub_title(text['subtext2']), subtitle3 = txt.sub_title(text['subtext3']), ct11 = text['subtext1'], ct12 = text['subtext2'], ct13 = text['subtext3'], colorNumber=colNumber)
                        else:
                            overlay_image = temp.post_it4(title=text['title'], sub1=txt.sub_title(text['subtext1']), cont11=text['subtext1'], sub2=txt.sub_title(text['subtext2']), cont21=text['subtext2'], cont22=" ", cont23=" ", sub3=txt.sub_title(text['subtext3']), cont31=text['subtext3'], cont32=" ", cont33=" ", colorNumber=colNumber)               
                        
                    else:
                        overlay_image = get_content_image(text, colNumber)
                
        

                # 결과 및 다운로드
                if overlay_image: 
                    image_byte_array = overlay_image.save("output.jpg")
                    st.image(image_byte_array)
                    st.download_button(label=f"다운로드 {i+1}", data=image_byte_array, file_name=f"image_{i+1}.jpg")
    else:
        st.error('You have to login first!')

def inputform():
    add_input = st.button("추가")
    if 'num_inputs' not in st.session_state:
        st.session_state.num_inputs = 0

    if add_input:
        st.session_state.num_inputs += 1

    with st.form("form"):
        for i in range(st.session_state.num_inputs):
            slide_text = st.text_input(f"슬라이드 {i+1} 문장", key=f"text_{i}")

            if i < len(st.session_state.slides):
                st.session_state.slides[i] = {'text': slide_text}
            else:
                st.session_state.slides.append({'text': slide_text})

        submit = st.form_submit_button("생성")
        if submit:
            with st.spinner('Wait for it...'):
                time.sleep(5)

def get_content_image(text, colNumber):
    args = {
        "title": text['title'],
        "sub1": txt.sub_title(text['subtext1']),
        "sub2": txt.sub_title(text['subtext2']),
        "sub3": txt.sub_title(text['subtext3']),
        "ct1": text['subtext1'],
        "ct2": text['subtext2'],
        "ct3": text['subtext3'],
        "label": text['subtext4'],
        "colorNumber": colNumber
    }
    temp_set = [temp.content1, temp.content2, temp.content3, temp.content4]
    random_index = random.randint(0, 3)
    return temp_set[random_index](**args)

if __name__ == "__main__":
    main()
