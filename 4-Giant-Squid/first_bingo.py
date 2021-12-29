# Challenge Day 4:
import numpy as np
import sys
from collections import deque
from typing import List, Deque

"""
Needs tests added BT 2021-12-7

Puzzle 1: Identify and score the earliest winning bingo board

Method:
1) store first line as deque
2) read rest of text file as list of arrays (bingo rows, cols)
3) def empty call_list to add pop'd values from deque
4) while loop until bingo happens
5) add bingo call from deque to call_list
6) remove bingo call from deque (via .popleft())
7) check for bingo in rows/cols
8) when while loop is done, store winning index row/col (bingo line)
9) locate winning subarray (bingo board)
10) calculate unmarked sum of winning board (vals in winning board not in call_list)
11) report final score (unmarked sum * last val in call_list) to stdout
"""


def txt_to_dq(in_file: str) -> Deque[int]:
    """
    store first line of input txt file as a deque of future bingo calls
    """
    with open(in_file, 'r') as file:
        for line in file:
            return(deque(map(int, line.strip().split(",")))) # 1)

def txt_to_arr(in_file: str, skip_header: int) -> np.ndarray:
    """
    read input txt file excluding the header as array of arrays
    """
    in_arr = np.loadtxt(in_file, skiprows=skip_header)
    in_arr_split = np.split(in_arr, len(in_arr)/len(in_arr[0])) # assume symmetrical board
    return(in_arr, in_arr_split) # 2) These are the bingo rows

def transpose_by_subarrs(in_subarrs: np.ndarray) -> np.ndarray:
    """
    From an array of arrays, transpose each subarray.
    This allows same row operations for both horizontal and vertical bingo calls.
    """
    transposed_subarrs = list(np.transpose(sub_arr) for sub_arr in in_subarrs)
    transposed_arrs = np.concatenate(transposed_subarrs)
    return(transposed_arrs) # 2) these are the bingo columns, in row format

def bingo_check(in_arr: np.ndarray, in_calls: List[int]) -> int:
    """
    if all numbers in a row/col were called, return index of row/col
    """
    for index, rows in enumerate(in_arr):
        if set(rows).issubset(in_calls):
            return(index)

def marked_index(in_calls: List[int], in_dq: Deque[int], row_arr: np.ndarray, col_arr: np.ndarray) -> int:
    """
    Send calls from deque to in_call until bingo, which returns the index of the winning row/col.
    """
    while True: # 4)
        try:
            in_calls.append(in_dq[0]) # 5)
            in_dq.popleft() # 6)
            winning_row = bingo_check(row_arr, in_calls) # 7)
            winning_column = bingo_check(col_arr, in_calls) # 7)
            assert(winning_row == None) # 7)
            assert(winning_column == None) # 7)
        except AssertionError:
            index_out = max(i for i in [winning_row, winning_column] if i is not None)
            return(index_out) # 8)

def subarr(in_subarrs: np.ndarray, in_index: int) -> np.ndarray:
    """
    Use in_index to return the associated, full bingo subarray
    """
    return(in_subarrs[int(in_index/len(in_subarrs[0]))]) # 9)

def unmarked_sum(input_subarry: np.ndarray, in_calls: List[int]) -> int:
    """
    Filter for uncalled numbers using in_call list, then sum
    """
    return(sum(np.setdiff1d(input_subarry, in_calls))) # 10)

def final_score(unmarked_sum: int, in_calls: List[int]) -> int:
    """
    multiply sum by the last number called to trigger bingo
    """
    return(unmarked_sum*in_calls[-1]) # 11)

def main():
    dq_calls = txt_to_dq(sys.argv[1]) # 1)
    arr, arr_split = txt_to_arr(sys.argv[1], 2) # 2)
    tposed_arr = transpose_by_subarrs(arr_split) # 2)
    call_list = [] # 3)
    bingo_line = marked_index(call_list, dq_calls, arr, tposed_arr) # 4-8)
    winning_board = subarr(arr_split, bingo_line) # 9)
    board_score = unmarked_sum(winning_board, call_list) # 10)
    print(final_score(board_score,call_list)) # 11)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()