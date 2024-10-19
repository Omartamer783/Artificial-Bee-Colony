import numpy as np
from ObjectiveFunctions import *
from WorkerBee import WorkerBee
from EmployeeBee import EmployeeBee

class onlookerBee(WorkerBee):

    last_food_source = 0


    """
    function :  onlook on the best fodd sources explored by Employeed bee
    arguments:  best_food_sources ==> positions of employeed bees(solutions)
    """
    
    def exploit_food_sources(self, best_food_sources):

        for i in range(len(best_food_sources)):
            r = np.random.uniform(0, 1)
            
            if r < best_food_sources[(i + onlookerBee.last_food_source) % len(best_food_sources)].compute_prob():

                self.position = best_food_sources[i].position.copy()
                self.objectivevalue = self.evaluate(self.position)
                self.fitness = self.calculate_fitness(self.objectivevalue)
                self.trial = best_food_sources[i].trial


                partner = np.random.choice(best_food_sources)
                
                while ((partner.position == self.position).any()):
                    partner = np.random.choice(best_food_sources)
        
                component = np.random.choice(self.position) 
                index = np.where(self.position == component)[0][0]   #index of descition variable in partner position to be modified
        
                phi = np.random.uniform(-1, 1)
        
                new_position = self.position.copy()
                new_position[index] = new_position[index] + phi*(component - partner.position[index]) 
                
        
                new_position =  best_food_sources[i].check_limits(new_position)
                new_objective_value = best_food_sources[i].evaluate(new_position)
        
                new_fitness =  best_food_sources[i].calculate_fitness(new_objective_value)
        
                best_food_sources[i].update_worker(new_position, new_fitness)
                best_food_sources[i].objectivevalue = best_food_sources[i].evaluate(best_food_sources[i].position)
                best_food_sources[i].prob = best_food_sources[i].compute_prob()
                

                onlookerBee.last_food_source += 1
                break

            else:
                onlookerBee.last_food_source += 1








