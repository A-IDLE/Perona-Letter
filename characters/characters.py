import sqlite3

DATABASE_NAME = "characters"
TABLE_NAME = "harry_potter_characters"



class HarryPotterCharacter:
    def __init__(self, character_name):
        self.character_name = character_name
        self.biography = None
        self.physical_description = None
        self.personality_and_trait = None
        self.magical_abilities_and_skills = None
        self.possessions = None
        self.relationships = None
        self.etymology = None
        self.examples_tone_of_voice = None
        self.character_id = None

    def set_biography(self, biography):
        self.biography = biography

    def set_physical_description(self, physical_description):
        self.physical_description = physical_description

    def set_personality_and_trait(self, personality_and_trait):
        self.personality_and_trait = personality_and_trait

    def set_magical_abilities_and_skills(self, magical_abilities_and_skills):
        self.magical_abilities_and_skills = magical_abilities_and_skills

    def set_possessions(self, possessions):
        self.possessions = possessions

    def set_relationships(self, relationships):
        self.relationships = relationships

    def set_etymology(self, etymology):
        self.etymology = etymology

    def set_examples_tone_of_voice(self, examples_tone_of_voice):
        self.examples_tone_of_voice = examples_tone_of_voice
        
    def display_info(self):
        print(f"Character Name: {self.character_name}")
        print("Biography:", self.biography or "Not available")
        print("Physical Description:", self.physical_description or "Not available")
        print("Personality and Trait:", self.personality_and_trait or "Not available")
        print("Magical Abilities and Skills:", self.magical_abilities_and_skills or "Not available")
        print("Possessions:", self.possessions or "Not available")
        print("Relationships:", self.relationships or "Not available")
        print("Etymology:", self.etymology or "Not available")
        print("Examples of Tone of Voice:", self.examples_tone_of_voice or "Not available")
    
    @staticmethod
    def init_db():
        conn = sqlite3.connect(f'database/{DATABASE_NAME}.db')
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
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        conn = sqlite3.connect(f'database/{DATABASE_NAME}.db')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} (character_name, biography, physical_description, personality_and_trait, 
            magical_abilities_and_skills, possessions, relationships, etymology, examples_tone_of_voice)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (self.character_name, self.biography, self.physical_description, self.personality_and_trait,
              self.magical_abilities_and_skills, self.possessions, self.relationships, self.etymology, self.examples_tone_of_voice))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_info_by_name(self):
        conn = sqlite3.connect(f'database/{DATABASE_NAME}.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {TABLE_NAME} WHERE character_name = ?', (self.character_name,))
        result = cursor.fetchone()
        conn.close()
        if result:
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
            return None

    
    
    
