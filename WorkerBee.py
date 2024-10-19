import numpy as np
from ObjectiveFunctions import ObjectiveFunctions

class WorkerBee :

    max_fitness = -1


    
    def __init__(self, objectivefunction):
        self.objectivefunction = objectivefunction 
        self.lower_bound = objectivefunction.lower_bound
        self.upper_bound = objectivefunction.upper_bound
        self.position = objectivefunction.random_sample()
        self.objectivevalue = objectivefunction.objective_value(self.position)
        self.trial = 0
        self.fitness = self.calculate_fitness(self.objectivevalue)
        self.checkMax_fitness()
        self.prob = 0.0
        

    def checkMax_fitness(self):
        if self.fitness > WorkerBee.max_fitness:
            WorkerBee.max_fitness = self.fitness


    def check_limits(self , position) :
        if (position < self.lower_bound).any() or (position > self.upper_bound).any():
            position[position > self.upper_bound] = self.upper_bound
            position[position < self.lower_bound] = self.lower_bound
        return position 
    
    
    def calculate_fitness(self , objectivevalue) :
        if objectivevalue >= 0 :
           fitness= 1/(1+objectivevalue)
        else :
            fitness = abs(objectivevalue) + 1

        return fitness    

    def update_worker(self , new_position , new_fitness ) :
       

        if new_fitness > self.fitness :
            self.position = new_position.copy()
           
            self.fitness = new_fitness
            self.trial = 0
            self.checkMax_fitness()

        else :
            self.trial +=1
      

    def evaluate(self, arr) :
         return self.objectivefunction.objective_value(arr)

    def compute_prob(self):
        return  (0.9 * (self.fitness / WorkerBee.max_fitness) + 0.1)

    



        