import sqlite3
from characters.characters import HarryPotterCharacter

DATABASE_NAME = "characters"
TABLE_NAME = "harry_potter_characters"

@staticmethod
def init_db():
    conn = sqlite3.connect(f'database/{DATABASE_NAME}.db')  # Connect to SQLite database named 'harry_potter.db' or create if it doesn't exist.
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            character_id INTEGER PRIMARY KEY AUTOINCREMENT,  
            character_name TEXT,  
            biography TEXT,
            physical_description TEXT,
            personality_and_trait TEXT,
            magical_abilities_and_skills TEXT,
            possessions TEXT,
            relationships TEXT,
            etymology TEXT,
            examples_tone_of_voice TEXT
        );
    ''')  # SQL command to create a new table 'characters' with 'character_id' as primary key.
    conn.commit()  # Commit changes to the database.
    conn.close()  # Close the database connection.


def get_info_by_name(character_name):

        conn = sqlite3.connect(f'database/{DATABASE_NAME}.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {TABLE_NAME} WHERE character_name = ?', (character_name,))
        result = cursor.fetchone()
        conn.close()
        
        
        if result:
            print("get info SUCCESS")
            character = HarryPotterCharacter(result[1])
            character.biography = result[2]
            character.physical_description = result[3]
            character.personality_and_trait = result[4]
            character.magical_abilities_and_skills = result[5]
            character.possessions = result[6]
            character.relationships = result[7]
            character.etymology = result[8]
            character.examples_tone_of_voice = result[9]
            character.character_id = result[0]
            return character
        else:
            print("get info FAIL")
            return None
        
        
        
@staticmethod
def init_letter_db():
    conn = sqlite3.connect(f'database/letters.db')  # Connect to SQLite database named 'harry_potter.db' or create if it doesn't exist.
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS letters (
            letter_id INTEGER PRIMARY KEY AUTOINCREMENT,  
            sender_name TEXT,  
            receiver_name TEXT,
            content TEXT,
            created_date DATE
        );
    ''')  # SQL command to create a new table 'characters' with 'character_id' as primary key.
    conn.commit()  # Commit changes to the database.
    conn.close()  # Close the database connection.