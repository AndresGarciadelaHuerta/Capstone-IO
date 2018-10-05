# modelo de ruteo

from gurobipy import *

m = Model('Modelo_ruteo')

# model.addvariables

# tamaño zona
t = 3

# costos
c = [[0,4,5],[1,0,3],[1,2,0]]

#diferencias
b = [3,-4,1]

# capacidad camiones
q = 80



# crear variables
y = []
x = []
for i in range(3):
    e = []
    r = []
    for j in range(3):
        e.append(m.addVar(vtype=GRB.BINARY, name= 'y_{}_{}'.format(i,j)))
        r.append(m.addVar(vtype=GRB.INTEGER, name= 'x_{}_{}'.format(i,j)))
    y.append(e)
    x.append(r)

m.update()

# F.O
m.setObjective(quicksum(c[i][j] * y[i][j] for i in range(t) for j in range(
    t)), GRB.MINIMIZE)

# restricciones
for j in range(t):
    m.addConstr(quicksum(x[i][j] for i in range(t)) - quicksum(x[j][k] for k
            in range(t)), GRB.EQUAL, b[j], 'c0')

for i in range(t):
    for j in range(t):
        m.addConstr(x[i][j], GRB.LESS_EQUAL, q * y[i][j], 'c2')

for j in range(t):
            m.addConstr(quicksum(y[i][j] for i in range(t)) - quicksum(y[j][
                k] for k in range(t)), GRB.EQUAL, 0, 'c3')

for i in range(t):
    for j in range(t):
        m.addConstr(x[i][j], GRB.GREATER_EQUAL, 0, 'c4')



# resolver
m.optimize()

for v in m.getVars():
    print(v.varName, v.x)






