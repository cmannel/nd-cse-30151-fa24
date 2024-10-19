import csv
import time
import matplotlib.pyplot as plt
import numpy as np

SAT = "SAT"
UNSAT = "UNSAT"

def unit_propagation(clauses, assignments):
  # assign values for unit literals
  unit_clauses = find_unit_clauses(clauses, assignments) 

  # choosing units means will evaluate to true
  if unit_clauses: 
    for unit in unit_clauses:
      
      # T inside clause, remove clause
      for clause in clauses:
        if unit in clause: 
          clauses.remove(clause)
         
      # F inside clause, remove unit
      for clause in clauses:
        if -unit in clause: 
            clause.remove(-unit)
  
def find_unit_clauses(clauses, assignments):
  # picking units, then assign values
  unit_clauses = [clause[0] for clause in clauses if len(clause) == 1] 
  
  for unit in unit_clauses:
    literal = unit
    
    if literal > 0:
      assignments[literal] = True
    else:
      assignments[-literal] = False

  return unit_clauses

def propagate_pure(clauses, pure_literals, assignments):
  # assign pure values
  for pure in pure_literals:
    assignments[abs(pure)] = True if pure > 0 else False 
    
    # remove pure literals
    for clause in clauses:
      clause = [literal for literal in clause if literal not in pure_literals] 
  
def find_pure_literals(clauses):
  literal_count = {}
  for clause in clauses:
    for literal in clause:
      if literal in literal_count:
        literal_count[literal] += 1
      else:
        literal_count[literal] = 1

  # choose pure literals
  pure_literals = [literal for literal, count in literal_count.items() if -(literal) not in literal_count] 
  return pure_literals

def select_unassigned_variables(assignments):
  # choose unassigned variables
  unassigned_variable = [variable for variable, assignment in assignments.items() if assignment == None] 
  return unassigned_variable 

def DPLL(clauses, assignments):

  # keep unit proping while there are units
  while any(len(clause) == 1 for clause in clauses): 
    unit_propagation(clauses, assignments)

  # further simplify by removing pure literals
  pure_literals = find_pure_literals(clauses) 
  propagate_pure(clauses, pure_literals, assignments) 

  # base cases 
  if clauses == []: # SAT case
    return SAT, assignments 
    
  if any(len(clause) == 0 for clause in clauses): # UNSAT case
    return UNSAT, None

  # continue assigning by recursing through DPLL on next unassigned
  unassigned_literals = select_unassigned_variables(assignments) 
  if unassigned_literals != []:
    literal = unassigned_literals[0]
    return DPLL(clauses + [[literal]], assignments) if DPLL(clauses + [[literal]], assignments) == SAT else DPLL(clauses + [[-literal]], assignments)

  return SAT, assignments

def document(problem_number, data): 
  # output problem details to file
  status, run_time, num_literals = data
  
  with open('output.txt', 'a') as file:
    file.write(f'Problem {problem_number}: {status} \n  run time: {run_time}\n  num literals: {num_literals}\n')

def update_axes(x_sat, y_sat, x_unsat, y_unsat, data): 
  # append new data to graph axes 
  status, run_time, num_literals = data
  
  if status == SAT:
    x_sat.append(num_literals)
    y_sat.append(run_time)
  else:
    x_unsat.append(num_literals)
    y_unsat.append(run_time)
    
def graph(x, y, status):  # create and show graphs, save to pngs
  # Plotting the dots
  x = np.array(x)
  y = np.array(y)

  # Plotting the dots
  plt.scatter(x, y, color='blue', label='Data Points')

  # Fitting an exponential trendline
  log_y = np.log(y)
  coefficients = np.polyfit(x, log_y, 1)  # Linear fit to log-transformed data
  a = np.exp(coefficients[1])
  b = coefficients[0]

  def exponential_func(x):
      return a * np.exp(b * x)

  # Plotting the exponential trendline
  plt.plot(x, exponential_func(x), color='red', label='Exponential Trendline')

  # Adding titles and labels
  plt.title(f'{status} Plot')
  plt.xlabel('Number of Literals')
  plt.ylabel('Run Time')
  plt.legend()

  # Save the plot to a file
  plt.savefig(f'{status}_plot.png')

  # Display the plot
  plt.show()

def main():
  
  file_name = input("Enter file name: ")
  try:
    with open(file_name, mode ='r') as file:
      csvFile = csv.reader(file)
      
      # Init values
      x_sat, y_sat = [], []
      x_unsat, y_unsat = [], []

      clauses = []
      assignments = {}
      
      problem_number = 0
      k = 0
      num_clauses = 0
      count = 0

      for lines in csvFile: 
          
          # Init new problem
          if lines[0] == 'c':
            print(f"Problem {problem_number}:", end=' ')
            problem_number += 1
            count = 0
            clauses = []
            assignments = {}
            
          # Info of problem
          elif lines[0] == 'p':
            k = int(lines[2])
            num_clauses = int(lines[3])

          # Read and run DPLL
          else: 
            # Read clauses and init assignments
            int_lines = [int(literal) for literal in lines[:-1]]
            clauses.append(int_lines)
            
            for literal in int_lines:
              assignments[abs(literal)] = None
              
            count += 1
            
            # Done reading, run DPLL
            if count == num_clauses:

              start_time = time.time()
              status, assignments = DPLL(clauses, assignments)
              end_time = time.time()
              
              data = (status, end_time-start_time, num_clauses * k)
              
              # Documentation
              document(problem_number, data)
              update_axes(x_sat, y_sat, x_unsat, y_unsat, data)
              
              print(status, assignments)
              
    # Graphing
    graph(x_sat, y_sat, SAT)
    graph(x_unsat, y_unsat, UNSAT)

  # Invalid input
  except FileNotFoundError:
    print("File not found")
   
main()