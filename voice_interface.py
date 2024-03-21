
'''
Приклад системи розпізнавання голосу / природньої мови (Український текст) з конверцією повідомлення у текст:
https://reintech.io/blog/how-to-create-a-voice-recognition-system-with-python

необхідне оточення:
pip install SpeechRecognition
pip install PyAudio

Сценарій роботи:
1. Запис голосового повідомлення;
2. Перетворення запису до тексту;
3. Реалізація діалогу.

Застосування:
text mining голосових повідомлень;
елементарний голосовий bot (robot).

Package                      Version
---------------------------- -----------
PyAudio                      0.2.13
SpeechRecognition            3.10.0


'''

import speech_recognition as sr
import sounddevice

from visual import *
from prediction import *
from glossary import yahoo_watchlist_dictionary


# 1. Створення екземпляру класу Recognizer
recognizer = sr.Recognizer()

# 2. Запис голосового повідомлення
def capture_voice_input():
    with sr.Microphone(device_index=0) as source:
        print("Привіт, я голосовий фінансовий помічник\n"
              "Пропоную інформацію про наступні активи за останні 100 днів: ")
        for key in yahoo_watchlist_dictionary.keys():
            print(key)
        audio = recognizer.listen(source)
    return audio


# 3. Перетворення голосового повідомлення на текст
def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
        print("Ви сказали: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Вибачте, я Вас не розумію.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text

# 4. Обробка голосових команд
def process_voice_command(text):
    for key in yahoo_watchlist_dictionary.keys():
        if key in text.lower():
            process_key(key)
    if "хочу інвестувати" in text.lower():
        print("Рекомендую інвестувати сюди")
        # investment_recomendation()
    elif "бувай" in text.lower():
        print("До побачення! Гарного дня!")
        return True
    else:
        print("Команда не зрозуміла. Будь ласка спробуйте ще раз.")
    return False


def process_key(key):
    url = 'https://finance.yahoo.com/quote/'+yahoo_watchlist_dictionary[key]+'/history/'
    print('Пропоную подивитися на вартість даного активу за останні 100 днів \n'
          'та дізнатися скільки буде коштувати даний актив через тиждень:')
    raw_data = bs4_url_to_pandas(url, 'Open')
    prediction = regr_pred(raw_data)
    model_visualise(raw_data, prediction, text=key)
    return


# 5. Головні виклики
def main():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)


if __name__ == "__main__":
    main()
