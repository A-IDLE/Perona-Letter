from create_character import create_character

## 페르소나를 입힐 케릭터 이름들 - 캐릭터 하나당 1분정도 소요
characters_names = [
    "Harry Potter",
    "Hermione Granger",
    "Ron Weasley",
    "Albus Dumbledore",
    "Severus Snape",
    "Sirius Black",
    "Luna Lovegood",
    "Rubeus Hagrid",
    "Voldemort",
    "Dobby"
]

for character_name in characters_names:
    create_character(character_name)
