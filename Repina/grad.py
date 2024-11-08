import Simplex

def Grad(dictFile, x0):
    a = 1
    Fdx1 = Derivative(dictFile['F'], 1)
    Fdx2 = Derivative(dictFile['F'], 2)
    fx0 = funk_F(Fdx1, Fdx2, x0)
    print(f"Grad = {fx0}")
    if (fx0[0] == 0 and fx0[1] == 0):
        return
    C = fx0
    a, C = GradSimplex(dictFile, C)
    
    # Simplex.print_table(a)
    # print(C)
    a = Simplex.Simplex(a, C, 0)
    # Simplex.print_table(a)
    # res = scipy.optimize.linprog([-4, 1], A_ub = [[2,-1],[-1,2]], b_ub= [2,2])
    # print(res)
    x_0 = [0, 0]
    for i in range (2):
        if (a[i][0] < 3):
            x_0[a[i][0] - 1] = a[i][2]
    
    s0 = [x_0[0] - x0[0], x_0[1] - x0[1]]
    
    x1 = [[x0[0],s0[0]],[x0[1],s0[1]]]
    newf = substitute(dictFile['F'], x1)
    
    lam = -newf[1] / (newf[0] * 2)
    
    x_1 = [x0[0] + lam * s0[0], x0[1] + lam * s0[1]]
    # print(Fdx1)
    # print(Fdx2)
    # print(fx0)
    # print(C)
    # print(x_0)
    print(f's0:{s0}')
    # print(f"newf:{newf}")
    print(f"lam:{lam}")
    # print(f'x_1:{x_1}')
    return x_1




def substitute(F, x):
    newF = [0] * 3

    newF[0] += float(F[0]) * x[0][1]**2 + float(F[1]) * x[1][1]**2 + float(F[2]) * (x[0][1] * x[1][1])
    
    newF[1] += float(F[0]) * 2 * x[0][0] * x[0][1] + float(F[1]) * 2 * x[1][0] * x[1][1] + float(F[2]) * ((x[0][0] * x[1][1]) + (x[0][1] * x[1][0]))
    newF[1] += float(F[3]) * x[0][1] + float(F[4]) * x[1][1]

    newF[2] += float(F[0]) * x[0][0]**2 + float(F[1]) * x[1][0]**2 + float(F[2]) * (x[0][0] * x[1][0])
    newF[2] += float(F[3]) * x[0][0] + float(F[4]) * x[1][0]

    return newF


def GradSimplex(dictFile, C):
    a = []
    countL = CounteLim(dictFile)
    for i in range (countL + 1):
        a.append([0] * (len(dictFile['L1']) + 2 + countL))

    for i in range(countL):
        for j in range(len(dictFile[f"L{i+1}"]) - 1):
            a[i][j+3] = int(dictFile[f"L{i+1}"][j])
        a[i][2] = int(dictFile[f"L{i+1}"][-1])
        a[i][2 + len(dictFile[f"L{i+1}"]) + i] = 1
        a[i][0] = len(dictFile[f"L{i+1}"]) + i
        a[i][1] = 0
        C.append(0)
    return a, C


def CounteLim(dictFile):
    counteX = 1
    while(True):
        if f"L{counteX}" in dictFile:        
           counteX += 1
        else:
            counteX -= 1
            break     
    return counteX

def funk_F(Fdx1, Fdx2, x0):
    x1 = Fdx1[0] * x0[0] + Fdx1[1] * x0[1] + Fdx1[2]
    x2 = Fdx2[0] * x0[0] + Fdx2[1] * x0[1] + Fdx2[2]
    return [x1, x2]

def Derivative(F, x):
    F = list(map(float, F))
    newF = [0] * 3
    if (x == 1):
        newF[0] += F[0] * 2 
        newF[1] += F[2]
        newF[2] += F[3]
    if (x == 2):
        newF[1] += F[1] * 2 
        newF[0] += F[2]
        newF[2] += F[4]
    return newF