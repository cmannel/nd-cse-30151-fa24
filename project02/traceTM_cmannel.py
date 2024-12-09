#!/usr/bin/env python3

# traceTM_cmannel.py
# cmannel
# NTM tracer

import argparse
import csv
from collections import deque

class TuringMachine:
    def __init__(self):
        # Initializes a Turing Machine with the specified attributes.
        self.name  = None         # Name of the Turing Machine
        self.Q     = []           # List of state names
        self.sigma = []           # List of characters from the input alphabet (Σ)
        self.gamma = []           # List of characters from the tape alphabet (Γ)
        self.start_state  = None  # The start state of the Turing Machine
        self.accept_state = None  # The accept state of the Turing Machine
        self.reject_state = None  # The reject state of the Turing Machine
        self.rules = []           # List of transition rules [curr_state, input, next_state output, direction]

    def __repr__(self):
        # String representation of the Turing Machine for debugging
        return (
            f"TuringMachine(name={self.name}, Q={self.Q}, sigma={self.sigma}, "
            f"gamma={self.gamma}, start_state={self.start_state}, "
            f"accept_state={self.accept_state}, reject_state={self.reject_state}"
        )
        
class TreeNode:
    def __init__(self, index, string, children, state):
        self.index = index              # Position of the node in the tree (eg. 132) represents the path
        self.string = string            # String on tape
        self.children = children        # List to hold child nodes (eg. 1321, 1322, 1323...)
        self.state = state              # TM state [curr_state, head_index, next_state output, direction]
        
    def __repr__(self):
        # String representation of the Node for debugging
        return (
            f"Node(index={self.index}, string = {self.string}, children={self.children}, state={self.state}"
        )           
    
    def get_children(self, current_node, rules, end_index):
        # Function to dynamically generate children when visiting a node
        node_index = current_node.index
        TM_input = current_node.string
        curr_state = current_node.state[0]
        head_index = current_node.state[1]
        
        children = []
        new_node_index = (node_index * 10)
        
        for rule in rules:
            new_node_index += 1
                    
            # Check if reached a blank space on tape
            if head_index >= len(TM_input):
                input_char = '_'
            else:
                input_char = TM_input[head_index]
            
            # if node_index == 112:
                # print(f"    curr_state {curr_state}, head_at {input_char}.")
                # print(f"    target_state {rule[0]}, target_input {rule[1]}.")
                # print("   ", curr_state == rule[0], input_char == rule[1])
            
            # Find rule that applies, create a node per rule
            if curr_state == rule[0] and input_char == rule[1]:  
                
                # Concatenate by cases              
                try:
                    TM_input = TM_input[0:head_index] + rule[3] + TM_input[head_index + 1:]
                    configuration = TM_input[0:head_index] + curr_state + rule[3] + TM_input[head_index + 1:]
                except:
                    TM_input = TM_input + rule[3]
                    configuration = TM_input + curr_state + rule[3]
                
                # Move head over
                if rule[4] == 'R':
                    head_index += 1
                elif rule[4] == 'L' and head_index > 0:
                    head_index -= 1
                    
                # Set state for node
                child_state = [rule[2], head_index]
                
                child = TreeNode(new_node_index, TM_input, None, child_state)
                
                if end_index != -1:
                    length = len(str(new_node_index))
                    # print(length)
                    # print(str(new_node_index), end_index, str(end_index)[:length])
                    if str(new_node_index) == str(end_index)[:length]:
                        print(configuration)
                        
                children.append(child)
                
        return children
                
def csv_to_machine(csv_file):
    tm = TuringMachine()
    
    # Open the CSV file
    with open(csv_file, mode="r") as file:
        csv_reader = csv.reader(file)
        
        # Enumerate over the rows
        for i, row in enumerate(csv_reader):
            
            if i == 0:
                tm.name = row[0]
            if i == 1:
                tm.Q = row
            if i == 2:
                tm.sigma = row
            if i == 3:
                tm.gamma = row
            if i == 4:
                tm.start_state = row[0]
            if i == 5:
                tm.accept_state = row[0]
            if i == 6:
                tm.reject_state = row[0]
            if i >= 7:
                tm.rules.append(row)
    
    return tm

def bfs(root, accept_state, rules, limit, depth): 
    transitions_taken = 0
    node_index = 0
    if root is None:
        return None, transitions_taken, node_index

    queue = deque([root])  # Initialize the queue with the root node
   
    while queue:
        current_node = queue.popleft()  # Dequeue the front node
        node_index = current_node.index
     
        if current_node.state[0] == accept_state:
            return current_node, transitions_taken, node_index # found an accept
                
        children = current_node.get_children(current_node, rules, depth)
        transitions_taken = len(str(node_index))

        # Enqueue all children of the current node
        for child in children:
            queue.append(child)
            
        if transitions_taken == limit: 
            return "Limit Exceeded", transitions_taken, node_index
        
    return None, transitions_taken, node_index # all paths rejected    
            
def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Process arguments with an optional flag for a 4th argument.")

    # Define the required positional arguments
    parser.add_argument("TM_file", type=str, help="Name of TM file")
    parser.add_argument("input", type=str, help="Input to TM")

    # Define the optional flag
    parser.add_argument("--terminate", nargs="?", const=None, type=int, help="Enable the max transition limit")

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    TM_file = args.TM_file
    TM_input = args.input
    transition_limit = args.terminate
       
    # Create Turing Machine
    tm = csv_to_machine(TM_file)
    
    # Header output
    print(f"Turing Machine: {tm.name}")
    print(f"Initial string: {TM_input}")
    
    # Begin search for accept state
    root = TreeNode(1, TM_input, None, [tm.start_state, 0])
    target = tm.accept_state
    rules = tm.rules
    accept_node, depth, node_index = bfs(root, target, rules, transition_limit, -1)
     
    # Print paths according to accept or reject state
    if accept_node == None:
        print("String rejected in", depth, "transitions")
        bfs(root, target, rules, transition_limit, node_index)
    if accept_node == "Limit Exceeded":
        print("Execution stopped after", depth, "transitions")
    else:
        print("String accepted in", depth, "transitions")
        bfs(root, target, rules, transition_limit, node_index)
        # TODO: print configuration path
        # format: left of head string, state, head character, right of string

if __name__ == "__main__":
    main()


"""
input: aaa

q1aaa
aq1aa
aaq1a
aaaq2
aaq3a


"""