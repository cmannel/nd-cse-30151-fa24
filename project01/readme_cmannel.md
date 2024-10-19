**Team name:** teamceleste
**Names of all team members:** Celeste Mannel
**Link to github repository:** https://github.com/cmannel/nd-cse-30151-fa24
**Which project options were attempted:** DumbSAT solver implementing DPLL
**Approximately total time spent on project:** 10 hrs

**The language you used, and a list of libraries you invoked:**
I used python and invoked csv, time, matplotlib.pyplot, and np libraries

**How would a TA run your program (did you provide a script to run a test case?)**
A TA can run this program best in Colab to see the graphics.
If the TA wanted to run the program in the terminal, they would need to comment out the lines that call graph() (lines 204-205) to avoid this error `ModuleNotFoundError: No module named 'matplotlib'`. Then, they could run python3 `.\dpll_sat.py` in the project01 directory. 
When the TA runs the code, they will be prompted to input a file name. Here any input .cnf file in the project01 directory can be used. 

**A brief description of the key data structures you used, and how the program functioned.**
For the clauses, I used a 2D array. This way, I kept track of the clauses in a single array. 
For the assignments to the variables, I used a dict that kept track of the variables and their assignments. This allowed for easy access and reference to its value.

The program functions by heavily relying on simplifications to make the searching easier. For example, pure propagation and unit propagation simplify the clauses by removing clauses literals where it is safe to do so. A clause is removed when the whole clause is satisfied, and a literal is removed when it evaluates to false. 
If the array of clauses ends up empty, then every clause evaluated to true and the wff is therefore satisfiable. If at any point there is an empty clause, then every literal in it evaluated to false, making the wff unsatisfiable. These are the two base cases of the recursive function.

In unit propagation, for every unit variable, we give an assignment, and since the unit must be satisfied, we can remove every clause with that single literal or remove every instance of the opposite literal in the other clauses.
In pure propagation, we create an array of literals which have no occurrences of their complement in any other clauses. These variables we can remove, since they can safely not conflict and are not dependent upon any other variable. 

Finally, we choose a new unassigned variable to test and recursively call DPLL on, if that fails, then we call the opposite assignment. This is what facilitates the backtracking.

**A discussion as to what test cases you added and why you decided to add them (what did they tell you about the correctness of your code). Where did the data come from? (course website, handcrafted, a data generator, other)**
I have larger and smaller test cases, both a mix of SAT and UNSAT problems. These test files helped me realize that my code had an issue when it comes to unit propagating. It continued to fit an assignment upon literals that have already been assigned and forces an assignment to make the wff satisfiable. This was incorrect. 

By debugging, I discovered that I was deleting a clause from clauses while iterating through clauses at the same time. This was causing issues when I tried to access values after deleting that no longer exissted. 

**An analysis of the results, such as if timings were called for, which plots showed what? What was the approximate complexity of your program?**
It appears that as the number of literals increases, the complexity of the program increases as well. This is due to the various iterations and nesting of loops throughout the algorithm. There is an exponential trend to the complexity data.

**A description of how you managed the code development and testing.**
I primarily used print statements to determine what my code was doing. To test, I simplified examples I knew were satisfiable and traced through the steps to ensure each part of the algorithm was funcioning correctly.

**Did you do any extra programs, or attempted any extra test cases**
I attempted a good mix of satisfiable and unsatisfiable cases. I have simple test cases to facilitate correctness checking.