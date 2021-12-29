# Challenge Day 4:
import numpy as np
import sys
from collections import deque
from typing import List, Deque

"""
Needs tests added BT 2021-12-7

Puzzle 2: Identify and score the last winning bingo board

Method:
1) store first line as deque
2) read rest of text file as list of arrays (bingo rows, cols)
3) def empty call_list to add pop'd values from deque
4) while loop until bingo happens
5) add bingo call from deque to call_list
6) remove bingo call from deque (via .popleft())
7) check for bingo in rows/cols of any boards, append winners to winning_boards
8) when while loop is done, obtain last winning board index (last_bingo)
9) locate values of subarray/bingo board by last_bingo
10) calculate unmarked sum of winning board (vals in last winning board not in call_list)
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

def transpose_by_subarrs(in_subarr: np.ndarray) -> np.ndarray:
    """
    From an array of arrays, transpose each subarray.
    This allows same row operations for both horizontal and vertical bingo calls.
    """
    transposed_subarrs = list(np.transpose(sub_arr) for sub_arr in in_subarr)
    transposed_arr = np.concatenate(transposed_subarrs)
    return(transposed_arr) # 2) these are the bingo columns, in row format

def bingo_check(in_arr: np.ndarray, in_calls: List[int], removed_boards: List[int]) -> int:
    """
    Updated bingo_check() from first_bingo.py (Puzzle 1)

    rather than determining when bingo first occurs,
    moves boards (in_arr) that has achieved bingo w/ each call to removed_boards list
    returns num of boards w/ bingo
    """
    for index, rows in enumerate(in_arr):
        board_num = int(index/len(in_arr[0]))
        if board_num not in removed_boards:
            if set(rows).issubset(in_calls):
                removed_boards.append(board_num)
    return(len(removed_boards))

def last_winning_board(in_calls: List[int], in_dq: Deque[int], row_arr: np.ndarray, col_arr: np.ndarray) -> int:
    """
    Store winning board indices until the last board wins (num_winning_boards = max_board num)
    Raises exception to return index of last winning board
    """
    winning_boards = []
    max_board_num = len(row_arr)/len(row_arr[0])
    while True: # 4)
        try:
            in_calls.append(in_dq[0]) # 5)
            in_dq.popleft() # 6)
            num_winning_boards = bingo_check(row_arr, in_calls, winning_boards) # 7)
            assert(num_winning_boards < max_board_num)
            num_winning_boards = bingo_check(col_arr, in_calls, winning_boards) # 7)
            assert(num_winning_boards < max_board_num)
        except AssertionError:
            last_to_win = winning_boards[-1]
            return(last_to_win) # 8)

def subarr(in_subarrs: np.ndarray, in_index: int) -> np.ndarray:
    """
    Use in_index to return the associated, full last-bingo subarray
    """
    return(in_subarrs[in_index]) # 9)

def unmarked_sum(input_subarry: np.ndarray, input_call_list: List[int]) -> int:
    """
    Filter for uncalled numbers using in_call list, then sum
    """
    return(sum(np.setdiff1d(input_subarry, input_call_list))) # 10)

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
    last_bingo = last_winning_board(call_list, dq_calls, arr, tposed_arr) # 4-8)
    winning_board = subarr(arr_split, last_bingo) # 9)
    board_score = unmarked_sum(winning_board, call_list) # 10)
    print(final_score(board_score,call_list)) # 11)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()