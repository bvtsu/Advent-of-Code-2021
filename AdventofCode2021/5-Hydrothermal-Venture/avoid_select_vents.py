# Challenge Day 5:

import numpy as np
import pandas as pd
import sys

"""
Puzzle 1: Count number of points with >= 2 path* overlap
*horiz and vert paths considered

Method (UPDATED 2021-12-14):
1) lazy pandas dataframe style (x1, y1, x2, y2, horiz/vert type) 
2) add data corresponding to path type
3) create dotplot grid WITH numpy array of arrays, using 0's to rep for "."
4) loop through horiz type, += 1 at locs by list comp across rows
5) loop through vert type, transpose dotplot, += 1 at locs by list comp across rows, then re-transpose
6) after loop, count any occurrences >= 2
"""

def csv_to_coord_df(path: str) -> pd.DataFrame:
    """
    Split input txt file by , and -> to acquire df with X1, Y1, X2, Y2
    A Direction col is named, to-be filled with add_direction()
    """
    return(pd.read_csv(path, sep=",|->", names=['X1','Y1','X2','Y2', 'Direction'], engine='python')) # txt import separated by two delims , and ->

def create_np_dotplot(x_size: int, y_size: int) -> np.ndarray:
    """
    Create numpy array of zeroes to represent dotplot for paths
    """
    np_dotplot = np.zeros((y_size, x_size), dtype = int)
    return(np_dotplot)

def max_XY(in_df: pd.DataFrame) -> int:
    """
    Return X and Y dotplot bounds from input data
    """
    max_Xval = max(in_df[["X1", "X2"]].max(axis = 0))
    max_Yval = max(in_df[["Y1", "Y2"]].max(axis = 0))
    return(max_Xval, max_Yval)

def add_direction(in_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill Direction col with vert/horiz strings, row-based 
    on whether X vals are fixed (vert) or Y vals are fixed (horiz)
    """
    for index, row in in_df.iterrows():
        if row['X1'] == row['X2']:
            in_df.loc[index, 'Direction'] = "vert"
        if row['Y1'] == row['Y2']:
            in_df.loc[index, 'Direction'] =  "horiz"
    in_df = in_df.dropna(subset = ['Direction'])
    return(in_df)

def plot_paths(in_df: pd.DataFrame, in_dotplot: np.ndarray, direction: str) -> np.ndarray:
    """
    Takes df filtered by direction, and adds +1 along row-provided coordinate path

    Special: if direction is vert, transpose to use operations designed for horiz paths,
    then transpose after operations are performed
    """
    if direction == "vert":
        in_dotplot = np.transpose(in_dotplot)
        col = 'X1'
        axis_st = 'Y1'
        axis_end = 'Y2'
    else:
        col = 'Y1'
        axis_st = 'X1'
        axis_end = 'X2'
    sort_df = in_df.sort_values(by = col)
    filtered_df = sort_df[sort_df['Direction'] == direction]
    for index, row in filtered_df.iterrows():
        row_ind = row[col]
        st = row[axis_st]
        end = row[axis_end]
        if st < end:
            in_dotplot[row_ind, st:end+1] += 1
        elif st > end:
            in_dotplot[row_ind, end:st+1] += 1
        else:
            in_dotplot[row_ind, st:end+1] += 1
    if direction == "vert":
        in_dotplot = np.transpose(in_dotplot)
    return(in_dotplot)

def count_stacked(in_dotplot: np.ndarray) -> int:
    """
    count num of positions with vals >= 2 (where paths overlapped)
    """
    stacked_paths = (in_dotplot >= 2).sum()
    return(stacked_paths)

def main():
    # setup dotplot numpy array of 0's
    coord_df = csv_to_coord_df(sys.argv[1]) # 1)
    directional_df = add_direction(coord_df) # 2)
    X_max, Y_max = max_XY(directional_df) # 3)
    path_dotplot = create_np_dotplot(X_max+1, Y_max+1) # 3)

    # fill with horiz, vert data
    horiz_filled = plot_paths(directional_df, path_dotplot, "horiz") # 5)
    vert_filled = plot_paths(directional_df, horiz_filled, "vert") # 6)
    print(count_stacked(vert_filled)) # 7)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()