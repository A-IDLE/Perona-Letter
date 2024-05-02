from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from retriever import load_faiss_retriever
from model import load_model
from utils import document_to_string, load_prompt
from prompt import load_character_prompt
from embeddings import embed_letter
from datetime import datetime
from database.database import init_letter_db
import sqlite3

class Letter:
    def __init__(self):
        self.letter_id = None
        self.sender_name = None
        self.receiver_name = None
        self.content = None
        self.created_date = None

    def __str__(self):
        date_str = self._created_date.strftime('%Y-%m-%d %H:%M:%S') if self._created_date else "Not set"
        return (f"Letter ID: {self._letter_id}, Sender: {self._sender_name}, "
                f"Receiver: {self._receiver_name}, Content: '{self._content}', "
                f"Date: {date_str}")

    # Setter for sender_name
    def set_sender_name(self, sender_name):
        self.sender_name = sender_name

    # Setter for receiver_name
    def set_receiver_name(self, receiver_name):
        self.receiver_name = receiver_name

    # Setter for content
    def set_content(self, content):
        self.content = content

    # Setter for created_date
    def set_created_date(self, created_date):
        if not isinstance(created_date, datetime):
            raise ValueError("created_date must be a datetime object")
        self.created_date = created_date
        
    def save_to_db(self):
        conn = sqlite3.connect(f'database/letters.db')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO letters (
                sender_name ,  
                receiver_name ,
                content ,
                created_date
            )
            VALUES (?, ?, ?, ?);
        ''', (
                self.sender_name, 
                self.receiver_name, 
                self.content, 
                self.created_date
            ))
        conn.commit()
        conn.close()
        
        
        

def generate_questions(letter):
    # # 총 몇개의 질문을 만들지
    # max_questions = 3

    prompt_text = """
            You are an AI assistant tasked with generation of 3 questions to explore deeper based on the following letter
            
            ## Letter
            {letter}
            
            Please answer in format only, without any other content.
            
            """
    prompt = PromptTemplate.from_template(prompt_text)

    llm = load_model()
    
    llm_chain = (
         {"letter": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = llm_chain.with_config(configuarble={"llm":"gpt-4-turbo-preview"}).invoke(letter)
    return response


def retrieve_letter(questions):
    retriever = load_faiss_retriever()
    letters = retriever.invoke(questions)
    
    print("this is retrieved letters \n"+"****"*10)
    print(letters)

    return letters


def retrieve_through_letter(letter):
     ## 2-1. 수신 메일에 대한 질의 작성
    questions = generate_questions(letter)

    ## 2-2. 질의 내용을 RAG를 통해서 관련 메일 추출
    related_letters = retrieve_letter(questions)
    
    return related_letters

def write_letter(letter):
    # 1. Embed the received Letter
    
    related_letters = retrieve_through_letter(letter)
    related_letters_str = [document_to_string(related_letter) for related_letter in related_letters]
    
    added_prompt =(
        f"""
        
        ## Reference
        {related_letters_str}
        
        """ 
    )

    
    ## 1. Prompt
    file_name = "hermione_markdown_including_pottermore"
    
    hermione_prompt = load_prompt(file_name)
    final_prompt = hermione_prompt + added_prompt
    
    prompt = PromptTemplate.from_template(final_prompt)
    
    
    print("THIS IS FINAL PROMPT \n\n")
    print(prompt)
    
    
    ## 2. LLM
    llm = load_model()
    
    ## 3. Chain
    chain = (
        { "letter": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 4. Write Mail
    try:
        
        response = chain.invoke(letter)

        return response
    
    except Exception as e:
        ("An error occurred: " + str(e))
        pass
    
    
def write_letter_character(letter_send):
    
    letter = letter_send.content
    character_name = letter_send.receiver_name
    
    related_letters = retrieve_through_letter(letter)
    related_letters_str = [document_to_string(related_letter) for related_letter in related_letters]
    
    added_prompt =(
        f"""
        
        ## Reference
        {related_letters_str}
        
        """ 
    )

    
    ## 1. Prompt
    character_prompt = load_character_prompt(character_name)
    
    final_prompt = character_prompt + added_prompt
    
    prompt = PromptTemplate.from_template(final_prompt)
    
    
    print("THIS IS FINAL PROMPT \n\n")
    print(prompt)
    
    
    ## 2. LLM
    llm = load_model()
    
    ## 3. Chain
    chain = (
        { "letter": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 4. Write Mail
    try:
        
        response = chain.invoke(letter)

        # 응답한 메일을 초기화
        letter_reply = Letter()
        letter_reply.set_sender_name(character_name)
        letter_reply.set_receiver_name(letter_send.sender_name)
        letter_reply.set_content(response)
        letter_reply.set_created_date(datetime.now())
        
        embed_letter(letter_reply)
        
        init_letter_db()
        print("init success")
        letter_reply.save_to_db()
        print("save success")

        return response
    
    except Exception as e:
        ("An error occurred: " + str(e))
        pass
    
