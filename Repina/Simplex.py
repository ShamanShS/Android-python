# import pandas as pd #необходимо для оформления симлекс-таблиц
import copy
import scipy
import scipy.optimize
dele = 0


def Simplex(a, C, pr = 1):
    a[-1] = delta(a, C)
    if (pr == 1):
        print_table(a)
    return simplexMetod(a, C, pr)

def Analysis2(a, C, newP0, Basis):
    B_1 = []
    for i in range(len(Basis)):
       B_1.append([0] * len(Basis))
       for j in range(len(Basis)):
           B_1[i][j] = a[i][Basis[j] + 2]
    BP = mult_matrix(newP0, B_1)
    for i in range(len(BP)):
        a[i][2] = BP[i]

    delt = delta(a, C)
    a[-1] = delt

    print_table(a)
    for i in range(len(a) - 1):
        if (a[i][2] < 0):
            if double_simplex(a,C) == -1:
                 return -1
            break
    return a

def print_res(a, expenses = 0):
    f_x = a[len(a) - 1][2]
    x = [0] * 3
    for i in range(len(a) - 1):
        if (a[i][0] > 0 and a[i][0] < 4):
            x[a[i][0] - 1] = a[i][2]
    print(f"x* = {x}; f(x*) = {f_x}\n Чистая прибль {(-f_x - expenses)}")


def print_table(a, iter = -1):
    col = ['B','Cb','X_']
    for i in range (1, len(a[0]) - 2):
        col.append(f'X{i}')
    task = pd.DataFrame(columns = col,data = a)
    if (iter != -1):
        print(f"Итерация {iter}")
    print(task)

def simplexMetod(a, c, pr = 1):
    flag = True
    iter = 0
    flag_w = True
    while(flag):
        iter += 1
        flag_w = False
        for i in range(len(a) - 1):
            if (a[i][1] == 'w'):
                flag_w = True
                break

        if (flag_w):
            a = replacement_w(a, c)
        else:
            a = replacement(a, c)

        delt = delta(a, c)
        a[-1] = delt
        if (pr == 1):
            print_table(a, iter)

        flag = False
        for i in range(3, len(delt) - dele):
            if (delt[i] > 0):
                flag = True
    return a

def double_simplex(a, c):
    flag = True
    iter = 0
    while(flag):
        iter += 1
        a = double_replacement(a, c)
        if (a == -1):
            return -1
        delt = delta(a, c)
        a[-1] = delt

        print_table(a, iter)

        flag = False
        for i in range(len(a) - 1):
            if (a[i][2] < 0):
                flag = True
    

        
def double_replacement(a, c):
    max_j = 0
    max_vali = 0
    min_valj = 10000000
    min_i = 15
    for j in range(3, len(a[0])):
        if (a[len(a) - 1][j] < 0 and max_vali < abs(a[len(a) - 1][j])):
            for i in range(len(a) - 1):
                if (a[i][j] < 0 and a[i][2] < 0):
                    if (a[i][2] / a[i][j] < min_valj):
                        min_i = i
                        min_valj = a[i][2] / a[i][j]
                        max_j = j
                        max_vali = abs(a[len(a) - 1][j])
    a[min_i][0] = max_j - 2
    a[min_i][1] = c[max_j - 3]
    a[min_i] = div_vec(a[min_i], a[min_i][max_j])

    for i in range(len(a) - 1):
        if (a[i][max_j] != 0 and i != min_i):
            a[i] = add_vec(a[i], a[min_i], -a[i][max_j])
    return a

    

def delta(a, c):
    delt = [0] * len(a[0])
    for i in range(2, len(delt)):
        if (c[i - 3] == 'w'):
            delt[i] = scalar(a, i, 1) - 1
        else:
              delt[i] = scalar(a, i, 1) - c[i - 3]
    return delt

def scalar(a, x, y):
    res = 0
    for i in range(len(a) - 1):
        if (a[i][y] == 'w'):
            res += a[i][x]
        else:
            res += a[i][x] * a[i][y]
    return res

def replacement_w(a, c):
    global dele
    max_j = 0
    max_i = 0
    flag = False
    for i in range(len(a)-1):
        if (a[i][1] == 'w'):
            for j in range(3, len(a[0]) - dele):
                if (a[i][j] > 0 and a[len(a) - 1][j] > 0):
                    max_j = j
                    max_i = i
                    flag = True
                    break
        if (flag):
            break

    temp = a[max_i][0]
    a[max_i][0] = max_j - 2
    a[max_i][1] = c[max_j - 3]
    a[max_i] = div_vec(a[max_i], a[max_i][max_j])

    for i in range(len(a) - 1):
        if (a[i][max_j] != 0 and i != max_i):
            a[i] = add_vec(a[i], a[max_i], -a[i][max_j])
    # delete_vec(a, temp)
    
    dele += 1
    print(dele)
    return a

def replacement(a, c):
    max_j = 0
    max_vali = 0
    min_valj = 10000000
    min_i = 15
    for j in range(3, len(a[0]) - dele):
        if (a[len(a) - 1][j] > 0 and max_vali < a[len(a) - 1][j]):
            for i in range(len(a) - 1):
                if (a[i][j] > 0):
                    if (a[i][2] / a[i][j] < min_valj):
                        min_i = i
                        min_valj = a[i][2] / a[i][j]
                        max_j = j
                        max_vali = a[len(a) - 1][j]

    a[min_i][0] = max_j - 2
    a[min_i][1] = c[max_j - 3]
    a[min_i] = div_vec(a[min_i], a[min_i][max_j]) #деление вектора на число, которое нужно сделать единицей

    for i in range(len(a) - 1):
        if (a[i][max_j] != 0 and i != min_i):
            a[i] = add_vec(a[i], a[min_i], -a[i][max_j]) #сладывание векторов
    return a

def delete_vec(a, val):
    for i in range(len(a)):
        a[i].pop(val + 2 - dele) 

def div_vec(vec, val):
    for i in range(2, len(vec)):
        vec[i] = round(vec[i] / val, 3)
    return vec

def add_vec(vec1, vec2, val):
    for i in range(2, len(vec1)):
        vec1[i] = round(vec1[i] + vec2[i] * val, 3)
    return vec1

def sub_vec(vec1, vec2, val):
    for i in range(2, len(vec1)):
        vec1[i] = round(vec1[i] - vec2[i] * val, 3)
    return vec1

def mult_matrix(a, b):
    res = [0] * len(a)
    for j in range(len(b)):
        sum_val = 0
        for r in range(len(a)):
            sum_val += a[r] * b[j][r]
        res[j] = sum_val
    return res
