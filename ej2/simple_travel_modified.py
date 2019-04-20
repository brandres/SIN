"""
The "travel from home to the park" example from Dana Nau lectures.
Author: Dana Nau <nau@cs.umd.edu>, May 31, 2013
This file should work correctly in both Python 2.7 and Python 3.2.

Modified: Antonio Garrido
Version with a single goal
"""


# Funcion auxiliar

def taxi_rate(dist):
    return (1.5 + 0.5 * dist)


# Operadores: devuelven el estado (si las conds se cumplen) o False (si las conds no se cumplen)
# Importante: los operadores NO se pueden descomponer

def walk(state, a, x, y):
    if state.loc[a] == x:
        state.loc[a] = y
        return state
    else:
        return False


def call_taxi(state, a, x):
    if state.wants_taxi[a]:
        state.phoned_times[a] += 1
        state.loc['taxi'] = x
        return state
    else:
        return False


def wait_taxi(state, a):
    state.waiting_time[a] += 10
    return state


def read_book(state, a):
    state.read_book[a] = True
    return state


def ride_taxi(state, a, x, y):
    if state.loc['taxi'] == x and state.loc[a] == x:
        state.loc['taxi'] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        return state
    else:
        return False


def pay_driver(state, a):
    if state.cash[a] >= state.owe[a]:
        state.cash[a] = state.cash[a] - state.owe[a]
        state.owe[a] = 0
        return state
    else:
        return False


# Declaracion de los operadores. NO BASTA con definirlos con "def" sino que 
# tambien hay que indicarselo a pyhop.
# Importante: se deben declarar TODOS los operadores en un UNICO "declare_operators"

pyhop.declare_operators(walk, call_taxi, wait_taxi, read_book, ride_taxi, pay_driver)

print('')
pyhop.print_operators()


# Definición de dos metodos para "read_if_necessary_book". Solo uno de ellos se ejecutara
# como maximo. Deben devolver un conjunto de operadores/tareas (aunque sea vacio) o False
# si no se puede aplicar

def do_read(state, a, x, y):
    if not state.read_book[a]:
        return [('read_book', a)]
    return False


def dont_read(state, a, x, y):
    if state.read_book[a]:
        return []
    return False


# Indicamos cual es la descomposicion de "read_if_necessary_book"

pyhop.declare_methods('read_if_necessary_book', do_read, dont_read)


# Definicion de dos metodos para "travel". Solo uno de ellos se ejecutara como maximo

def travel_by_foot(state, a, x, y):
    if state.dist[x][y] <= 2:
        return [('walk', a, x, y)]
    return False


def travel_by_taxi(state, a, x, y):
    if state.cash[a] >= taxi_rate(state.dist[x][y]):
        return [('call_taxi', a, x), ('wait_taxi', a), ('read_if_necessary_book', a, x, y), ('ride_taxi', a, x, y),
                ('pay_driver', a)]
    return False


# Indicamos cual es la descomposicion de "travel"

pyhop.declare_methods('travel', travel_by_foot, travel_by_taxi)
print('')
pyhop.print_methods()

# Definicion del estado

state1 = pyhop.State('state1')
state1.loc = {'me': 'home'}  # the location of "me"
state1.cash = {'me': 20}  # the money "me" has
state1.owe = {'me': 0}  # the money "me" owes
state1.dist = {'home': {'park': 8}, 'park': {'home': 8}}  # distribution of distances
state1.phoned_times = {'me': 0}  # how many times "me" has phoned
state1.wants_taxi = {'me': True}  # does "me" want a taxi?
state1.waiting_time = {'me': 0}  # waiting time for a taxi of "me"
state1.read_book = {'me': False}  # has "me" read the book?

print("""
********************************************************************************
Call pyhop.pyhop(state1,[('travel','me','home','park')]) with different verbosity levels
********************************************************************************
""")

# Buscamos un plan a partir de un estado inicial para que "me" viaje de "home" a "park"

pyhop.pyhop(state1, [('travel', 'me', 'home', 'park')], verbose=1)

"""
Importante para depurar:

Necesitamos: import pdb

Ponemos la instruccion "pdb.set_trace()" donde queramos en nuestro codigo y se detendra la ejecucion
Luego simplemente escribimos la letra 'n' desde el shell que ejecutara la siguiente sentencia y podemos ir
viendo el valor de las variables
"""
