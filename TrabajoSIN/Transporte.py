from lib import pyhop


def cambiar_camion(estado, a, b):
    estado.aparcados.add(estado.conduce[a])
    estado.conduce[a] = b


def aparcar_camion(estado, a):
    estado.aparcados.add(estado.conduce[a])
    estado.conduce[a] = ''


def precio_autobus(x):
    return x * 1.21


def get_camion(estado, b, x):
    for a in estado.posicion.keys():
        if estado.posicion[a] == x and 'T' in a and estado.conduce[b] != a and a not in estado.aparcados:
            return a
    return 'null'


def camion_cercano(estado, a, x):
    for y in estado.conexion[x].keys():
        if get_camion(estado, a, y) != 'null':
            return y
    return 'null'


def paquete_cercano(estado, x):
    for y in estado.conexion[x].keys():
        if get_carga_no_gestionada(estado, y) != 'null':
            return y
    return 'null'


def camion_ocupado(estado, b):
    for c in estado.conduce.keys():
        if estado.conduce[c] == b:
            return True
    return False


def get_carga_no_gestionada(estado, x):
    for a in estado.posicion.keys():
        if estado.posicion[a] == x and 'P' in a and not carga_gestionada(estado, a):
            return a
    return 'null'


def carga_gestionada(estado, c):
    if c in estado.entregados:
        return True
    else:
        for x in estado.carga.keys():
            if c in estado.carga[x]:
                return True
    return False


def caminar(estado, a, x, y):
    if estado.posicion[a] == x:
        estado.posicion[a] = y
        estado.conduce[a] = ''
        return estado
    else:
        return False


def conducir_camion(estado, a, b, x, y):
    if estado.posicion[a] == x and estado.posicion[b] == x:
        estado.posicion[a] = y
        estado.posicion[b] = y
        estado.conduce[a] = b
        for key in estado.carga[b]:
            estado.posicion[key] = y
        return estado
    else:
        return False


def ir_en_autobus(estado, a, x, y):
    if estado.posicion['autobus'] == x and estado.posicion[a] == x:
        estado.dinero[a] -= precio_autobus(1)
        estado.posicion['autobus'] = y
        estado.posicion[a] = y
        return estado
    else:
        return False


def esperar_autobus(estado, a):
    estado.tiempo_esperando[a] += 10
    return estado


def cargar_camion(estado, a, b, c):
    if estado.posicion[a] == estado.posicion[b] == estado.posicion[c]:
        estado.carga[b].add(c)
        estado.conduce[a] = b
        return estado
    else:
        return False


def descargar_camion(estado, a, b, c):
    if estado.posicion[a] == estado.posicion[b] == estado.posicion[c]:
        estado.entregados.add(c)
        estado.carga[b].remove(c)
        return estado
    else:
        return False


pyhop.declare_operators(caminar, conducir_camion, ir_en_autobus, esperar_autobus, cargar_camion, descargar_camion)
print('')
pyhop.print_operators()


def realizar_carga(estado, a, b, x, y):
    pos = estado.posicion[a]
    c = get_carga_no_gestionada(estado, pos)
    if c != 'null' and c not in estado.carga[b] and 'D' in a and 'T' in b and c not in estado.entregados:
        return [('cargar_camion', a, b, c)]
    return False


def realizar_descarga(estado, a, b, x, y):
    pos = estado.posicion[a]
    for c in estado.carga[b]:
        if c in estado.carga[b] and 'D' in a and 'T' in b and pos == y:
            return [('descargar_camion', a, b, c)]
    return False


def reparto(estado, a, b, x, y):
    if estado.conexion[x][y] == 'carretera':
        return [('conducir_camion', a, b, x, y)]
    else:
        return False


pyhop.declare_methods('gestionar_camion', realizar_carga, realizar_descarga, reparto)


def moverse_a_pie(estado, a, x, y):
    if estado.conexion[x][y] == 'senda' and 'D' in a:
        return [('caminar', a, x, y)]
    return False


