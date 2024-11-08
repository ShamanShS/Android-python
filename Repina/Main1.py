import readFile 
import Simplex
import scipy.optimize

def linprog(L):
    res = scipy.optimize.linprog(L[0], A_ub = L[1], b_ub= L[2], bounds=L[3])
    print(res)


path = "plan.txt"

a, C, expenses, masLinProg, Basis = readFile.ReadAndPrepareToSimplex(path)

a = Simplex.Simplex(a, C)
Simplex.print_res(a, expenses)
linprog(masLinProg)

# pr = a[-1][2]
# newLimit = [200, 1499, 10, 10, 10]
# a1 = a
# flag = True
# # Simplex.Analysis2(a, C, newLimit, Basis)
# while(flag):
    
#     print(newLimit)
#     masLinProg[2] = newLimit[0:2]
#     for i in range (len(masLinProg[3])):
#         masLinProg[3][i] = (newLimit[i + 2], None)
#     # linprog(masLinProg)
#     if Simplex.Analysis2(a, C, newLimit, Basis) != -1:
#         if abs(pr) > abs(a[-1][2]):
#             # print(newLimit)
#             Simplex.print_res(a, expenses)
#             flag = False
#     a = a1
#     newLimit[1] -= 1

linprog(masLinProg)