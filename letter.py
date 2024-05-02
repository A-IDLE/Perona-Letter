from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from retriever import load_faiss_retriever
from model import load_model
from embeddings import embed_text
from utils import document_to_string, load_prompt

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
    embed_text(letter)
    
    related_letters = retrieve_through_letter(letter)
    related_letters_str = [document_to_string(related_letter) for related_letter in related_letters]
    
    added_prompt =(
        f"""
        
        ## Reference
        {related_letters_str}
        
        
        write ONLY IN KOREAN
        """ 
    )

    
    ## 1. Prompt
    file_name = "hermione_markdown_including_pottermore"
    
    hermione_prompt = load_prompt(file_name)
    final_prompt = hermione_prompt + added_prompt
    
    prompt = PromptTemplate.from_template(final_prompt)
    
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