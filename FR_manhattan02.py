#!/usr/bin/env python
import sys
import os
import csv
#import matplotlib.pyplot as plt
from datetime import datetime
import re
import string

#open file
#textfile = open("/home/ruge/Documents/ALGO/NeedlemannWunsch/rm15_11", 'r')
textfile = open("./rdm50/rmd50_11", 'r')
#read file into lists
gright=[]
gdown=[]
gdiag=[]
switch="down"
for line in textfile:
    if line.startswith(' ') and switch == "down":
        gdown.append(line.split())
    if line.startswith("---")and switch == "down":
        switch="right"

    if line.startswith(" ") and switch == "right":
        gright.append(line.split())

    if line.startswith("---")and switch == "down":
        switch="diag"

    if line.startswith(" ") and switch == "diag":
        gright.append(line.split())
print("gdown")
for line in gdown:
	print(line)

print("#################################################################")
print("gright")
for line in gright:
	print(line)

print("gdiag")
for line in gdiag:
	print(line)

#initialize matrix
mati=[[0] * (len(gdown)+1) for x in range(len(gright))]
print("Length of matrix "+str(len(gdown)+1)+" * "+str(len(gright)))
nright=int(len(gdown)+1)
ndown=int(len(gright))

#fill up first row - mati[0][i]
for i in range(len(mati[0])):
    if i == 0:
        mati[0][i] = 0
    else:
        mati[0][i] = round(float(mati[0][i-1]) + float(gright[0][i-1]),2)

#fill up first column mati[j][0]
for j in range(len(mati[0])):
    if j == 0:
        #print("ll")
        mati[j][0]= 0
    else:
        #print(j)
        mati[j][0]= round(float(mati[j-1][0]) + float(gdown[j-1][0]), 2)


def readFileAndReturnMatrix(file):
    textfile = open(file, 'r')


#print matrix with first row and column filled up
#for row in mati:
#	print(row)

#fill rest of matrix
print(range(nright))
for i in range(nright):
#	print("i")
#	print(1)
	for j in range(ndown):
		if i==0 or j==0:
			pass
		else:
#			print("j")
#			print(j)
			mati[j][i]=round(max(mati[j-1][i] + float(gdown[j-1][i]) , mati[j][i-1] + float(gright[j][i-1])),2)
print(gdown[0][1])
print(gright[1][0])

#print complete matrix
for i in range(len(mati)):
#   #for j in range(len(gdown[i])):
    print(mati[i])

textfile.close()

print("GUGU")
