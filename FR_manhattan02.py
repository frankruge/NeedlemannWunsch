#!/usr/bin/env python
import sys
import os
import csv
import string

#open file
#textfile = open("/home/ruge/Documents/ALGO/NeedlemannWunsch/rm15_11", 'r')
textfile = open("./rdm50/rmd50_11", 'r')
#read file into lists
gright=[]
gdown=[]
gdiag=[]
switch = "down"

#for line in textfile:
#    if line.startswith('G'):
#        print(line)



for line in textfile:
    if line.startswith('  ') and switch == "down":
        gdown.append(line.strip().split())
        #print(switch)
    if line.startswith("---")and switch == "down":
        switch = "right"
        continue
        #print(switch)
    if line.startswith('  ') and switch == "right":
        gright.append(line.strip().split())
        #print(switch)
    if line.startswith("---")and switch == "right":
        switch = "diag"
        continue
        #print(switch)
    if line.startswith('  ') and switch == "diag":
        gdiag.append(line.strip().split())
        #print(switch)
    if line.startswith('G'):
        continue

print("gdown")
for line in gdown:
	print(line)

print("#################################################################")
print("gright")
for line in gright:
	print(line)
print("#################################################################")
print("gdiag")
for line in gdiag:
	print(line)


def manhattan_tourist(down, right, diag):
    #matrix
    m_down=[][]
    for i in range(len(down)):
        for j in range(len(down[i])):
            #print(down[i][j])
            m_down[i][j] = float(down[i][j])
    return m_down

a=manhattan_tourist(down=gdown, right=gright, diag=gdiag)
print(a)

'''
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
'''