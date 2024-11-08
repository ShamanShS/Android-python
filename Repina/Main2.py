import grad
import readFile
import math

def Fx (F, x):
    return float(F[0]) * x[0]**2 + float(F[1]) * x[1]**2 + float(F[2]) * x[0] * x[1] + float(F[3]) * x[0] + float(F[4]) * x[1]



t = readFile.readFileGrad('grad.txt')
eps = 0.000001
x1 = [1.5,1.5]
Fx1 = Fx(t['F'], x1)
x0 = grad.Grad(t, x1)
Fx0 = Fx(t['F'], x0)
iter = 0
print(f'Итерация {iter} \nx0 = {x0}')
# print(math.sqrt(abs(x1[0] - x0[0])**2 + abs(x1[1] - x0[1])**2))
while (math.sqrt(abs(x1[0] - x0[0])**2 + abs(x1[1] - x0[1])**2) > eps):
    
    print("----------------------------------------------({})\n")
    iter += 1
    x1 = x0
    Fx1 = Fx0
    x0 = grad.Grad(t, x1)
    Fx0 = Fx(t['F'], x0)
    print(f'Итерация {iter}\n x0 = {x0}, F(x0) = {Fx0}')
    print(math.sqrt(abs(x1[0] - x0[0])**2 + abs(x1[0] - x0[0])**2))

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
 
# defining surface and axes
X = np.linspace(0, 2, 100)
Y = X.copy().T

x, y = np.meshgrid(X, Y)

z = np.cos(x ** 2 + 2/3 * y ** 2 - 0.5 * x * y - 5.5 * x + 1/6 * y)
 
fig = plt.figure()
 
# syntax for 3-D plotting
ax = plt.axes(projection='3d')
 
# syntax for plotting
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_title('Surface plot geeks for geeks')
plt.show()