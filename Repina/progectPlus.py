import pandas as pd #необходимо для оформления симлекс-таблиц
import copy
import scipy
import scipy.optimize
dele = 0

def delta(a, c):
    delt = [0] * (16 - dele)
    for i in range(2, len(delt)):
        if (c[i - 3] == 'w'):
            delt[i] = scalar(a, i, 1) - 1
        else:
              delt[i] = scalar(a, i, 1) - c[i - 3]
    return delt

def scalar(a, x, y):
    res = 0
    for i in range(len(a)):
        if (a[i][y] == 'w'):
            res += a[i][x]
        else:
            res += a[i][x] * a[i][y]
    return res

def replacement_w(a, c):
    max_j = 0
    max_i = 0
    max_vali = 0
    flag = False
    for i in range(len(a)-1):
        if (a[i][1] == 'w'):
            for j in range(3, len(a)):
                if (a[i][j] > 0 and a[5][j] > 0):
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
    delete_vec(a, temp)
    global dele
    dele += 1
    return a

def replacement(a, c):
    max_j = 0
    max_vali = 0
    min_valj = 10000000
    min_i = 15
    for j in range(3, len(a[5])):
        if (a[5][j] > 0 and max_vali < a[5][j]):
            for i in range(len(a) - 1):
                if (a[i][j] > 0):
                    if (a[i][2] / a[i][j] < min_valj):
                        min_i = i
                        min_valj = a[i][2] / a[i][j]
                        max_j = j
                        max_vali = a[5][j]

    # min_i = 0
    # min_valj = 10000000
    # for i in range(len(a) - 1):
    #     if (a[i][max_j] > 0 and a[i][2] >= 0):
    #         if (a[i][2] / a[i][max_j] < min_valj):
    #             min_i = i
    #             min_valj = a[i][2] / a[i][max_j]

    a[min_i][0] = max_j - 2
    a[min_i][1] = c[max_j - 3]
    a[min_i] = div_vec(a[min_i], a[min_i][max_j])

    for i in range(len(a) - 1):
        if (a[i][max_j] != 0 and i != min_i):
            a[i] = add_vec(a[i], a[min_i], -a[i][max_j])
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


col = ['B','Cb','X_','X1','X2','X3','X4','X5','X6','X7','X8', 'X9', 'X10', 'X11', 'x12', 'x13']
maxC = 13
x = [[] * 2] * 5
B = []
b = []
c = []
C = [0] * maxC
f = open("planPlus.txt", "r")
B = list(map(int ,f.readline()[3::].split(',')))#Кол-во ресурсов
x[0] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 1
x[1] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 2
x[2] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 3
x[3] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 3
x[4] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 3
bi = list(map(int ,f.readline()[3::].split(',')))#Издержки за ед рес
c = list(map(int ,f.readline()[3::].split(',')))#Стоимость товара
bb = list(map(int ,f.readline()[3::].split(',')))#План продаж
for i in range(len(bb)):
    B.append(bb[i])

for i in range(5):
    C[i] = -(c[i] - (bi[0] * x[i][0] + bi[1] * x[i][1]))
for i in range(5, 10):
    C[i] = 0
for i in range(10, 13):
    C[i] = "w"
# print(C)

A = []
for i in range(5):
    A.append([0] * maxC)
for i in range(2):
    for j in range(5):
        A[i][j] = x[j][i]
A[0][5] = 1
A[1][6] = 1
A[2][7] = -1
A[2][0] = 1
A[3][1] = 1
A[4][2] = 1
A[3][8] = -1
A[4][9] = -1
A[2][10] = 1
A[3][11] = 1
A[4][12] = 1


basis = [6, 7, 11, 12, 13]
lin_prog = A
for x in range(5):
  lin_prog[x].insert(0,B[x])
  lin_prog[x].insert(0,basis[x])
  lin_prog[x].insert(1,C[basis[x] - 1])
delt = delta(lin_prog, C)
lin_prog.append(delt)
task = pd.DataFrame(columns = col,data = lin_prog)
temp = copy.deepcopy(lin_prog)
for i in range(len(lin_prog)):
    print(lin_prog[i])
print(task)
flag = True
a = temp
iter = 0
flag_w = True
while(flag):
    iter += 1
    if (iter == 10):
        x += 1 
    flag_w = False
    for i in range(len(a) - 1):
        if (a[i][1] == 'w'):
            flag_w = True
            break
    if (flag_w):
        a = replacement_w(a, C)
        col.pop(-1)
        if (len(a[1]) == 12):
            x = 1
    else:
        a = replacement(a, C)
    delt = delta(a, C)
    a[-1] = delt
    task = pd.DataFrame(columns = col,data = a)
    print(f"Итерация{iter}")
    print(task)
    flag = False
    for i in range(3, len(delt)):
        if (delt[i] > 0):
            flag = True

B1 = B[0:2]
print(B1)
A1 = [[2, 5, 0],
      [0, 30, 2]]
C1 = [-110, -5000, -18]
B1 = [210,1100]
res = scipy.optimize.linprog(C1, A_ub = A1, b_ub= B1, bounds=(10, None))
print(res)