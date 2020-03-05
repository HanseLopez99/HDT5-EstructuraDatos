#Hoja de Trabajo # 5
#Hansel Andre Lopez Montenegro
#19026

import simpy
import random
import math
import matplotlib.pyplot as plt

lista = []

def main():
    env = simpy.Environment()
    RANDOM_SEED = 40
    random.seed(RANDOM_SEED)
    processor = simpy.Resource(env, capacity=2)
    RAM = simpy.Container(env, init=100, capacity=100)
    totalProcesses = 25
    creationInterval = 10.0
    memory = 0 
    numberOfInstructions = 0
    env.process(source(env, totalProcesses, creationInterval, processor, RAM))
    env.run()
    media = promedio(lista)
    print("")
    print("La media es: ")
    print(media)
    print("")
    desvest = desviacionStandar(lista, media)
    print("La desviacion estandar es: ")
    print(desvest)
    print("")
    print("-Simulation Complete!")
    desplegarGrafica(lista)

def appendLista(elemento):
    lista.append(elemento)

def desplegarGrafica(lista):
    plt.plot(lista)
    plt.title("Grafica Tiempo/Procesos")
    plt.xlabel("Processes")
    plt.ylabel("Time(Units of time)")
    plt.show()

def promedio(lista):  
    sumatoria = 0
    for numero in lista:
        sumatoria+=numero #Esta parte suma todos los elementos de la lista
        
    cantidad = len(lista) #Esta parte cuenta los elementos de la lista
    
    resultado = sumatoria/float(cantidad) #Eta parte aplica la formula de promedio
    resultado = round(resultado, 3)
    return (resultado)

def desviacionStandar(lista,media):
    lista2 = []
    sumatoria = 0
    n = len(lista)
    for numero in lista:
        parentesis = numero-media
        elemento = parentesis*parentesis
        lista2.append(elemento)
        numero = numero+1
    cantidad = len(lista)-1
    for i in lista2:
        sumatoria = sumatoria + i
    division = sumatoria/n
    resultado = math.sqrt(division)
    resultado = round(resultado,3)
    return resultado
    
def source(env, totalProcesses, interval, processor, ram):
    for n in range(totalProcesses):
        memory = random.randint(1,10)  
        numberOfInstructions = random.randint(1,10)
        ram.get(memory)
        proc = processorSimulation(env, 'Process%02d status' % n, processor, totalProcesses, processorCapacity=1.0)
        ram.put(memory)
        env.process(proc)
        time = random.expovariate(1.0 / interval)
        yield env.timeout(time)   

def processorSimulation(env, name, processor, totalProcesses, processorCapacity):
    
    arrive = env.now
    print('%7.2f %s: Ready to start' % (arrive, name))

    with processor.request() as req:
        patience = random.uniform(1, 3)
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            print('%7.2f %s: Waited  %6.2f' % (env.now, name, wait))
            time = random.expovariate(1.0 / processorCapacity)
            yield env.timeout(time)
            print('%7.2f %s: Finished' % (env.now, name)) 
            appendLista(env.now)         
        else:
            print('%7.4f %s: RENEGED after %6.2f' % (env.now, name, wait))



if __name__ == '__main__':
    main()