#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as pl
import sys
import codecs

#tsvデータとgraph.pngというファイルからレポートのtexソースを出力する
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
    print tmp
    data.append(tmp.split("\t"))
    

fout = codecs.open("./final_report.tex","w")
rs = "r"*(1+len(data[0]))
fout.write("\\documentclass[a4j,12pt,twoside]{tetsujsarticle}\n\\usepackage[top=30truemm,bottom=30truemm,left=25truemm,right=25truemm]{geometry}\n\\usepackage{tetsuryoku}\n\\usepackage{booktabs}\n")
fout.write("\\begin{document}\n\\title{実験レポート\\\\Open Hack Day 3}\n\\author{UT-HACKs}\n\\maketitle")
fout.write("\\begin{center}\n")
fout.write("\\img<0.45>{application.macosx/fig/graph.png}\\\\\n")
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
fout.write("\\end{center}\n")
fout.write("\\section{特色}\n Camiappで取り込んだデータが10秒で \\TeX の表とグラフに！")
fout.write("\\end{document}")
fout.close()
fin.close()
