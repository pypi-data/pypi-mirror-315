import os

from dotenv import load_dotenv
from tarot_reader import *

load_dotenv()

api_key = "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"

user_question = input('What do you wish to ask the magical tarot reader? - ')

tarot_reader = TarotReader(open_ai_api_key=api_key, model_name='gpt-4o-mini')
reading = tarot_reader.get_reading(user_question, 3)
print(reading.response)