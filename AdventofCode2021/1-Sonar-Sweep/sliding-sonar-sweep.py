from typing import List

import sys

"""
Puzzle 2: Count num of depth increases from prev sliding window measurement

stdin reqs: 
sys.argv[1] # an input txt file containing one depth value per line
sys.argv[2] # slider size int

Method:
1) set up counter
2) starting sum (given range of slider_size) -> prev_depths
3) enumerate (i, depth) loop through input til i = -slider_size
4) sum(depths[i:i + slider_size]) -> current_depths
5) if current_depths > prev_depths, counter + 1
6) current_depths -> prev_depth
7) after loop, return counter
"""

def file_to_list(name: str) -> List[int]:
    with open(name, "r") as depth_file: # open input
        lines = [int(line) for line in depth_file.readlines() if line.strip()] # line eles -> list, no whitespace
    return(lines)

def depth_inc(depths: List[int], slider_size: int) -> int:
    """
    Use a counter to count each time the sonar sweep reports a depth increase over the previous
    >>> depth_inc([607, 618, 618, 617, 647, 716, 769, 792], 3)
    5
    """
    counter = 0 # 1)
    prev_depths = sum(depths[0:slider_size]) # 2)
    for i, depth in enumerate(depths[:-(slider_size-1)]): # 3) depth is a throwaway, alternative: len()
        current_depths = sum(depths[i:i+slider_size]) # 4)
        if current_depths > prev_depths: # 5)
            counter += 1
        prev_depths = current_depths # 6)
    return(counter) # 7)

def main():
    depth_list = file_to_list(sys.argv[1]) # stdin txt -> list
    print(depth_inc(depth_list, int(sys.argv[2]))) # return counter for increasing sliding depth sum to stdout

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()