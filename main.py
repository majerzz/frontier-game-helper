from graf import *
from bd_work import *
from itertools import repeat
import random
from flask import Flask, render_template, request, redirect, session



def get_category(cat_think, cat_laugh):
    if cat_think > cat_laugh:
        return "think"
    elif cat_think < cat_laugh:
        return "laugh"
    else:
        return random.choice(["подумать", "посмеяться"])


def get_time(result, count):
    result //= count
    return result


def get_difficult(result, count):
    result //= count
    return result


def get_genre(category, genres):
    return create_graf(category, genres)


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
    app = Flask(__name__)

    global t_slider_time #время
    global cat #категория
    global dif #сложность
    global laugh, think
    global genres #массив с жанрами

    t_slider_time = 0
    cat = 0
    dif = 0
    laugh = 0
    think = 0

    app = Flask(__name__)

    @app.route("/")
    def index():
        t_slider_time = 0
        session["t_slider_time"] = t_slider_time
        cat = 0
        session["cat"] = cat
        dif = 0
        session["dif"] = dif
        laugh = 0
        session["laugh"] = laugh
        think = 0
        session["think"] = think
        return render_template('one.html')

    @app.route("/2", methods=['GET', 'POST'])
    def index2():
        return render_template('two.html')

    @app.route('/3', methods=['GET', 'POST'])
    def index3():
        needValues = request.values.to_dict()
        number_players = needValues['count1']
        session["number_players"] = number_players
        fixed_players = int(number_players)
        session["fixed_players"] = fixed_players
        if "fixed_players" in session:
            return render_template('three.html')

    @app.route('/4', methods=['GET', 'POST'])
    def index4():
        number_players = session["number_players"]
        fixed_players = session["fixed_players"]
        dif = session["dif"]

        needValues = request.values.to_dict()
        session["difficulty"] = needValues['radio2']
        difficulty = session["difficulty"]

        d = int(difficulty)
        if(d == 1):
            d = 1
        elif (d == 2):
            d = 3
        elif (d == 3):
            d = 5

        dif += d

        if (int(number_players) == 1):
            sss_dif = get_difficult(dif, fixed_players)
            print(sss_dif, "СЛОЖНОСТЬ", fixed_players)
            session["sss_dif"] = sss_dif

        print(needValues['radio2'])
        return render_template('four.html')

    @app.route('/5', methods=['GET', 'POST'])
    def index5():
        t_slider_time = session["t_slider_time"]
        number_players = session["number_players"]
        fixed_players = session["fixed_players"]

        needValues = request.values.to_dict()
        session["slider_time"] = needValues['slider']
        slider_time = session["slider_time"]

        t = int(slider_time)
        if (t >= 1 and t <= 15):
            t = 15
        elif (t >= 16 and t <= 60):
            t = 60
        elif (t >= 61 and t <= 120):
            t = 120
        else:
            t = 360
        t_slider_time += t
        print(t_slider_time, "вРЕМЯ")
        if (int(number_players) == 1):
            session["sss_time"] = get_time(t_slider_time, fixed_players)
            sss_time = session["sss_time"]
            print(sss_time, " ВРЕМЯ", fixed_players)
        return render_template('five.html')

    @app.route('/6', methods=['POST'])
    def index6():
        cat = session["cat"]
        laugh = session["laugh"]
        think = session["think"]
        number_players = session["number_players"]

        needValues = request.values.to_dict()
        cat = needValues['radio1']
        session["cat"] = cat

        c = int(cat)
        if (c == 1):
            laugh += 1
        elif (c == 2):
            think += 1

        if (int(number_players) == 1):
            session["sss_cat"] = get_category(think, laugh)
            sss_cat = session["sss_cat"]
            print(sss_cat, " - Категория")

        if (int(number_players) > 1):
            t = int(number_players)
            t -= 1
            number_players = t
            session["number_players"] = number_players
            return render_template('three.html')

        if request.method == 'POST':
            if needValues['radio1'] == '1':
                return render_template('six.html')
            elif needValues['radio1'] == '2':
                return render_template('seven.html')
        else:
            pass


    @app.route('/8', methods=['GET', 'POST'])
    def index8():
        global genres
        cat = session["cat"]
        global select_games
        fixed_players = session["fixed_players"]
        session["scat"] = "whaa"
        session["icat"] = int(cat)
        icat = session["icat"]
        if (icat == 1):
            needValues = request.form.getlist('checkbox1')
            session["needValues"] = needValues
            print(needValues)
            session["scat"] = "laugh"
        elif (icat == 2):
            needValues = request.form.getlist('checkbox2')
            session["needValues"] = needValues
            print(needValues)
            session["scat"] = "think"
        needValues = session["needValues"]
        scat = session["scat"]

        session["genres"] = get_genre(scat, needValues)
        genres = session["genres"]
        connection = create_connection(f"data\\bd\\{scat}_categ.sqlite")

        if (scat == "laugh"):
            select_games = f"SELECT * from party"
        else:
            select_games = f"SELECT * from think"

        result = {}

        games = execute_read_query(connection, select_games)

        for game in games:

            # suitable - коэф насколько подходит игра, изначально равна коэф. жанра
            suitable = genres[game[7]]

            coef = get_coef(t_slider_time, game[4], game[5])  # коэф. времени
            suitable *= 1 / coef

            coef = get_coef(fixed_players, game[2], game[3])  # коэф. кол-ва игроков
            suitable *= 1 / coef

            coef = get_coef(dif, game[3], game[6])  # коэф. сложности
            suitable *= 1 / coef * 3  # в три раза сильнее влияет чем время

            if not game[2] <= fixed_players <= game[3]:
                suitable *= 0  # если не подходит по кол-ву игроков не предлогаем игру

            # по ключу равному id игры, сопоставляем suitable
            result[game[0]] = suitable / 4  # делим на 4 для критерия Лапласа

        result = sorted(result.items(), key=itemgetter(1), reverse=True)

        x = 0
        mylist = ["a", "b", "c", "d", "e", "f"]

        for game in result:

            print(showName(connection, game[0], scat))
            mylist[x] = showName(connection, game[0], scat)
            print(game[1])
            x+=1

            if(x == 6):
                break
        print(mylist)
        return render_template('eight.html', data=mylist)


    if __name__ == "__main__":
        app.secret_key = 'super secret key'
        app.run(debug=True)

if __name__ == '__main__':
    main()