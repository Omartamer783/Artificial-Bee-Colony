from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import numpy as np
from ObjectiveFunctions import *
from WorkerBee import WorkerBee
from main import ABC
from EmployeeBee import EmployeeBee
from OnlookerBee import onlookerBee
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


root = Tk()
root.title("Artificial Bee Colony Algorithm")


def get_inputs_objevtive():
        global function_object
        selected_function = function_var.get()
        if selected_function == "Ackkley function":
                function_object = Ackley_function(int(entry_dimension.get()),float( entry_lower_bound.get()),float( entry_upper_bound.get()))
        if selected_function == "rastrigin_function":
                function_object = rastrigin_function(int(entry_dimension.get()), float(entry_lower_bound.get()), float(entry_upper_bound.get())) 
        if selected_function ==  "sphere function":
                function_object = Sphere_function(int(entry_dimension.get()), float(entry_lower_bound.get()),float( entry_upper_bound.get())) 
        
        print(function_object.dimension)

def create_ABC():
        global evolution
        np.random.seed(int(entry_seed_number.get()))
        evolution = ABC(function_object,int(entry_colony_size.get()),int( entry_no_generation.get()),int( entry_onlooker_limit.get()) )
        evolution.initialize_employees()
        evolution.initialize_onlookers()
        create_plot()
        print(evolution.employee_bees[0].position)

def create_plot():
    global fig, ax_3d, surface, employee_points, ani
    
    x = np.linspace(-5.12, 5.12, 50)
    y = np.linspace(-5.12, 5.12, 50)
    X, Y = np.meshgrid(x, y)

    # Calculate the objective values
    Z = np.apply_along_axis(function_object.objective_value, axis=1, arr=np.column_stack((X.ravel(), Y.ravel())))
    Z = Z.reshape(X.shape)
    
    # Create a Figure and Axes for the plots
    fig = plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    ax_3d = fig.add_subplot(121, projection='3d')  # Subplot for 3D plot
    ax_contour = fig.add_subplot(122)  # Subplot for contour plot

    # Plot the initial surface in 3D plot
    surface = ax_3d.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis')

    

    # Plot the initial employee points in 3D plot
    employee_points, = ax_3d.plot([], [], [], 'ro', markersize=10)

    # Plot the contour lines
    contour = ax_contour.contour(X, Y, Z, cmap='viridis')

    # Plot the initial employee points on the contour plot
    employee_points_contour, = ax_contour.plot([], [], 'ro', markersize=5)

    # Function to update the plots for each animation frame
    # Function to update the plots for each animation frame

    # Add text annotation to display iteration number and optimal solution
  
    def update(frame):
        ax_3d.clear()  # Clear the existing 3D plot
        ax_contour.clear()  # Clear the existing contour plot

        # Plot the surface in 3D plot
        surface = ax_3d.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis')

        # Plot the employee points in 3D plot
        for obj in evolution.employee_bees:
                color = 'yellow' if obj.trial > evolution.limit else 'red'
                ax_3d.scatter(obj.position[0], obj.position[1], obj.objectivevalue, color=color, s=50)

        # Update the data for employee_points in 3D plot
        employee_points.set_data([obj.position[0] for obj in evolution.employee_bees], [obj.position[1] for obj in evolution.employee_bees])
        employee_points.set_3d_properties([obj.objectivevalue for obj in evolution.employee_bees])

        # Plot the contour lines
        contour = ax_contour.contour(X, Y, Z, cmap='viridis')

        # Plot the employee points on the contour plot
        for obj in evolution.employee_bees:
                color = 'yellow' if obj.trial > evolution.limit else 'red'
                ax_contour.scatter(obj.position[0], obj.position[1], color=color, s=5)
        ax_contour.scatter(evolution.optimal_solution.position[0], evolution.optimal_solution.position[1], color = "blue")
        # Update the data for employee_points_contour in the contour plot
        employee_points_contour.set_data([obj.position[0] for obj in evolution.employee_bees], [obj.position[1] for obj in evolution.employee_bees])

        evolution.employee_bees_phase()
        evolution.onlooker_bees_phase()
        evolution.check_scout_phase()
        evolution.update_optimal_solution()
        label_results.config(text=f"Iteration: {frame}, Optimal Solution: {evolution.optimal_solution.position}, Objective Value: {evolution.optimal_solution.objectivevalue}")

        print(f"Iteration: {frame}, Optimal Solution: {evolution.optimal_solution.position}, Objective Value: {evolution.optimal_solution.objectivevalue}")


    # Create the animation
    ani = FuncAnimation(fig, update, frames=evolution.n_iter, interval=100)

    # Create a canvas to embed the plots in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # Add a toolbar (optional)
    toolbar_frame = ttk.Frame(root)
    toolbar_frame.pack(side=BOTTOM, fill=X)

    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()



#objective function and its inputs
objective_frame = ttk.LabelFrame(root, text="Objective Function" )
objective_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
functions = ["Ackkley function", "rastrigin_function", "sphere function"]
function_var = StringVar()
function_combobox = ttk.Combobox(objective_frame, textvariable=function_var, values=functions)
label_functions = Label(objective_frame, text= "function name")
label_functions.grid(row=0 , column= 0)
function_combobox.grid(row=0, column = 1)
label_dimension = Label(objective_frame, text= "dimension")
entry_dimension = Entry(objective_frame)
label_lower_bound = Label(objective_frame, text= "lower bound")
entry_lower_bound = Entry(objective_frame)
label_upper_bound = Label(objective_frame, text= "upper bound")
entry_upper_bound = Entry(objective_frame)
label_dimension.grid(row=1 , column=0)
entry_dimension.grid(row=1, column=1)
label_lower_bound.grid(row=2 , column= 0)
entry_lower_bound.grid(row=2 , column=1)
label_upper_bound.grid(row=3 , column=0)
entry_upper_bound.grid(row=3 , column=1)
objective_button = Button(objective_frame, text="Get Inputs", command=get_inputs_objevtive)
objective_button.grid(row=4, column=1, padx=20, pady=10)


# parameters of the algorithm 
algo_frame = ttk.LabelFrame(root, text="parameters" )
algo_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
label_colony_size = Label(algo_frame, text= "colony size")
entry_colony_size = Entry(algo_frame)
label_no_generation = Label(algo_frame, text= "generations number")
entry_no_generation = Entry(algo_frame)
label_onlooker_limit = Label(algo_frame, text= "onlooker_limit")
entry_onlooker_limit = Entry(algo_frame)
label_seed_number = Label(algo_frame, text= "seed_number")
entry_seed_number = Entry(algo_frame)
label_colony_size.grid(row=0, column=0)
entry_colony_size.grid(row=0 , column=1)
label_no_generation.grid(row=1 , column=0)
entry_no_generation.grid(row=1, column=1)
label_onlooker_limit.grid(row=2, column=0)
entry_onlooker_limit.grid(row=2, column=1)
label_seed_number.grid(row=3 , column=0)
entry_seed_number.grid(row=3, column=1)
run_button = Button(algo_frame, text="run" , command=create_ABC)
run_button.grid(row=4, column=1, padx=20, pady=10)

#plot 1 frame 
plot_frame = ttk.LabelFrame(root, text="visualizing the function")
plot_frame.grid(row=0 , column=1)
results_frame = ttk.LabelFrame(root, text="result")
results_frame.grid(row=1, column= 1)

label_results = Label(results_frame, text =" ")
label_results.pack()


root.mainloop()









