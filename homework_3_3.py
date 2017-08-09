import requests
import os
import chardet


def get_current_dir():
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'for_translation')
    return current_dir


def get_files():
    files = os.listdir(get_current_dir())
    files_for_translation = []
    for file in files:
            files_for_translation.append(file)
    return files_for_translation


def translate_it(text, lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def save_translations():
    if not os.path.exists('result_of_translation'):
        os.makedirs('result_of_translation')
    current_dir = get_current_dir()
    for file in get_files():
        lang = file.lower()[:-4] + '-ru'
        with open(os.path.join(current_dir, file), 'rb') as f:
            data = f.read()
            result = chardet.detect(data)
            result_encoding = result['encoding']
            text = data.decode(result_encoding)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result_of_translation', file.replace('.txt', '_translated.txt')), 'w') as f:
                f.write(translate_it(text, lang))

save_translations()