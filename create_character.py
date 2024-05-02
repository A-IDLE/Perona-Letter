


# CHARACTER RELATED
from characters.characters import HarryPotterCharacter
from model import load_make_character_model
from prompt import load_prompt
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def parse_character_description(description, character_name):
    sections = description.split("## ")
    character = HarryPotterCharacter(character_name)  # Assuming the character's name is known beforehand.

    for section in sections[1:]:  # skip the first empty section
        title_end = section.find('\n')
        title = section[:title_end].strip()
        content = section[title_end:].strip()

        if title == "Biography":
            character.set_biography(content)
        elif title == "Physical Description":
            character.set_physical_description(content)
        elif title == "Personality and Traits":
            character.set_personality_and_trait(content)
        elif title == "Magical Abilities and Skills":
            character.set_magical_abilities_and_skills(content)
        elif title == "Possessions":
            character.set_possessions(content)
        elif title == "Relationships":
            character.set_relationships(content)
        elif title == "Etymology":
            character.set_etymology(content)
        elif title == "Examples of Tone of Voice":
            character.set_examples_tone_of_voice(content)

    return character

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


def create_character(character_name):
    print("시작합니다")
    # character_name = input("Write the Character that you want to create : ")
    character_info = get_character_info(character_name)
    print(character_info)
    character = parse_character_description(character_info,character_name)
    character.save_to_db()
    print("Character Saved!!")