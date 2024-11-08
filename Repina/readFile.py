def ReadAndPrepareToSimplex(path):
    return prepareToSimplex(exam(readFileSimplex(path)))





def readFileGrad(path):
    f = open(path, "r")
    dictFile = dict()
    for i in f:
        temp = i.split(':')
        dictFile[temp[0]] = temp[1].split(',')
        for j in range(len(dictFile[temp[0]])):
            if ('/' in dictFile[temp[0]][j]):
                t = dictFile[temp[0]][j].split('/')
                dictFile[temp[0]][j] = float(t[0]) / float(t[1]) #x1^2 + x2^2 + x1*x2 + x1 + x2
    return dictFile


def readFileSimplex(path):
    f = open(path, "r")
    dictFile = dict()
    for i in f:
        temp = i.split(',')
        dictFile[temp[0]] = list(map(int, temp[1::]))
    return dictFile



def CounteProd(dictFile):
    counteX = 1
    while(True):
        if f"x{counteX}" in dictFile:        
           counteX += 1
        else:
            counteX -= 1
            break     
    return counteX

def exam(dictFile):
    errors = OnTheSpot(dictFile)
    if (len(errors) == 0):
        counteRes = len(dictFile["Bi"])

        counteX = CounteProd(dictFile)
        for i in range(1, counteX + 1):
            if (counteRes != len(dictFile[f"x{i}"])):
                errors += f"len(x{i}) != len(Bi)\n"
                break
        if (len(dictFile["bi"]) != len(dictFile["Bi"])):
            errors += "len(bi) != len(Bi)\n"
        
        if (counteX != len(dictFile["ci"])):
            errors += "len(ci) != Количеству x\n"
        if (counteX != len(dictFile["BB"])):
            errors += "len(BB) != Количеству x\n"
    
    if (len(errors) != 0):
        raise Exception(errors)
    return dictFile

def OnTheSpot(dictFile):
    errors = ""
    if ("Bi" not in dictFile):
        errors += "Нету Bi(Ограничений ресурсов)\n"
    if ("bi" not in dictFile):
        errors += "Нету bi(стоимости ресурсов)\n"
    if ("ci" not in dictFile):
        errors += "Нету bi(стоимости товаров)\n"
    if ("BB" not in dictFile):
        errors += "Нету BB(плана продаж)\n"
    if ("x1" not in dictFile):
        errors += "Нету x-ов или их нумерация не начинается с 1\n"
    return errors


def prepareToSimplex(dictFile):
    a = []
    CounteX = CounteProd(dictFile)
    for i in range(len(dictFile["BB"]) + len(dictFile["Bi"])):
        a.append([0] * (3 + (CounteX  + len(dictFile["Bi"]) + len(dictFile["BB"]) * 2)))

    for i in range(CounteX):
        for j in range(len(dictFile[f"x{i+1}"])):
            a[j][i+3] = dictFile[f"x{i+1}"][j]
    
    for i in range(len(a)):
        if (i < len(dictFile["Bi"])):
            a[i][2] = dictFile["Bi"][i]
        else:
            a[i][2] = dictFile["BB"][i - len(dictFile["Bi"])]

    for i in range(len(dictFile["BB"])):
        a[i + len(dictFile["Bi"])][i + 3] = 1
        a[i + len(dictFile["Bi"])][i + 3 + CounteX + len(dictFile["Bi"])] = -1
        a[i + len(dictFile["Bi"])][i + 3 + CounteX + len(dictFile["Bi"]) + len(dictFile["BB"])] = 1

    for i in range(len(dictFile["Bi"])):
        a[i][i + 3 + CounteX] = 1

    C = [0] * (len(a[0]) - 2)
    for i in range(len(C)):
        if (i < CounteX):
            C[i] = -1 * (dictFile["ci"][i])
        elif (len(C) - i - 1 < len(dictFile["BB"])):
            C[i] = "w"
    expenses = 0
    for i in range (len(dictFile["bi"])):
        expenses += dictFile["bi"][i] * dictFile["Bi"][i]
    print(C)
    Basis = []
    for i in range(len(a)):
        if (i < len(dictFile["Bi"])):
            Basis.append(i + len(dictFile["Bi"]) + 1 + 1)
            a[i][0] = Basis[i]
            a[i][1] = C[Basis[i]]
        else:
             Basis.append(i + CounteX + len(dictFile["Bi"]) + len(dictFile["BB"]) - 1)
             a[i][0] = Basis[i]
             a[i][1] = C[Basis[i] - 1]
    a.append([0] * len(a[0]))

    masLinProg = [] 
    masLinProg.append(C[0:len(dictFile["ci"])])
    for i in range (3):
        masLinProg.append([])
    for i in range (len(dictFile["Bi"])):
        masLinProg[1].append([0] * CounteX)
        for j in range (CounteX):
            masLinProg[1][i][j] = dictFile[f"x{j+1}"][i]
        masLinProg[2].append(dictFile["Bi"][i])
    for i in range (len(dictFile["BB"])):
        masLinProg[3].append((dictFile["BB"][i], None))          

    for i in masLinProg:
        print(i)
    return a, C, expenses, masLinProg, Basis




