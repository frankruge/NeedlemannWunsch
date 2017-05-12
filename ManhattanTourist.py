import sys
import re

file = sys.argv[1]

def (file):
    gright = []
    gdown = []
    switch = "down"
    for line in textfile:
        if line.startswith(' ') and switch == "down":
            gdown.append(line.split())
        if line.startswith("---") and switch == "down":
            switch = "right"

        if line.startswith(" ") and switch == "right":
            gright.append(line.split())
