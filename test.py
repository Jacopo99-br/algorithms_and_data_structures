# -*- coding: utf-8 -*-
from Edit_distance_alg import *
import random
from timeit import default_timer as timer
import pickle


path = ["paroleitaliane/9000_nomi_propri.txt",    "paroleitaliane/1000_parole_italiane_comuni.txt",   "paroleitaliane/400_parole_composte.txt"]
#path = ["paroleitaliane/9000_nomi_propri.txt",    "paroleitaliane/60000_parole_italiane111.txt",   "paroleitaliane/280000_parole_italiane.txt"]

#prendo 3 parole da 3 file diversi creando l'indice 3-gram
n_word = 1
n_type = 6
n_gram = 3

c = [[] for i in range(len(path))]
_parola = [[] for i in range(0, len(path))] #vettore delle parole
for i in range(len(path)): #####################################################################togliere 1
    _parola[i] = [] #per ogni _parola ho un altro vettore
    #file_to_gram(path[i], n_gram)
    #TO_DO
    file_to_gram(path[i], n_gram)
    path_ = (path[i].split("/"))[1].split("_")[0]
    # prendo n_word parole a caso dal file in considerazione ,in questo caso nword è 1 quindi 1 parola dal file
    for k in range(n_word):
        fp = open(path[i])
        rand = int(random.uniform(0, int(
            ((path[i].split("/"))[1].split("_")[0]))))
        for j, line in enumerate(fp):
            if j == rand:
                line=accent_check(line)
                _parola[i].append(line.rstrip()) #rstrip per levare lo spazio in fondo
        fp.close()

    c[i] = [[] for j in range(n_word)] #array num parole prese da ciascun file
    for j in range(n_word):
        c[i][j] = [[] for k in range(n_gram)] # per ogni parola fo l'indice 3-gram
        for k in range(n_gram): #entro 3 volte qui dentro

            # ricerca stringa vicina al primo elemento di _parola
            start = timer()
            A, CJ = n_gram_comparing(path[i], _parola[i][j], k) #n-gram_comparing inserisco il file ,la parola che mi interessa del file
                                                                # e il numero di gram che sto facendo.
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end-start)
            c[i][j][k].append(CJ)

            # ricerca stringa randomizzata
            tmp = ''.join(random.sample(_parola[i][j],len(_parola[i][j])))
            start = timer()
            A, CJ = n_gram_comparing(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # parola senza un elemento
            tmp = _parola[i][j]
            midlen = int(len(tmp) / 2)
            tmp = tmp[:midlen] + tmp[midlen + 1:]
            start = timer()
            A, CJ = n_gram_comparing(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # perola con un elemento random
            tmp = _parola[i][j]
            midlen = int(len(tmp) / 2)
            tmp = tmp[:midlen] + chr(int(random.uniform(97, 122)))+tmp[midlen:]
            start = timer()
            A, CJ = n_gram_comparing(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # 1 SCAMBIATE CON LE VICINE
            a = ['s', 'q', 'z']
            v = ['c', 'f', 'g', 'b']
            y = ['t', 'g', 'h', 'u']
            u = ['i', 'j', 'h', 'y']
            l = ['p', 'o', 'k']
            tmp = ''
            count = None
            print(_parola[i][j])
            for char in _parola[i][j]:
                if char in a and count is None:
                    char = a[int(random.uniform(0, len(a)))]
                    count = 1
                elif char in v and count is None:
                    char = v[int(random.uniform(0, len(v)))]
                    count = 1
                elif char in y and count is None:
                    char = y[int(random.uniform(0, len(y)))]
                    count = 1
                elif char in u and count is None:
                    char = u[int(random.uniform(0, len(u)))]
                    count = 1
                elif char in l and count is None:
                    char = l[int(random.uniform(0, len(l)))]
                    count = 1
                tmp = tmp + char
            if count is None:
                randi = int(random.uniform(0, len(tmp)))
                tmp = tmp[:randi]+chr(ord(list(tmp)[randi])+1)+tmp[randi+1:]
            start = timer()
            A, CJ = n_gram_comparing(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)


            # 2 SCAMBIATE CON LE VICINE
            tmp = ''
            count = 0
            for char in _parola[i][j]:
                if char in a and count < 2:
                    char = a[int(random.uniform(0, len(a)))]
                    count += 1
                elif char in v and count < 2:
                    char = v[int(random.uniform(0, len(v)))]
                    count += 1
                elif char in y and count < 2:
                    char = y[int(random.uniform(0, len(y)))]
                    count += 1
                elif char in u and count < 2:
                    char = u[int(random.uniform(0, len(u)))]
                    count += 1
                elif char in l and count < 2:
                    char = l[int(random.uniform(0, len(l)))]
                    count += 1
                tmp = tmp + char
            if count < 2:
                randi = int(random.uniform(0, len(tmp)))
                tmp = tmp[:randi]+chr(ord(list(tmp)[randi])+1)+tmp[randi+1:]
                count += 1
            if count < 2:
                randi = int(random.uniform(0, len(tmp)))
                tmp = tmp[:randi]+chr(ord(list(tmp)[randi])+1)+tmp[randi+1:]
            start = timer()
            A, CJ = n_gram_comparing(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

with open('c.pkl','wb') as c_file:
    pickle.dump(c,c_file)
#pickle.dump(c, open("c.pickle","wb"))
with open('parola.pkl','wb') as parola_file:
    pickle.dump(_parola,parola_file)
#pickle.dump(_parola, open("parola.pickle", "wb"))

res = [[] for i in range(len(path))]
med = [[] for i in range(len(path))]

for i in range(len(path)):
    res[i] = [[0]*n_type*3 for j in range(n_gram)]
    med[i] = [0]*n_gram
    for k in range(n_word):
        for l in range(n_gram):
            for j in range(n_type*3):
                res[i][l][j] = ((int(res[i][l][j])*int(med[i][l])) + (c[i][k][l][j][1] if isinstance(c[i][k][l][j],
                    (list, tuple)) else c[i][k][l][j]))/(med[i][l]+1)
            med[i][l] += 1

with open('res.pkl','wb') as res_file:
    pickle.dump(res,res_file)
#pickle.dump(res, open("res.pickle", "wb"))

