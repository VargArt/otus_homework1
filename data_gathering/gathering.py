"""
ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью ниже)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать time.sleep(seconds),
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

Зачем нужны __init__.py файлы
https://stackoverflow.com/questions/448271/what-is-init-py-for

Про документирование в Python проекте
https://www.python.org/dev/peps/pep-0257/

Про оформление Python кода
https://www.python.org/dev/peps/pep-0008/


Примеры сбора данных:
https://habrahabr.ru/post/280238/

Для запуска тестов в корне проекта:
python3 -m unittest discover

Для запуска проекта из корня проекта:
python3 -m gathering gather
или
python3 -m gathering transform
или
python3 -m gathering stats


Для проверки стиля кода всех файлов проекта из корня проекта
pep8 .

"""

import logging

import sys
import vk_api
import csv

import language_statistic as ls
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""
Собираем данные со стены сообщества вк, по вашему выбору, с дальнейшей записью в tsv файл
В дальнейшей работе будут использованы данные со стены "типичного программиста"
"""
def gather_process():
    logger.info("gather")

    login = input('login: ')
    password = input('password: ')

    vk_session = vk_api.VkApi(login, password)

    try:
        logger.info("trying authorize in vk")
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    tools = vk_api.VkTools(vk_session)

    domain_name = input('enter vk short name')
    logger.info("getting posts")
    wall = tools.get_all('wall.get', 10, {'domain': domain_name})

    convert_data_to_table_format(wall)

"""
Преобразуем данные в tsv формат и записываем их в файл
"""
def convert_data_to_table_format(data):
    logger.info("transform")

    file_name = input('enter file name without extension') + '.tsv'
    with open(file_name, 'w') as csv_file:
        interesting_fields = ['id', 'from_id', 'owner_id', 'date', 'marked_as_ads', 'post_type', 'text', 'likes',
                              'reposts', 'views']

        tsv_writer = csv.DictWriter(csv_file, delimiter='\t', fieldnames = interesting_fields, extrasaction='ignore')
        tsv_writer.writeheader()
        for wall_item in data['items']:
            formated_dict = {}
            for k, v in wall_item.items():
                if k == 'likes' or k == 'reposts' or k == 'views':
                    formated_dict[k] = v['count']
                elif k == 'text':
                    formated_dict[k] = v.replace("\t", " ")
                else:
                    formated_dict[k] = v
            tsv_writer.writerow(formated_dict)


"""
выводим статистику
"""
def stats_of_data():
    logger.info("stats")
    posts = pd.read_csv('tproger_posts.tsv', sep='\t')

    print('Среднее количество лайков:', posts['likes'].mean())
    print('Среднее количество репостов:', posts['reposts'].mean())
    print('Среднее количество просмотров:', posts['views'].mean())

    ads = posts[posts['marked_as_ads'] > 0]
    print('Количество рекламных записей:', ads.shape[0], 'из:', posts.shape[0], '(', (1067/21461), '%', ')')

    'статистика по языкам программирования'

    ls.language_statistic(posts)


if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        print('oops!')

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
