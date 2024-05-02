import streamlit as st
from letter import write_letter


api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Letter from Hermione", page_icon="✉️")
st.title("✉️ Letter from Hermione(with md)")

def main():
    # 사용자 입력 텍스트 영역
    letter = st.text_area("Write a letter to Hermione:", height=250)

    if st.button('Send Letter'):
        if not letter:
            st.warning('Please write something in the letter.')
        else:
            response = write_letter(letter)
            st.write("Hermione's response:")
            st.write(response)

if __name__ == "__main__":
    main()
