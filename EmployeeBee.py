import numpy as np
from WorkerBee import WorkerBee
from ObjectiveFunctions import ObjectiveFunctions

class EmployeeBee(WorkerBee) :



    def __init__(self, objectivefunction):
        super().__init__(objectivefunction)
        


    def generate_solution(self, EmployeeBees) :
       

        partner = np.random.choice(EmployeeBees)
        while ((partner.position == self.position).any()):
            partner = np.random.choice(EmployeeBees)
        
        component = np.random.choice(self.position)          #decsition variable in current position to be modified
        index = np.where(self.position == component)[0][0]   #index of descition variable in partner position to be modified
        
        phi = np.random.uniform(-1, 1)
        
        new_position = self.position.copy()
        new_position[index] = new_position[index] + phi*(component - partner.position[index]) 
       
        
        new_position = self.check_limits(new_position)
        new_objective_value = self.evaluate(new_position)
        
        new_fitness = self.calculate_fitness(new_objective_value)
        
        self.update_worker(new_position, new_fitness)
        self.prob = self.compute_prob()
        self.objectivevalue = self.evaluate(self.position)


    def __gt__(self, other):
        return self.trial > other.trial

