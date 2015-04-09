# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
import sys
import codecs

#tsvデータからレポートのtexソースを出力する
argvs = sys.argv
argc = len(argvs)
if (argc != 2):
    print "not collect"
    quit()

fin = codecs.open(argvs[1],"r")
data = []

for line in fin:
    if line[-1] == "\n":
        tmp = line[:-1]
    else:
        tmp = line
    data.append(tmp.split("\t"))
    

fout = codecs.open("./result.tex","w")
rs = "r"*(1+len(data[0]))
fout.write("\\begin{tabular}{"+rs+"}\\toprule \n")
for count,line in enumerate(data):
    if(count != 0):
        fout.write(str(count))
        fout.write("&")
    else:
        fout.write("No.")
        fout.write("&")
        
    for i in range(len(line)):
        fout.write(line[i])
        if(i != len(line)-1):
            fout.write("&")
    fout.write("\\\\\n")
    if(count == 0):
        fout.write("\\midrule\n")

fout.write("\\bottomrule\n")
fout.write("\\end{tabular}\n")
fout.close()
fin.close()
