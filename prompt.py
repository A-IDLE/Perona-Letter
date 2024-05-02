from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from model import load_make_character_model
from characters.characters import parse_character_description
from database.database import init_db, get_info_by_name
from characters.characters import HarryPotterCharacter
import textwrap

###### PROMPT LOADER
def load_prompt(file_name):
    
    root_path = "prompt/"
    full_path = root_path+file_name+".md"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        print("Error has Occured")
        pass


def get_character_info(character):
    
    # 1. prompt
    base_prompt = load_prompt("make_character") 
    
    print("prompt loaded")
    print(base_prompt)
    
    prompt = PromptTemplate.from_template(base_prompt)
    
    # 2. model
    llm = load_make_character_model()
    
    # 3. chain
    chain = (
        {"character": RunnablePassthrough()}
        |prompt
        |llm
        | StrOutputParser()
    )
    
    result = chain.invoke(character)
    
    return result

# print("시작합니다")
# character_name = input("Write the Character that you want to create : ")
# character_info = get_character_info(character_name)
# print(character_info)
# character = parse_character_description(character_info,character_name)


def load_character_prompt(character_name):
    
    character = get_info_by_name(character_name)
    
    prompt_inputs = {
        'character_name': lambda x:character.character_name,
        'biography': lambda x:character.biography,
        'physical_description': lambda x:character.personality_and_trait,
        'personality_and_traits': lambda x:character.personality_and_trait,
        'possessions': lambda x:character.possessions,
        'etymology': lambda x:character .etymology,
        'examples_tone_of_voice': lambda x: character.examples_tone_of_voice,
    }
    
    base_prompt = load_prompt("form")
    
    
load_character_prompt("Draco Malfoy")
    