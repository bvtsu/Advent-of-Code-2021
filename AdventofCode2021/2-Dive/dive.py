from functools import reduce
from typing import Tuple

import pandas as pd
import sys

"""
Puzzle 1: Determine multiplicative product of final coordinates 
(horizontal, depth) for planned dive course

Expected input format:
forward X # increases the horizontal position by X units.
down X # increases the depth by X units.
up X # decreases the depth by X units.

Method: csv_to_coord_df()->df_to_coords()->coord_mul() # alternative: motif from 3.10
1) Generate dataframe from input
2) sum vals associated w/ string 'forward' -> h_pos # horizontal
3) Subtract sums of vals associated w/ string 'down' from string 'up' -> d_pos # depth
4) return tuple(h_pos, d_pos)
5) Multiply coords -> print to stdout
"""
def csv_to_coord_df(path: str) -> pd.DataFrame:
    return(pd.read_csv(path, delim_whitespace=True, names=['Coord_type','Dist_unit'])) # 1)

def df_to_coords(input_df: pd.DataFrame) -> Tuple[int, int]:
    """
    Determine h_pos and d_pos coordinates for planned dive course
    1) Sum Dist_unit vals grouped by Coord_type vals in pd.DataFrame
    2) Subtract summed 'up' vals from summed 'down' vals

    Example
    --------
    >>> import pandas as pd
    >>> df_test = pd.DataFrame([['forward', 4], ['down', 5], ['up', 6]],
    ...                         columns=['Coord_type', 'Dist_unit'])
    >>> df_to_coords(df_test)
    (4, -1)
    """
    aggregated_sum = input_df.groupby('Coord_type').sum() # sum all vals associated with each Coord_type string
    h_pos = aggregated_sum.Dist_unit['forward'] # 2)
    d_pos = aggregated_sum.Dist_unit['down'] - aggregated_sum.Dist_unit['up'] # 3)
    return((h_pos, d_pos)) # 4)

def coord_mul(incoords: Tuple[int, int]) -> int:
    """
    Multiply elements of tuple record with each other
    
    Example
    --------
    >>> coord_mul((4, -1))
    -4
    """
    return(reduce(lambda x, y: x*y, incoords)) # 5) reduce to apply lambda mul to all eles

def main():
    input_df = csv_to_coord_df(sys.argv[1]) # 1)
    coords = df_to_coords(input_df) # 2-4)
    print(coord_mul(coords)) # 5)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()