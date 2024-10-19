import numpy as np 


      


class ObjectiveFunctions :
    
    name = None
   
    def __init__(self, dimension, lower_bound, upper_bound) :
        self.dimension =  dimension
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    

    def random_sample(self) :
           return np.random.uniform(low=self.lower_bound, high=self.upper_bound, size=self.dimension)

    def objective_value(self, arr) :
           pass
    


class Ackley_function (ObjectiveFunctions):
      name = "Ackley_function"
      color = 'blue'
      def objective_value(self, arr) :
            arr_np = np.array(arr)
            n = len(arr_np)
            a = 20
            b = 0.2
            c = 2 * np.pi
            term1 = -a * np.exp(-b * np.sqrt(np.sum(arr_np**2) / n))
            term2 = -np.exp(np.sum(np.cos(c * arr_np)) / n)
            return term1 + term2 + a + np.e
          
class  Sphere_function (ObjectiveFunctions) :
        
        name = "Shpere"
        color = 'black'
        def objective_value(self, arr) :
               arr_np = np.array(arr)
               return np.sum(arr_np**2)


class bukin_function_n6(ObjectiveFunctions):
           name = "bukin_function_n6"
           color = 'green'
           def objective_value(self, arr):
                arr_np = np.array(arr)
                x1, x2 = arr_np
                return 100 * np.sqrt(np.abs(x2 - 0.01 * x1**2)) + 0.01 * np.abs(x1 + 10)
           
class rastrigin_function(ObjectiveFunctions):
             color = 'red'
             name = "rastrigin_function"
             def objective_value(self, arr):
                      arr_np = np.array(arr)
                      n = len(arr_np)
                      return 10 * n + np.sum(arr_np**2 - 10 * np.cos(2 * np.pi * arr_np))