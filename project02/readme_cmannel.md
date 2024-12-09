**Team name:** cmannel
**Names of all team members:** Celeste Mannel
**Link to github repository:** https://github.com/cmannel/nd-cse-30151-fa24
**Which project options were attempted:** DumbSAT solver implementing DPLL

**Approximately total time spent on project:** 10 hrs

**The language you used, and a list of libraries you invoked:** I used python and invoked csv, argparse, and deque from collections libraries.

**How would a TA run your program (did you provide a script to run a test case?)** ./traceTM_cmannel.py test_files/a_plus.csv aaa aaaa --terminate 5
flag is optional, program can support multiple input strings

**A brief description of the key data structures you used, and how the program functioned.** To represent the possible NTM states, I used a tree by creating the TreeNode class. I used lists to represent the rules and the node states.

The NTM tracing program functions by representing the TM description as a TuringMachine class and storing each state of the machine as a TreeNode. 
The TuringMachine class has the following attributes: name, Q, sigma, gamma, start_state, accept_state, reject_state, rules. The TreeNode class has the following attributes: index (position of the node in the tree), string (string on the tape), children (list to hold child nodes), state (state of the TM [curr_state, head_index]).

The main function does the following:
Parse the arguments: if invalid entry, throw error. If flag used, set limit.
Use the filename provided to create the TM
Initiate the first node at the start_state at the first char of the string.
Run bfs on the node, generating the tree as each node is visited through the get_children function of the TreeNode class
Once bfs is complete, either because accept was reached, no accept was found, or the limit was reached, print the corresponding data

**A discussion as to what test cases you added and why you decided to add them (what did they tell you about the correctness of your code). Where did the data come from? (course website, handcrafted, a data generator, other)**

I used three test cases: a_plus, equal_01s, and 2x0_DTM
In each case, the TM was effective in recognizing strings in the languages and deciding strings that are not in the language.

I used these files to test my code and debug issues that I had. For example, I identified an issue in my concatenation when creating the new tape string and when creating the next tape configuration. By printing out the configurations, it was easier to see where in the code I had gone wrong.


**An analysis of the results, such as if timings were called for, which plots showed what? What was the approximate complexity of your program?**

After debugging, I can say that the results are correct. I manually tested all the cases provided. For each file provided, the machine can decide strings that are and are not in the language described by the machine. 

**A description of how you managed the code development and testing.**

primarily used print statements to determine what my code was doing. I wrote the functions in small parts and tested their correctness by printing the structures before and after running the functions.

I embedded print formatting for each class to facilitate this debugging.

**Did you do any extra programs, or attempted any extra test cases** no.