def moverse_en_camion(estado, a, x, y):
    pos = estado.posicion[a]
    b = estado.conduce[a] if estado.conduce[a] != '' else get_camion(estado, a, pos)
    print(b)
    if 'D' in a and 'T' in b:
        return [('gestionar_camion', a, b, x, y)]
    return False


def moverse_en_autobus(estado, a, x, y):
    if 'D' in a and precio_autobus(1) <= estado.dinero[a] and estado.conexion[x][y] == 'senda':
        return [('ir_en_autobus', a, x, y), ('esperar_autobus', a)]
    return False


pyhop.declare_methods('moverse', moverse_en_camion, moverse_a_pie, moverse_en_autobus)


def hay_paquetes(meta):
    for a in meta.posicion.keys():
        if 'P' in a:
            return meta.posicion[a]
    return ''


def realizar_transporte(estado, meta):
    if len(meta.posicion) > 0:
        for a in meta.posicion.keys():
            if 'D' in a:
                x = estado.posicion[a]
                if get_camion(estado, a, x) == 'null' and estado.conduce[a] == '':
                    y = camion_cercano(estado, a, x)
                else:
                    if get_carga_no_gestionada(estado, x) != 'null':
                        y = meta.posicion[get_carga_no_gestionada(estado, x)]
                    else:
                        if paquete_cercano(estado, x) != 'null':
                            y = paquete_cercano(estado, x)
                        else:
                            if estado.conduce[a] != '' and len(estado.carga[estado.conduce[a]]) > 0:
                                c = next(iter(estado.carga[estado.conduce[a]]))
                                y = meta.posicion[c]
                            else:
                                if estado.conduce[a] in meta.posicion:
                                    if estado.conduce[a] not in estado.aparcados:
                                        y = meta.posicion[estado.conduce[a]]
                                        aparcar_camion(estado, a)
                                    else:
                                        y = meta.posicion[a]
                                else:
                                    if get_camion(estado, a, x) != 'null':
                                        cambiar_camion(estado, a, get_camion(estado, a, x))
                                        y = meta.posicion[estado.conduce[a]]
                                    else:
                                        y = camion_cercano(estado, a, x)
                if get_carga_no_gestionada(estado, x) != 'null' or camion_cercano(estado, a,
                                                                                  x) != 'null' or x != y or \
                        estado.conduce[a] != '':
                    return [('moverse', a, x, y), ('realizar_transporte', meta)]
    return []


pyhop.declare_methods('realizar_transporte', realizar_transporte)
print('')
pyhop.print_methods()

estado1 = pyhop.State('estado1')
estado1.conexion = {'C0': {'P_01': "senda", 'C1': "carretera", 'C2': "carretera"},
                    'C1': {'C0': "carretera", 'P_12': "senda", 'C2': "carretera", 'P01': "senda"},
                    'C2': {'C0': "carretera", 'C1': "carretera", 'P_12': "sendero"},
                    'P_01': {'C0': "senda", 'C1': "senda"},
                    'P_12': {'C1': "senda", 'C2': "senda"}}
estado1.posicion = {'T2': 'C0', 'P1': 'C0', 'P2': 'C0', 'D1': 'P_01', 'D2': 'C1', 'T1': 'C1'}
estado1.carga = {'T1': set(), 'T2': set()}
estado1.tiempo_esperando = {'D1': 0, 'D2': 0}
estado1.dinero = {'D1': 0, 'D2': 2}
estado1.conduce = {'D1': '', 'D2': ''}
estado1.entregados = set()
estado1.aparcados = set()

meta1 = pyhop.Goal('meta1')
meta1.posicion = {'D1': 'C0', 'T1': 'C0', 'P1': 'C2', 'P2': 'C1'}

pyhop.pyhop(estado1, [('realizar_transporte', meta1)], verbose=3)
