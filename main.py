from graf import *
from bd_work import *
import random


def input_check(string, choice):
    while string not in choice:
        print("Неверное значение, введите еще раз:")
        string = input().lower()
    return string


def get_category(count):
    cat_think, cat_laugh = 0, 0
    for i in range(count):
        category = input_check(input().lower(), ['1', "подумать", '2', "посмеяться"])
        if category in ['1', "подумать"]:
            cat_think += 1
        else:
            cat_laugh += 1

    if cat_think > cat_laugh:
        return "think"
    elif cat_think < cat_laugh:
        return "laugh"
    else:
        return random.choice(["подумать", "посмеяться"])


def get_time(count):
    result = 0
    for i in range(count):
        time = input_check(input().lower(), ['1', "15 мин", '2', "1 час", '3', "1-2 часа", '4', "3+ часов"])
        if time in ['1', "15 мин"]:
            result += 15
        elif time in ['2', "1 час"]:
            result += 60
        elif time in ['3', "1-2 часа"]:
            result += 120
        elif time in ['4', "3+ часов"]:
            result += 240
    result //= count
    return result


def get_difficult(count):
    result = 0
    for i in range(count):
        difficult = input_check(input().lower(), ['1', "легко", '2', "средне", '3', "сложно"])
        if difficult in ['1', "легко"]:
            result += 1
        elif difficult in ['2', "средне"]:
            result += 3
        else:
            result += 5
    result //= count
    return result


def get_genre(category):
    vertex = [str(n) for n in input().split()] # Выбор
    return create_graf(category, vertex)


def get_coef(average, val_1, val_2):
    game_val = (val_1 + val_2) / 2
    difference = max(average, game_val) - min(average, game_val)
    if difference:
        return difference
    else:
        return 1


def debug(number_players, category, time, difficult, genres):
    print()
    print("Количество игроков: ", number_players)
    print("Категория: ", category)
    print("Время: ", time)
    print("Сложность: ", difficult)
    print("Жанры: ", genres)
    print()


def main():
    number_players = int(input("Введите количество игроков: "))

    print("По очереди введите категорию (1: подумать; 2: посмеяться):")
    category = get_category(number_players)

    print("По очереди введите время (1: 15 мин; 2: 1 час; 3: 1-2 часа; 4: 3+ часов):")
    time = get_time(number_players)

    print("По очереди введите сложность (1: легко; 2: средне; 3: сложно):")
    difficult = get_difficult(number_players)

    print(category)
    if(category == "laugh"):
        print("Выберете жанры и введите их через пробел (слова, ассоциации, порисовать, поговорить, поржать):")
    else :
        print("Выберете жанры и введите их через пробел (евро, попиздиться, area_control, колодострой, городострой, стратегии, кооператив, скрытые_роли, приключенческие_кампании, лавкрафт, детектив, евро, стратегии):")
    genres = get_genre(category)

    debug(number_players, category, time, difficult, genres)

    connection = create_connection(f"data\\bd\\{category}_categ.sqlite")

    result = {}

    if (category == "laugh"):
        select_games = f"SELECT * from party"
    else:
        select_games = f"SELECT * from think"

    games = execute_read_query(connection, select_games)

    for game in games:

        # suitable - коэф насколько подходит игра, изначально равна коэф. жанра
        suitable = genres[game[7]]

        coef = get_coef(time, game[4], game[5])  # коэф. времени
        suitable *= 1 / coef

        coef = get_coef(number_players, game[2], game[3])  # коэф. кол-ва игроков
        suitable *= 1 / coef

        coef = get_coef(difficult, game[3], game[6])  # коэф. сложности
        suitable *= 1 / coef * 3  # в три раза сильнее влияет чем время

        if not game[2] <= number_players <= game[3]:
            suitable *= 0 # если не подходит по кол-ву игроков не предлогаем игру

        # по ключу равному id игры, сопоставляем suitable
        result[game[0]] = suitable / 4  # делим на 4 для критерия Лапласа

    result = sorted(result.items(), key=itemgetter(1), reverse=True)
    for game in result:
        print(showName(connection, game[0], category))
        print(game[1])


if __name__ == '__main__':
    main()
