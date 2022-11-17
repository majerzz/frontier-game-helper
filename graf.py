import math
from operator import itemgetter


def create_graf(category, vertex):

    f = open(f"data\\graf\\{category}_categ.txt", "r", encoding="utf-8")
    data = [line.strip() for line in f]
    f.close()

    k = 0
    vert_count = int(data[k])  # Кол-во жанров
    k += 1
    V = [[math.inf] * vert_count for i in range(vert_count)]  # Массив графа
    edges_count = int(data[k])  # Кол-во связей
    k += 1
    grafOne = {}
    grafTwo = {}

    for i in range(vert_count):  # названия жанров
        j = data[k]
        grafOne[j] = i
        grafTwo[i] = j
        k += 1

    for i in range(edges_count):  # между какими жанрами есть связь
        a, b = map(str, data[k].split(' '))
        k += 1
        V[grafOne[a]][grafOne[b]] = float(data[k])
        V[grafOne[b]][grafOne[a]] = float(data[k])
        k += 1

    for i in range(vert_count):
        for j in range(vert_count):
            V[j][i] = V[i][j]

    for i in range(vert_count):
        V[i][i] = 0  # Длина массива

    for k in range(vert_count):
        for i in range(vert_count):
            for j in range(vert_count):
                d = V[i][k] + V[k][j]
                if V[i][j] > d:
                    V[i][j] = d

    vertexNums = []

    for i in vertex:
        vertexNums.append(grafOne[i])

    sumToVertex = [0] * vert_count  # Длины путей
    for i in range(vert_count):
        for j in vertex:
            sumToVertex[i] += V[i][grafOne[j]]
            sumToVertex[i] = round(sumToVertex[i], 2)

    maximum = max(sumToVertex)
    minimum = min(sumToVertex)
    genre = {}

    for i in range(vert_count):
        genre[grafTwo[i]] = sumToVertex[i]

    return dict(sorted(genre.items(), key=itemgetter(1)))