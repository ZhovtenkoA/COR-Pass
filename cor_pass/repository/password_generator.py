import string
import secrets
from cor_pass.schemas import PasswordGeneratorSettings, WordPasswordGeneratorSettings


# Список слов для генерации паролей из слов / заменить на открытую базу слов
WORDS_LIST = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya"]


def generate_password(settings: PasswordGeneratorSettings) -> str:
    characters = ""
    if settings.include_uppercase:
        characters += string.ascii_uppercase
    if settings.include_lowercase:
        characters += string.ascii_lowercase
    if settings.include_digits:
        characters += string.digits
    if settings.include_special:
        characters += string.punctuation

    if not characters:
        raise ValueError("No characters available for password generation.")

    return ''.join(secrets.choice(characters) for _ in range(settings.length))



def generate_word_password(settings: WordPasswordGeneratorSettings) -> str:
    if settings.separator_hyphen:
        separator = "-"
    elif settings.separator_underscore:
        separator = "_"
    else:
        separator = ""
    return separator.join(secrets.choice(WORDS_LIST) for _ in range(settings.length))