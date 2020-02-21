# TODO: собрать тело новости

# TODO: убрать строчки для дебага


import argparse
import requests
import sys
from bs4 import BeautifulSoup as bs
import csv


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
    """ Обрабатывает парсинг данных с сайта с новостями.
    Возвращает список всех новостей и всех статей.
    """
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

    return news, articles


def filter_date(news, articles, date, rubric, file_path):
    """ Сохраняет данные с сайта в зависимости от указания пользователем даты.

    news - список всех последних новостей
    articles - список всех последних статей
    date - дата появления новости или статьи (параметр по умолчанию - 'latest')
    rubric - вид требуемых данных: news для новости или article для статьи (параметр по умолчанию - 'both')
    file_path - путь к файлу для записи данных
    """
    news_filtered = []  # новости, отсортированные по дате
    articles_filtered = []  # статьи, отсортированные по дате
    if date is not 'latest':  # если пользователем указана дата для сортировки
        for piece in news:
            if piece['date'] == date:
                news_filtered.append(piece)
        for article in articles:
            if article['date'] == date:
                articles_filtered.append(article)

    if rubric == 'news' and date is not 'latest':
        # Сохранить в файл отсортированную по дате информацию о новостях.
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=news_filtered[0])
            writer.writerows(news_filtered)
        print('Запись заголовков новостей заданной даты была успешно произведена.')
        return news_filtered

    elif rubric == 'news' and date is 'latest':
        # Сохранить в файл не отсортированную по дате информацию о новостях (все последние новости).
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=news[0])
            writer.writerows(news)
        print('Запись заголовков последних новостей была успешно произведена.')
        return news

    elif rubric == 'article' and date is not 'latest':
        # Сохранить в файл отсортированную по дате информацию о статьях.
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=articles_filtered[0])
            writer.writerows(articles_filtered)
        print('Запись заголовков статей заданной даты была успешно произведена.')
        return articles_filtered

    elif rubric == 'article' and date is 'latest':
        # Сохранить в файл не отсортированную по дате информацию о статьях (все последние статьи).
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=articles[0])
            writer.writerows(articles)
        print('Запись заголовков последних статей была успешно произведена.')
        return articles

    else:
        sys.exit("Ошибка в указании рубрики (требуется либо news, либо article).")


def parse_news_text(elements):
    """ Записывает тела всех последних новостей в текстовый файл.

    elements - список новостей или статей
    """
    newstexts = []  # все тела элементов
    for element in elements:
        temp_url = element['link']
        session = requests.Session()
        response = session.get(temp_url)
        if response.status_code == 200:
            # Запрос выполнен успешно.
            soup = bs(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                newstexts.append(paragraph.text)
        else:
            sys.exit("Ошибка открытия страницы с новостью.")

    # Запись тел всех элементов в файл newstexts.txt
    with open('newstexts.txt', 'w', encoding='utf-8') as file:
        for line in newstexts:
            file.write(line + '\n')

    print('Запись тел всех новостей успешно произведена.')


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
    # news = []
    # articles = []
    # news, articles = parse_news()
    pass
