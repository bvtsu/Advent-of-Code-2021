# Challenge Day 5:

import numpy as np
import operator
import pandas as pd
import sys

"""
Puzzle 2: Count number of points with >= 2 path* overlap
*all paths considered

Method (UPDATED 2021-12-14):
1) lazy pandas dataframe style (x1, y1, x2, y2, horiz/vert/diag type) 
2) add data corresponding to path type
3) create dotplot grid WITH numpy array of arrays, using 0's to rep for .
4) loop through diag type, += 1 at locs based on signage and dist of Ydist and Xdist
5) loop through horiz type, += 1 at locs by list comp across rows
6) loop through vert type, transpose dotplot, += 1 at locs by list comp across rows, then re-transpose
7) after loop, count any occurrences >= 2
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
    Fill Direction col with vert/horiz strings, row-based on whether:
    1) X vals are fixed (vert)
    2) Y vals are fixed (horiz)
    3) neither vert or horiz (diag)
    """
    for index, row in in_df.iterrows():
        if row['X1'] == row['X2']:
            in_df.loc[index, 'Direction'] = "vert"
        elif row['Y1'] == row['Y2']:
            in_df.loc[index, 'Direction'] =  "horiz"
        else:
            in_df.loc[index, 'Direction'] =  "diag"
    in_df = in_df.dropna(subset = ['Direction'])
    return(in_df)

ops = {
    '+' : operator.add,
    '-' : operator.sub
    } # store dict of mathematical operator values callable by string keys

def eval_op(op1: int, oper: str, op2: int) -> int:
    """
    evaluate operation called by string for two int vals
    """
    op1, op2 = int(op1), int(op2)
    return ops[oper](op1, op2)

def set_ops(Xdist: int, Ydist: int) -> int:
    """
    determine pos/neg directionality of X and Y vals
    """
    setX = '+'
    setY = '+'
    if Ydist < 0:
        setY = '-'
    if Xdist < 0:
        setX = '-'
    return(setX, setY)

def plot_diag(in_dotplot: np.ndarray, x1: int, x2: int, y1: int, y2: int):
    """
    use pos/neg directionality of X and Y vals to add +1 along diag coordinates
    """
    Xdist = x2-x1
    Ydist = y2-y1
    X_op, Y_op = set_ops(Xdist, Ydist)
    tracker = 0
    while tracker <= abs(Xdist): # keep going til tracker covers dist
        Y_ind = eval_op(y1, Y_op, tracker)
        X_ind = eval_op(x1, X_op, tracker)
        in_dotplot[Y_ind, X_ind] += 1
        tracker += 1

def plot_allDiags(in_df: pd.DataFrame, in_dotplot: np.ndarray) -> np.ndarray:
    """
    for each row in df of diag coords, add +1 along diag coords
    return dotplot with accumulated diag paths
    """
    coord_df_diags = in_df.sort_values(by = "X1")
    filtered_diags = coord_df_diags[coord_df_diags['Direction'] == "diag"]
    for index, row in filtered_diags.iterrows():
        plot_diag(in_dotplot, row["X1"], row["X2"], row["Y1"], row["Y2"])
    return(in_dotplot)

def plot_altpaths(in_df: pd.DataFrame, in_dotplot: np.ndarray, direction: str) -> np.ndarray:
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

    # fill with diag, horiz, vert data
    diag_filled = plot_allDiags(directional_df, path_dotplot) # 4)
    horiz_filled = plot_altpaths(directional_df, diag_filled, "horiz") # 5)
    vert_filled = plot_altpaths(directional_df, horiz_filled, "vert") # 6)
    print(count_stacked(vert_filled)) # 7)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()