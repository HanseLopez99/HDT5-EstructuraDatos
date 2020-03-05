#Hoja de Trabajo # 5
#Hansel Andre Lopez Montenegro
#19026

import simpy
import random

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
    print("-Simulation Complete!")
    
def source(env, number, interval, processor, ram):
    for n in range(number):
        memory = random.randint(1,10)  
        numberOfInstructions = random.randint(1,10)
        ram.get(memory)
        proc = processorSimulation(env, 'Process%02d status' % n, processor, processorCapacity=1.0)
        ram.put(memory)
        env.process(proc)
        time = random.expovariate(1.0 / interval)
        yield env.timeout(time)   

def processorSimulation(env, name, processor, processorCapacity):
    
    arrive = env.now
    print('%7.2f %s: Starting process...' % (arrive, name))

    with processor.request() as req:
        patience = random.uniform(1, 3)
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            print('%7.2f %s: Waited  %6.2f' % (env.now, name, wait))
            time = random.expovariate(1.0 / processorCapacity)
            yield env.timeout(time)
            print('%7.2f %s: Finished' % (env.now, name))           
        else:
            print('%7.4f %s: RENEGED after %6.2f' % (env.now, name, wait))

if __name__ == '__main__':
    main()