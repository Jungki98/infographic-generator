import streamlit as st
import pymysql
import datetime
import hashing as hash
import time

db_host = st.secrets["database"]["host"]
db_port = st.secrets["database"]["port"]
db_name = st.secrets["database"]["database"]
db_user = st.secrets["database"]["user"]
db_password = st.secrets["database"]["password"]

db_config = {
    'host': db_host,      
    'user': db_user, 
    'password': db_password,  
    'database': db_name, 
    'port': db_port,             
    'charset': 'utf8mb4'      
}

st.title('Infographic Generator')
tab1, tab2 = st.tabs(['Login', 'Create Account'])

if 'login_nickname' not in st.session_state:
    st.session_state['login_nickname'] = 'Unknown'

if 'login_successful' not in st.session_state:
    st.session_state['login_successful'] = False

with tab1:
    st.text('You only can use the service after login')
    st.divider()

    login_id = st.text_input('Your ID', '', key='login_id')
    login_password = st.text_input('Your Password', '', key='login_password', type='password')

    if st.button('Login'):
        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            query = 'SELECT id, password, salt FROM user_account'
            cursor.execute(query)
            result = cursor.fetchall()

            login_successful = False

            for row in result:
                find_id = row[0]
                find_password = row[1]
                find_salt = row[2]

                if (find_id == login_id) and (hash.check_password(login_password, find_salt, find_password)):
                    login_successful = True
                    login_nickname = find_id
                    break

            if login_successful:
                st.success('Login Success! Welcome ' + login_nickname + '! Please wait a second')
                time.sleep(3)
                st.session_state['login_successful'] = True
                st.session_state['login_nickname'] = login_nickname
                st.switch_page('pages/main.py')
            else:
                st.error('Login Error! Please check your ID and password.')

        except pymysql.Error as e:
            st.error(f'An error occurred: {e}')

        finally:
            if connection:
                cursor.close()
                connection.close()

    if st.button('Community'):
        st.switch_page('pages/community.py')

with tab2:
    st.text('Create New Account for using this Service')
    st.divider()

    new_name = st.text_input('Your Name', '', key='create_name')
    new_birthday = st.date_input('Your Birthday', value=None, min_value=datetime.date(1900, 1, 1))
    new_id = st.text_input('Your ID', '', key='create_id')
    new_password = st.text_input('Your Password', '', key='create_password', type='password')
    
    if len(new_password) < 8:
        st.write('Password must consist of at least 8 English characters or numbers.')
    else:
        st.write('Right Value')
        
    salt, hashed_password = hash.hash_password(new_password)
    new_email = st.text_input('Your E-mail Address', '', key='create_email')

    container = st.container(border=True)
    container.write('우리는 비윤리적이거나 비사회적인 목적으로 본 서비스를 이용하는 것을 삼가합니다.')
    container.write('본 서비스를 비윤리적, 비사회적 목적으로 이용할 경우 책임은 이용자에게 있음을 명시합니다.') 
    container.write('이에 동의하시면 확인란을 선택해 주세요.')
    container.write('We refrain from using this service for unethical or unsocial purposes.') 
    container.write('It is stated that the user is responsible for using this service for unethical and unsocial purposes.') 
    container.write('If you agree to this, please check the box.')
    agree = container.checkbox('동의합니다(I Agree!)')

    if st.button('Create Account'):
        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            query = 'INSERT INTO user_account(name, birthday, id, password, salt, email) VALUES(%s, %s, %s, %s, %s, %s)'
            cursor.execute(query, (new_name, new_birthday, new_id, hashed_password, salt, new_email))
            connection.commit()
            st.success('Successful Account Creating!')
        except pymysql.Error as e:
            st.error(f'An error occurred: {e}')
        finally:
            if connection:
                cursor.close()
                connection.close()
