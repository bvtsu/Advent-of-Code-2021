from typing import List

import sys

"""
Puzzle 1: Count num of depth increases from prev measurement

stdin reqs: 
sys.argv[1] # an input txt file containing one depth value per line

Method: depth_inc()
1) set up counter
2) starting val -> prev_depth
3) loop through input_vals for vals
4) if next val > prev val, counter + 1
5) current val -> prev_depth
6) after loop, return counter
"""

def file_to_list(name: str) -> List[int]:
    with open(name, "r") as depth_file: # open input
        lines = [int(line) for line in depth_file if line.strip()] # line eles -> list, no whitespace, don't need readlines()
    return(lines)

def depth_inc(depths: List[int]) -> int:
    """Use a counter to count each time the sonar sweep reports a depth increase over the previous
    >>> depth_inc([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    7
    """
    counter = 0 # 1)
    prev_depth = depths[0] # 2)
    for index, depth in enumerate(depths): # 3) don't need index, alternative: no enum
        if depth > prev_depth: # 4)
            counter += 1
        prev_depth = depth # 5)
    return(counter) # 6)

def main():
    depth_list = file_to_list(sys.argv[1]) # stdin txt -> list
    print(depth_inc(depth_list)) # return depth increasing counter to stdout

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()