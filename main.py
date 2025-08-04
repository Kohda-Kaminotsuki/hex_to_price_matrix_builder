# Building an average from existing adjacents constructing matrix
# Example:
# [ NN , 10 , NN            [ 27 , 10 , 23
#   20 , 50 , 10    -->       20 , 50 , 10
#   10 , NN , NN]             10 , 24 , 28]

# Process: recursive for r in range(0, 255), g in range(0, 255), b in range(0, 255)
# if r, g, b is NN: try: average (r-1, g, b) (r+1, g, b) (r, g-1, b) (r, g+1, b) (r, g, b-1) (r, g, b+1), (r-1, g-1, b), (r+1, g+1, b), (r-1, g+1, b), (r+1, g-1, b), (r-1, g, b-1), (r+1, g, b+1), (r, g-1, b-1), (r, g+1, b+1), (r-1, g+1, b-1), (r+1, g-1, b+1)
# should have 26 max numbers to average with 
# if r, g, b of testing is not NaN and not -1: iterate up 1 averaging length and add value to sum
# if r, g, b of testing color is NaN: set value to -1 and run averager on it
# if r, g, b of testing color is -1: continue to next iteration
from itertools import product
import json
import sys
import pickle

rgb_value_dictionary = { (0, 0, 0): 100,
                         (255, 255, 255): 100 }

def open_existing():
    try:
        with open(sys.argv[1], "rb") as load_file:
            rgb_value_dictionary = pickle.load(load_file)
    except Exception as e:
        print(f"Error loading existing RGB value dictionary: {e}")
        sys.exit(1)

def check_dictionary_valid():
    for key in rgb_value_dictionary: 
        assert isinstance(key, tuple), f"{key} invalid, key must be tuple!"
        assert isinstance(rgb_value_dictionary[key], int), f"{key} value invalid, value must be int!"
        
def average_adjacent(r,g,b):
    if (r, g, b) in rgb_value_dictionary and (rgb_value_dictionary[(r,g,b)] != -1): return rgb_value_dictionary[(r, g, b)]
    average_list_length = 0
    average_sum = 0
    for neighbor in [
        (r-1, g, b),
        (r, g-1, b),
        (r, g, b-1),
        
        (r+1, g, b),
        (r, g+1, b),
        (r, g, b+1),

        (r-1, g-1, b),
        (r-1, g, b-1),
        (r, g-1, b-1),

        (r-1, g+1, b),
        (r-1, g, b+1),
        (r, g-1, b+1),

        (r+1, g-1, b),
        (r+1, g, b-1),
        (r, g+1, b-1),

        (r+1, g+1, b),
        (r+1, g, b+1),
        (r, g+1, b+1),

        (r-1, g-1, b-1),

        (r-1, g-1, b+1),
        (r-1, g+1, b-1),
        (r+1, g-1, b-1),

        (r-1, g+1, b+1),
        (r+1, g-1, b+1),
        (r+1, g+1, b-1),

        (r+1, g+1, b+1)
]:
        if neighbor in rgb_value_dictionary and rgb_value_dictionary[neighbor] != -1:
            average_sum += rgb_value_dictionary[neighbor]
            average_list_length += 1
        elif neighbor not in rgb_value_dictionary:
            rgb_value_dictionary[neighbor] = -1
            rgb_value_dictionary[neighbor] = average_adjacent(neighbor[0], neighbor[1], neighbor[2]) # type: ignore
    if average_list_length == 0: raise Exception(f"Recursion found no input for dictionary to average from.")
    return average_sum // average_list_length 

if len(sys.argv) == 2:
    open_existing()
elif len(sys.argv) > 2:
    print("Usage: python script.py [optional: path to existing rgb_value_dictionary.pkl]")
    sys.exit(1)

check_dictionary_valid()

for r, g, b in product(range(256), range(256), range(256)):
    if (r, g, b) not in rgb_value_dictionary:
        rgb_value_dictionary[(r, g, b)] = average_adjacent(r, g, b)

if len(sys.argv) == 2:
    confirm = input("Successfully built dictionary, would you like to save it? (y/n/save_as)")
    if confirm.lower() == "y":
        with open(sys.argv[1], "wb") as f:
            pickle.dump(rgb_value_dictionary, f)
        sys.exit(0)
    elif confirm.lower() == "save_as":
        new_file_name = input("Enter new name for dictionary file: ").strip()
        new_file_name = f"{new_file_name}.pkl" if not new_file_name.endswith(".pkl") else new_file_name
        with open(new_file_name, "wb") as f: 
            pickle.dump(rgb_value_dictionary, f)
        sys.exit(0)
    else:
        print("Dictionary not saved.")
        confirm = input("Press any key to exit.")
        sys.exit(0)
else:
    new_file_name = input("Enter new name for dictionary file: ").strip()
    new_file_name = f"{new_file_name}.pkl" if not new_file_name.endswith(".pkl") else new_file_name
    with open(new_file_name, "wb") as f: 
        pickle.dump(rgb_value_dictionary, f)
    sys.exit(0)
