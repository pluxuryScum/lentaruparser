# TODO: 1 аргумент программы - файл (обязательный, содержит путь до файла, в который будут сохраняться данные).

# TODO: 2 аргумент программы - рубрика (необязательный, фильтрует статьи по рубрике,
#  может быть либо news, либо articles. Если не указан, должны собираться все статьи (news + articles)).

# TODO: 3 аргумент программы - дата (необязательный, фильтрует статьи по дате).

# TODO: пример запуска программы: python lenta_ru.py --file="/home/Ivanov/crawler/data/lenta_ru.pkl" --rubric="news"
#  --date="2020.01.28"

# TODO: для каждой новости собрать ссылку

# TODO: для каждой новости собрать заголовок

# TODO: для каждой новости собрать дату

# TODO: собрать тело новости


import argparse
import requests
import sys
from bs4 import BeautifulSoup as bs


def create_parser():
    """ Обрабатывает аргументы командной строки.

    --file - файл (обязательный параметр, путь до файла, в который будут сохраняться данные)
    --rubric - рубрика (необязательный параметр, фильтрует статьи по рубрике, может быть либо news,
    либо articles. Если не указан, должны собираться все статьи)
    --date - дата (необязательный параметр, фильтрует статьи по дате)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--rubric', default='both')  # параметр по умолчанию равен 'both'
    parser.add_argument('--date', default='latest')  # параметр по умолчанию равен 'latest'

    return parser


def parse_news():
    base_url = 'https://lenta.ru'
    session = requests.Session()
    response = session.get(base_url)
    news = []  # список новостей
    articles = []  # список статей
    if response.status_code == 200:
        # Запрос выполнен успешно.
        soup = bs(response.content, 'html.parser')
        divs = soup.find_all('div', class_='titles')  # найти все теги <div> с атрибутами 'titles'
        # print(divs)
        for a in divs:  # поиск среди всех дочерних тегов <a> для каждого из тегов <div>
            # print(a)
            element = a.find('h3').find('a')
            # print(element)
            if str(element).startswith('<a href="/news'):  # если элемент - новость
                news.append({
                    'title': element.text,  # заголовок новости
                    'link': 'https://lenta.ru' + element.get('href'),  # ссылка на новость
                    'date': str(element)[15:25]  # дата публикации новости
                })

            elif str(element).startswith('<a href="/articles'):  # если элемент - статья
                articles.append({
                    'title': element.text,  # заголовок статьи
                    'link': 'https://lenta.ru' + element.get('href'),  # ссылка на статью
                    'date': str(element)[19:29]  # дата публикации статьи
                })
    else:
        sys.exit("Ошибка открытия страницы https://lenta.ru/")


if __name__ == "__main__":
    # DEBUG
    # news_parser = create_parser()
    # namespace = news_parser.parse_args(sys.argv[1:])
    #
    # if len(sys.argv) < 2:
    #     sys.exit('Ошибка. Переданных параметров слишком мало!')
    # elif len(sys.argv) > 4:
    #     sys.exit('Ошибка. Переданных параметров слишком много!')
    #
    # file_path = namespace.file
    # rubric = namespace.rubric
    # date = namespace.date
    pass
