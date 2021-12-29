from functools import reduce
from typing import Tuple

import pandas as pd
import sys

"""
Puzzle 2: Determine multiplicative product of final coordinates 
(horizontal, depth) for planned dive course

Expected input format:
forward X # increases the horizontal by X units and depth by aim * X.
down X # increases the aim by X units.
up X # decreases the aim by X units.


Method: csv_to_coord_df()->df_to_coords()->coord_mul()-> # takes pandas dataframe(), alternative: motif from 3.10
1) Generate dataframe from input
2) Set up counter for aim, d_pos, h_pos
3) for loop through df rows
4) if down/up, +/- units to aim
5) if forward, + units to h_pos, + units*aim to d_pos
6) return tuple(h_pos, d_pos)
*7) Multiply coords -> print to stdout
"""
def csv_to_coord_df(path: str) -> pd.DataFrame:
    return(pd.read_csv(path, delim_whitespace=True, names=['Coord_type','Dist_unit'])) # 1)

def df_to_coords(input_df: pd.DataFrame) -> Tuple[int, int]:
    """
    Determine h_pos and d_pos coordinates for planned dive course    
    1) Set up counter for aim, d_pos, h_pos
    2) for loop through df rows
    3) if down/up, +/- units to aim
    4) if forward, + units to h_pos, + units*aim to d_pos

    Examples
    --------
    >>> import pandas as pd
    >>> df_test = pd.DataFrame([['forward', 4], ['down', 5], ['up', 6]],
    ...                         columns=['Coord_type', 'Dist_unit'])
    >>> df_to_coords(df_test)
    (4, 0)
    
    >>> df_test = pd.DataFrame([['down', 4], ['up', 5], ['forward', 6]],
    ...                         columns=['Coord_type', 'Dist_unit'])
    >>> df_to_coords(df_test)
    (6, -6)
    """
    aim = 0 # 2)
    h_pos = 0 # 2)
    d_pos = 0 # 2)
    for index, row in input_df.iterrows(): # 3) index is throwaway var
        if row['Coord_type'] == 'down': # 4)
            aim += row['Dist_unit']
        elif row['Coord_type'] == 'up': # 4)
            aim -= (row['Dist_unit'])
        else: # 5)
            d_pos += (aim * row['Dist_unit'])
            h_pos += row['Dist_unit']
    return((h_pos, d_pos)) # 6)

def coord_mul(incoords: Tuple[int, int]) -> int:
    """
    Multiply elements of tuple record with each other
    
    Example
    --------
    >>> coord_mul((4, -1))
    -4
    """
    return(reduce(lambda x, y: x*y, incoords)) # 7) reduce to apply lambda mul to all eles

def main():
    input_df = csv_to_coord_df(sys.argv[1]) # 1)
    coords = df_to_coords(input_df) # 2-4)
    print(coord_mul(coords)) # 5

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()