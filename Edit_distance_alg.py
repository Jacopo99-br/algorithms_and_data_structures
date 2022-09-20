# PROGRAMMA PER LA CREAZIONE DELL ALGORITMO EDIT DISTANCE

# function for the operations of edit-distance:

#def copy(X,Y):
import os
import distance
from nltk.util import ngrams



def accent_check(word):
    if("a'" in word):
        word=word.replace("a'","à")
    if("e'" in word):
        word=word.replace("e'","è")
    if("i'" in word):
        word=word.replace("i'","ì")
    if("o'" in word):
        word=word.replace("o'","ò")
    if("u'" in word):
        word=word.replace("u'","ù")
    return word

#X = list(input("inserisci stringa X "))
#Y = list(input("inserisci stringa Y "))

def printlist(list):
    for i in list:
        print(i)


def cost(string):
    if(string in ["copy"]):
        return 0
    return 1

def Edit_Distance(X,Y):
    m = len(X)
    n = len(Y)
    c = [[float("inf") for i in range(n + 1)] for j in range(m + 1)]

    op = []
    for i in range(0,m):
        riga = []

        op.append(riga)
        for j in range(n):
            riga.append(" ")


    for i in range(0, m + 1):
        c[i][0] = i * cost("delete")
    for j in range(0, n + 1):
        c[0][j] = j * cost("insert")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + cost("copy")
            else:
                c[i][j] = c[i - 1][j - 1] + cost("replace")
            if i >= 2 and j >= 2 and X[i - 1] == Y[j - 2] and X[i - 2] == Y[j - 1] and c[i - 2][j - 2] + cost(
                    "twiddle") < c[i][j]:
                c[i][j] = c[i - 2][j - 2] + cost("twiddle")
            if c[i - 1][j] + cost("delete") < c[i][j]:
                c[i][j] = c[i - 1][j] + cost("delete")
            if c[i][j - 1] + cost("insert") < c[i][j]:
                c[i][j] = c[i][j - 1] + cost("insert")
    return c[m][n]

def decompose(string,n):
    string_splitted=string.split()
    #print(string_splitted)
    #print(n)
    return ngrams(string_splitted[0],n+1)

def jaccard(s1,s2):
    return distance.jaccard(s1, s2)

def comparing(path,x): #compara la parola presa con le parole del file e crea una lista con  tutte le parola con distanza minima
    #creo una lista dove metto tutti i minimi che trovo leggendo il file e confrontandoli con x
    min_list=[]
    min=[None,len(x)]
    min_list.append(min)
    f=open(path,'r')
    for y in f:
        y.rstrip()
        dist=Edit_Distance(x,y)
        if dist<min[1]:
            min[0]=y
            min[1]=dist
            min_list.append(min)
    f.close()

    return min #restituisco il minimo con la parola corrispondente
def n_gram_comparing(path,X,n):
    if n==0:
        comparing(path,X)
    n_path=path.split("/")[1].split(".")[0]
    X_decomposed=decompose(X,n)
    X_decomposed=list(X_decomposed)
    CJ = 0.0
    CJ_limit = 0.6
    min = [None, len(X)]
    list_of_min = []
    list_of_min.append(min)
    for i in X_decomposed:
        file = str(n_path) + "/" + str(n+1) + "-gram/" + str(X_decomposed[X_decomposed.index(i)]) + "_"
        if os.path.isfile(file):
            f = open(file, 'r')
            for y in f:
                y = y.rstrip()
                y_decomposed = decompose(y, n)
                jac = jaccard(X_decomposed, y_decomposed)
                if CJ_limit < jac:
                    dist = Edit_Distance(X, y)
                    if dist < min[1]:
                        min[0] = y
                        min[1] = dist
                        CJ = jac
                        list_of_min.append(min)
            f.close()


    return min, CJ

def file_to_gram(path, n_gram):
    #path_ = ((path.split(".")[0]).split("/"))[1].split("_")[0]
    path_ = path.split("/")[1].split(".")[0]
    if not os.path.exists(str(path_)):
        os.makedirs(str(path_))
        fp = open(path)
        for num, j in enumerate(fp):
            line = j.rstrip()
            line=accent_check(line)
            if str(line).__eq__("\n") or str(line).__eq__("\t") or str(line).__eq__("\r") or str(line).__eq__("") or str(line).__eq__('') :
                continue
            for k in range(n_gram):
                if not os.path.exists(str(path_)+"/"+str(k + 1) + "-gram"):
                    os.makedirs(str(path_)+"/"+str(k + 1) + "-gram")
                line_gram = decompose(line, k)
                # funzione che elimina gli elementi uguali
                #line_gram = dict.fromkeys(line_gram).keys()
                #line_gram=set(line_gram)
                line_gram_set=list(line_gram)

                for i in range(len(line_gram_set)):
                    file_name=str(line_gram_set[i])
                    if("\'" in file_name):
                        file_name=file_name.replace('\"','\'')
                    f = open(str(path_)+"/"+str(k+1)+"-gram/"+file_name+"_", 'a')
                    f.write(str(line)+'\n')
        fp.close()
