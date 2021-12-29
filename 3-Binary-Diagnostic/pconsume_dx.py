from functools import reduce
from typing import List, Tuple

import pandas as pd
import sys

"""
Puzzle 1: Obtain the gamma and epsilon rate
gamma rate - binary num composed of the most common bits in each input pos
epsilon rate - binary num composed of the least common bits in each input pos

bits are binary digits

Method: csv_to_bitpos_df()->df_to_bincoords()->coord_mul()
1) input -> df with each bit in its own col
2) gamma = [], epsilon = []
3) sum by cols -> 1's in each pos
4) for loop through each col of sums
5) subtract each col sum from num of rows -> 0's in each pos
6) if 1's > 0's, gamma.append(1), epsilon.append(0)
7) if 1's < 0's, gamma.append(0), epsilon.append(1)
8) gamma, epsilon int list -> str list for concat
9) gamma_concat.join(), epsilon_concat.join()
10) gamma_concat, epsilon_concat -> (int(gamma_concat, 2), int(epsilon_concat))
11) Multiply rates -> print resulting power consumption to stdout
"""
def csv_to_bitpos_df(path: str) -> pd.DataFrame:
    with open(path, 'r') as file:
        lines = [list(map(int, line.rstrip('\n'))) for line in file if line.strip()] # remove \n and convert each line to list of digits
    return(pd.DataFrame(lines)) # 1)

def bits_to_decimal(bits_int: List[int]) -> int:
    """
    Converts individual digits of a binary number* into joined decimal val
    *Only int values of 1 and 0 are allowed in the list
    
    Example
    ---------
    >>> digit_list = [1, 0, 1, 0, 1, 1]
    >>> bits_to_decimal(digit_list)
    43
    """
    bits_strL = [str(bits) for bits in bits_int]
    bits_concat = "".join(bits_strL)
    return(int(bits_concat,2))

def df_to_decord(df: pd.DataFrame) -> Tuple[int, int]:
    """
    From a pd dataframe:
    a) Determines most/least frequest occurring binary digit across a 
    b) if 1's > 0's, assign gamma list 1 (int) and epsilon list 0 (int)
    c) if 1's < 0's, assign gamma list 0 (int) and epsilon list 1 (int)
    d) return record of decimal vals representing joined gamma and epsilon
    
    Example
    ---------
    >>> import pandas as pd
    >>> bin_df = pd.DataFrame([[1, 0, 1], [1, 0, 0], [1, 1, 1]],
    ...                         columns=[0, 1, 2])
    >>> df_to_decord(bin_df)
    (5, 2)
    """
    gamma = [] # 2)
    epsilon = [] # 2)
    aggregated_df = df.sum(axis=0) # 3)
    for bitsum in aggregated_df: # 4)
        zero = len(df) - bitsum # 5)
        if bitsum > zero: # 6)
            gamma.append(1)
            epsilon.append(0)
        else: # 7)
            gamma.append(0)
            epsilon.append(1)
    gamma_dec = bits_to_decimal(gamma) # 8-9)
    epsilon_dec = bits_to_decimal(epsilon) # 8-9)
    return((gamma_dec, epsilon_dec)) # 10)

def record_mul(inrecord: Tuple[int, int]) -> int:
    """
    Multiply elements of tuple record with each other
    
    Example
    --------
    >>> record_mul((5, 2))
    10
    """
    return(reduce(lambda x, y: x*y, inrecord)) # 11) reduce to apply lambda mul to all eles

def main():
    input_df = csv_to_bitpos_df(sys.argv[1]) # 1)
    decord = df_to_decord(input_df) # 2-10)
    print(record_mul(decord)) # 11)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()