#!/usr/bin/python

# Copyright 2017, Gurobi Optimization, Inc.

# Solve a multi-commodity flow problem.  Two products ('Pencils' and 'Pens')
# are produced in 2 cities ('Detroit' and 'Denver') and must be sent to
# warehouses in 3 cities ('Boston', 'New York', and 'Seattle') to
# satisfy demand ('inflow[h,i]').
#
# Flows on the transportation network must respect arc capacity constraints
# ('capacity[i,j]'). The objective is to minimize the sum of the arc
# transportation costs ('cost[i,j]').

from gurobipy import *
import networkx as nx
import matplotlib.pyplot as plt
import random


def ruteo(estaciones, diccionario):
    # Model data
    m = Model('flow')
    nodes = {}
    for estacion in diccionario:
        nodes[estacion] = '{}'.format(estacion)
