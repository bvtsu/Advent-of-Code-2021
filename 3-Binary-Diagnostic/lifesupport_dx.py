from functools import reduce
from typing import List, Tuple

import pandas as pd
import sys

"""
Puzzle 2: Obtain the oxygen and CO2 scrubber rating
oxygen rating - binary num remaining after sequentially 
collecting most common bits in each input pos

CO2 scrubber rating - binary num remaining after sequentially 
collecting least common bits in each input pos

If bits are equal, 1 assigned to oxygen, 0 assigned to C02

Method: csv_to_bitpos_df()-> rating_filter()->record_mul()
1) input -> df with each digit in its own col
2) oxygen = [], CO2 = []
3) for loop through each col
4) filter by most/least for oxygen/CO2 from prev bitsums, if applicable
5) sum col -> # of bits = 1
6) determine if 5) is > , <, or = (# of bits)/2 -> append 0 or 1 depending on mcb/lcb state
7) oxygen, CO2 int list -> str list for concat
8) convert oxygen and CO2 rating from binary number to decimal val
9) Multiply rates -> print resulting life support rating to stdout
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

def rating_filter(df: pd.DataFrame, rating_type: str)->int:
    """
    most common bits (mcb)
    least common bits (lcb)

    Input
    -----------
    rating_type: 
    'o' for oxygen - binary num remaining after sequentially 
    collecting mcb in each input pos
    any str for CO2 - binary num remaining after sequentially 
    collecting lcb in each input pos
    
    Function
    --------
    Loops through df cols, storing mcb/lcb of prev col to use as a filter for the next col
    When 1 binary number composed of filtered bits remains, convert to decimal val

    Example
    ---------
    >>> import pandas as pd
    >>> bin_df = pd.DataFrame([[1, 0, 1], [1, 0, 0], [0, 1, 1]],
    ...                         columns=[0, 1, 2])
    >>> rating_filter(bin_df, 'o')
    5
    >>> rating_filter(bin_df, 'c')
    3
    >>> rating_filter(bin_df, 'anystring')
    3
    """
    rating = [] # 2)
    rating_df = df.copy()
    for colname in df: # 3)
        if colname != 0:
            rating_df = rating_df[rating_df[colname-1]==rating[colname-1]] # 4)
            if len(rating_df) == 1: # if only one row remains, end loop
                rating = rating_df.iloc[0,:].to_list() # store remaining row of bits
                break
        rating_1bit = rating_df[colname].sum() # 5)
        if rating_type == 'o': # 6)
            if rating_1bit >= len(rating_df)/2: # if 1 is mcb
                rating.append(1)
            else: # if 0 is mcb
                rating.append(0)
        else: # 6)
            if rating_1bit >= len(rating_df)/2: # if 0 is lcb
                rating.append(0)
            else: # if 1 is lcb
                rating.append(1)
    rating_dec = bits_to_decimal(rating) # 8)
    return(rating_dec)

def record_mul(inrecord: Tuple[int, int]) -> int:
    """
    Multiply elements of tuple record with each other
    
    Example
    --------
    >>> record_mul((5, 2))
    10
    """
    return(reduce(lambda x, y: x*y, inrecord)) # 9) reduce to apply lambda mul to all eles

def main():
    input_df = csv_to_bitpos_df(sys.argv[1]) # 1)
    oxygen = rating_filter(input_df, 'o') # 2-8)
    CO2 = rating_filter(input_df, 'c') # 2-8)
    print(record_mul((oxygen, CO2))) # 9)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()