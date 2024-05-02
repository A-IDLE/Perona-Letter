import streamlit as st
from letter import write_letter_character, Letter
from embeddings import embed_letter
from datetime import datetime
from database.database import init_letter_db


api_key = st.secrets["OPENAI_API_KEY"]

### IMPORTANT
# main.py 를 돌리기전에 test.py에서 캐릭터를 페르소나를 입히는 것 필요

st.set_page_config(page_title="Letter from Hermione", page_icon="✉️")
st.title("✉️ Letter from Hermione(with md)")

def main():
    
    # 사용자의 이름을 임의 설정
    username = "Inji"
    
    # 편지 객체 초기화
    letter_send = Letter()
    
    # 사용자 입력 텍스트 영역
    letter_content = st.text_area("Persona Letter", height=250)
    
    character_name = st.text_input('Character that you are write to')

    if st.button('Send Letter'):
        if not letter_content:
            st.warning('Please write something in the letter.')
        else:
            
            letter_send.set_sender_name(username)
            letter_send.set_content(letter_content)
            letter_send.set_receiver_name(character_name)
            letter_send.set_created_date(datetime.now())
            
            
            init_letter_db()
            letter_send.save_to_db()
            embed_letter(letter_send)
            
            response = write_letter_character(letter_send)
            st.write(f"{character_name}'s response:")
            st.write(response)

if __name__ == "__main__":
    main()
