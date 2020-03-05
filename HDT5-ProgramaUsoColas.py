#Hoja de Trabajo # 5
#Hansel Andre Lopez Montenegro
#19026

import simpy
import random

def main():
    env = simpy.Environment()
    RANDOM_SEED = 40
    random.seed(RANDOM_SEED)
    processor = simpy.Resource(env, capacity=3)
    RAM = simpy.Container(env, init=100, capacity=100)
    totalProcesses = 25
    creationInterval = 10.0


    
    env.process(source(env, totalProcesses, creationInterval, processor))
    env.run()
    print("-Simulation Complete!")
    
def source(env, number, interval, processor):
    for n in range(number):

        proc = processorSimulation(env, 'Process%02d' % n, processor, processorCapacity=3.0)
        env.process(proc)
        time = random.expovariate(1.0 / interval)
        yield env.timeout(time)   

def processorSimulation(env, name, processor, processorCapacity):
    
    arrive = env.now
    print('%7.2f %s: Starting process...' % (arrive, name))

    with processor.request() as req:
        patience = random.uniform(1, 3)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.2f %s: Waited %6.2f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / processorCapacity)
            yield env.timeout(tib)
            print('%7.2f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.2f' % (env.now, name, wait))

        

if __name__ == '__main__':
    main()