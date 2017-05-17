#! /usr/bin/env python3
from io import StringIO
import numpy as np
import os
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def exception_handler(message, errors=(Exception, )):
    """ wrapper for exception handling """
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except errors:
                print(message)
                exit()
        return wrapped_f
    return wrap

cd ~/Desk   @exception_handler("Matrix dimensions are not correct!", errors=IndexError)
def manhattan_tourist(n, m, down, right, diagonal=None):
    """ dynamic programming solution for manhattan tourist problem """
    b = np.empty((n, m), dtype=object)  # backtrack matrix
    s = np.zeros((n, m), dtype=float)  # sum matrix

    # Compute the first row and column.
    for i in range(1, n):
        s[i][0] = s[i-1][0] + down[i-1][0]
        b[i][0] = "↓"

    for j in range(1, m):
        s[0][j] = s[0][j-1] + right[0][j-1]
        b[0][j] = "→"

    # Compute the interior values.
    for i in range(1, n):
        for j in range(1, m):
            if diagonal is not None:
                s[i][j] = max(s[i-1][j] + down[i-1][j],
                              s[i][j-1] + right[i][j-1],
                              s[i-1][j-1] + diagonal[i-1][j-1])
                if s[i][j] == s[i-1][j-1] + diagonal[i-1][j-1]:
                    b[i][j] = "↘"

            else:
                s[i][j] = max(s[i-1][j] + down[i-1][j],
                              s[i][j-1] + right[i][j-1])

            if s[i][j] == s[i-1][j] + down[i-1][j]:
                b[i][j] = "↓"
            if s[i][j] == s[i][j-1] + right[i][j-1]:
                b[i][j] = "→"

    return s, b


class Node:
    """ Custom class for networkx-nodes with same label and different hash value """
    def __init__(self, cords, label):
        self.label = str(label)
        self.cords = cords

    def __str__(self):
        return self.label

    def __hash__(self):
        return hash(self.cords)


@exception_handler("Matrix dimensions do not match!", errors=IndexError)
def print_graph(s, b, down, right, diagonal=None):
    """ plotting ndarray from dynamic programming algorithm with matpotlib """
    blue = "#b3b3cc"
    red = "#cc0000"
    g = nx.DiGraph()
    for cords, label in np.ndenumerate(s):
        (d, r) = cords
        cords = (r, d * -1)  # if y coordinates negative -> 0,0 in upper left corner
        g.add_node(Node(cords, label), pos=cords)
    pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos, node_size=400, node_color=blue)

    for i, x in np.ndenumerate(down):
        (d, r) = i
        d, r = r, d * -1
        u = [k for k, v in pos.items() if v == (d, r)][0]
        w = [k for k, v in pos.items() if v == (d, r-1)][0]
        g.add_edge(u, w, label=x, color=blue, width=2.0)

    for i, x in np.ndenumerate(right):
        (d, r) = i
        d, r = r, d * -1
        u = [k for k, v in pos.items() if v == (d, r)][0]
        w = [k for k, v in pos.items() if v == (d+1, r)][0]
        g.add_edge(u, w, label=x, color=blue, width=2.0)

    if diagonal is not None:
        for i, x in np.ndenumerate(diagonal):
            (d, r) = i
            d, r = r, d * -1
            u = [k for k, v in pos.items() if v == (d, r)][0]
            w = [k for k, v in pos.items() if v == (d+1, r-1)][0]
            g.add_edge(u, w, label=x, color=blue, width=2.0)

    def backtrack(n, m):
        """ recursive backtracking from 'b'-array changing edge-color of path """
        if b[n][m] == "→":
            this_n, this_m = m, n * -1  # flip coordinates
            next_n, next_m = this_n - 1, this_m
            this_id = [k for k, v in pos.items() if v == (this_n, this_m)][0]
            next_id = [k for k, v in pos.items() if v == (next_n, next_m)][0]
            g[next_id][this_id]["color"] = red
            g[next_id][this_id]["width"] = 4.0
            backtrack(n, m-1)

        elif b[n][m] == "↓":
            this_n, this_m = m, n * -1
            next_n, next_m = this_n, this_m + 1
            this_id = [k for k, v in pos.items() if v == (this_n, this_m)][0]
            next_id = [k for k, v in pos.items() if v == (next_n, next_m)][0]
            g[next_id][this_id]["color"] = red
            g[next_id][this_id]["width"] = 4.0
            backtrack(n-1, m)

        elif b[n][m] == "↘":
            this_n, this_m = m, n * -1
            next_n, next_m = this_n - 1, this_m + 1
            this_id = [k for k, v in pos.items() if v == (this_n, this_m)][0]
            next_id = [k for k, v in pos.items() if v == (next_n, next_m)][0]
            g[next_id][this_id]["color"] = red
            g[next_id][this_id]["width"] = 4.0
            backtrack(n-1, m-1)

    backtrack(n-1, m-1)
    labels = nx.get_edge_attributes(g, "label")
    edges, widths = zip(*nx.get_edge_attributes(g, 'width').items())
    edges, colors = zip(*nx.get_edge_attributes(g, 'color').items())
    nx.draw_networkx_edges(g, pos, alpha=0.5, edgelist=edges, edge_color=colors, width=widths,
                           arrows=False)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=6, rotate=False)
    nx.draw_networkx_labels(g, pos, font_size=6, font_family='sans-serif')
    plt.show()


@exception_handler("Input data corrupted!", errors=(ValueError,))
def load_from_string(string):
    """ string to numpy ndarray """
    np_array = np.loadtxt(StringIO(string.split("\n", 1)[-1]), ndmin=2)

    return np_array


def extant_file(f):
    """    'Type' for argparse - checks if file exists without opening it. """
    if not os.path.isfile(f):
        raise argparse.ArgumentTypeError("{} does not exist".format(f))

    return f

parser = argparse.ArgumentParser(description="Manhattan tourist problem")
parser.add_argument("-i", "--input", dest="filename", required=True, type=extant_file,
                    help="input file with at least two matrices separated with '---'",
                    metavar="FILE")
args = parser.parse_args()

with open(args.filename, "r") as input_handle:
    matrix_list = [m.strip() for m in input_handle.read().split("---") if m.strip() != ""]

    down = load_from_string(matrix_list[0])
    right = load_from_string(matrix_list[1])

    n = down.shape[0] + 1
    m = right.shape[1] + 1

if len(matrix_list) == 2:
    s, b = manhattan_tourist(n, m, down, right)
    print_graph(s, b, down, right)

    print("maximum score is: {}".format(str(s[n - 1][m - 1])))

elif len(matrix_list) == 3:
    diagonal = load_from_string(matrix_list[2])
    try:
        assert diagonal.shape == (down.shape[0], right.shape[1])
    except AssertionError:
        print("Dimensions of diagonal matrix do not match!")
        exit()
    s, b = manhattan_tourist(n, m, down, right, diagonal=diagonal)
    print_graph(s, b, down, right, diagonal=diagonal)

    print("maximum score is: {}".format(str(s[n - 1][m - 1])))

else:
    print("No valid input format!")
