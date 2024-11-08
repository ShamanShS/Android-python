import pandas as pd #необходимо для оформления симлекс-таблиц
import copy
import scipy
import scipy.optimize
dele = 0
col = ['B','Cb','X_','X1','X2','X3','X4','X5','X6','X7','X8', 'X9', 'X10', 'X11']

def print_res(a):
    f_x = a[len(a) - 1][2]
    x = [0] * 3
    for i in range(len(a) - 1):
        if (a[i][0] > 0 and a[i][0] < 4):
            x[a[i][0] - 1] = a[i][2]
    print(f"x* = {x}; f(x*) = {f_x}")


def print_table(a, iter = -1):
    col = ['B','Cb','X_']
    for i in range (1, len(a[0]) - 2):
        col.append(f'X{i}')
    # print(col)
    # for i in a:
    #     print(i)
    task = pd.DataFrame(columns = col,data = a)
    if (iter != -1):
        print(f"Итерация {iter}")
    print(task)

def simplex(a, c):
    flag = True
    iter = 0
    flag_w = True
    Basis_1 = []
    flag_B = True
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
            if (flag_B):
                flag_B = False
                for i in range(len(a) - 1):
                    Basis_1.append(a[i][0])
            a = replacement(a, c)

        delt = delta(a, c)
        a[-1] = delt

        print_table(a, iter)

        flag = False
        for i in range(3, len(delt) - dele):
            if (delt[i] > 0):
                flag = True
    return a, Basis_1

def double_simplex(a, c):
    flag = True
    iter = 0
    while(flag):
        iter += 1
        a = double_replacement(a, c)
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
    # print(a[min_i])

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
    for i in range(len(a)):
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



maxC = 11
xlist = [[] * 2] * 3
B = []
b = []
c = []
C = [0] * maxC
f = open("plan.txt", "r")
B = list(map(int ,f.readline()[3::].split(',')))#Кол-во ресурсов
xlist[0] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 1
xlist[1] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 2
xlist[2] = list(map(int ,f.readline()[3::].split(',')))#ПРоизводство товара 3
bi = list(map(int ,f.readline()[3::].split(',')))#Издержки за ед рес
c = list(map(int ,f.readline()[3::].split(',')))#Стоимость товара
bb = list(map(int ,f.readline()[3::].split(',')))#План продаж
f.close()
for i in range(len(bb)):
    B.append(bb[i])

for i in range(3):
    C[i] = -(c[i] - (bi[0] * xlist[i][0] + bi[1] * xlist[i][1]))
for i in range(3, 8):
    C[i] = 0
for i in range(8, 11):
    C[i] = "w"
# print(C)

A = []
for i in range(5):
    A.append([0] * maxC)
for i in range(2):
    for j in range(3):
        A[i][j] = xlist[j][i]
A[0][3] = 1
A[1][4] = 1
A[2][5] = -1
A[2][0] = 1
A[3][1] = 1
A[4][2] = 1
A[3][6] = -1
A[4][7] = -1
A[2][8] = 1
A[3][9] = 1
A[4][10] = 1


basis = [4, 5, 9, 10, 11]
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

print(C)
a = temp
a, Basis_1 = simplex(a,C)
print_res(a)

f = open("plan.txt", "r")
B1 = list(map(int ,f.readline()[3::].split(',')))
f.close()

A1 = []
for j in range(2):
    A1.append([xlist[0][j], xlist[1][j], xlist[2][j]])

C1 = [0] * 3
for i in range(3):
    C1[i] = -(c[i] - (bi[0] * xlist[i][0] + bi[1] * xlist[i][1]))

res = scipy.optimize.linprog(C1, A_ub = A1, b_ub= B1, bounds=[(bb[0], None),(bb[1], None),(bb[2], None)])
print(res)

Basis_1 = basis.copy()
# print(Basis_1)

# for i in range(len(a) - 1):
#         Basis_1[i] = a[i][0]

B_1 = []
for i in range(len(Basis_1)):
    B_1.append([0] * len(Basis_1))
    for j in range(len(Basis_1)):
        B_1[i][j] = a[i][Basis_1[j] + 2]
        
# for i in B_1:
#     print(i)

P_0 = [150, 2000, 10, 10, 10] #Новые ограничения

BP = mult_matrix(P_0, B_1)

for i in range(len(BP)):
    a[i][2] = BP[i]

delt = delta(a, C)
a[-1] = delt

task = pd.DataFrame(columns = col,data = a)
print(task)
for i in range(len(a) - 1):
    if (a[i][2] < 0):
        double_simplex(a,C)
        break
print_res(a)


B1 = [P_0[0], P_0[1]]

A1 = []
for j in range(2):
    A1.append([xlist[0][j], xlist[1][j], xlist[2][j]])

C1 = [0] * 3
for i in range(3):
    C1[i] = -(c[i] - (bi[0] * xlist[i][0] + bi[1] * xlist[i][1]))

res = scipy.optimize.linprog(C1, A_ub = A1, b_ub= B1, bounds=[(P_0[2], None),(P_0[3], None),(P_0[4], None)])
print(res)
# print(Basis_1)





