#!/usr/bin/env python                                                           
import optparse
import sys
import string
from collections import defaultdict
import operator

lexGerDic = defaultdict(lambda: defaultdict(float))
lexGerCountDic = defaultdict(int)
file = open('EM-output.txt', 'r')
print 'open Dic'
for line in file:
    list = line.split('|||')
    lexGerDic[list[0]][list[1]] = float(list[2])
file.close()
print 'close Dic'
tupleList = []

def splitPairs(filename):
    index = 0
    for line in open(filename, "r"):
        sen_list = line.split("|||")
        genS = sen_list[0].strip()
        enS = sen_list[1].strip()
        tupleList.append((genS, enS))
        index += 1
print 'get pairs'
splitPairs("temp.txt")     
print 'done pairs'
neighbors = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]


def decode(tList):
    allout = open('output-fixed-thresh.txt', 'w')
    for i in xrange(len(tList)):
        printers=[]
        union = []
        (gs, es) = tList[i]
        glist = gs.split()
        elist = es.split()
        gAlignToE = []
        for gindex in xrange(len(glist)):
            gword = glist[gindex]
            tempEword = elist[0]
            tempMaxIndex = 0
            tempMax = lexGerDic[gword][tempEword]
            for eindex in xrange(1,len(elist)):
                eword = elist[eindex]
                if (lexGerDic[gword][eword] > tempMax):
                    tempMaxIndex = eindex
                    tempMax = lexGerDic[gword][eword]
            #if (tempMax > 0.08):
            union.append((gindex,tempMaxIndex))
            gAlignToE += [(gindex,tempMaxIndex)]
        eAlignToG = []
        for eindex2 in xrange(len(elist)):
            eword2 = elist[eindex2]
            tempGword = glist[0]
            tempGMaxIndex = 0
            tempGMax = lexGerDic[tempGword][eword2]
            for gindex2 in xrange(1, len(glist)):
                gword2 = glist[gindex2]
                if (lexGerDic[gword2][eword2] > tempGMax):
                    tempGMaxIndex = gindex2
                    tempGMax = lexGerDic[gword2][eword2]
            if (tempGMaxIndex,eindex2) not in union:
                union.append((tempGMaxIndex,eindex2))
            eAlignToG += [(tempGMaxIndex,eindex2)]
        
        #getting the interception
        inter = []
        for allA in eAlignToG:
            if allA in gAlignToE:
                inter += [allA]
        printers.extend(inter)

        alignE = []
        alignG = []
        for ea in printers:
            alignG += [ea[0]]
            alignE += [ea[1]]
        #get list of alignments printers
        for gi in xrange(len(glist)):
            for ei in xrange(len(elist)):
                if (gi,ei) in printers:
                    for direction in neighbors:
                        (newg, newe) = (direction[0] + gi, direction[1]+ei)
                        if (((newg not in alignG) or (newe not in alignE))
                            and ((newg, newe) in union)):
                            printers.append((newg,newe))
                            if (newg not in alignG):
                                alignG += [newg]
                            if (newe not in alignE):    
                                alignE += [newe]
        #try to implement final but does not work so commented out
        #for gi2 in xrange(len(glist)):
        #    for ei2 in xrange(len(elist)):
        #        if (((gi2 not in alignG) or (ei2 not in alignE)) 
        #                        and ((gi2, ei2) in union)):
        #            printers.append((gi2, ei2))
        #            if (gi2 not in alignG):
        #                alignG += [gi2]
        #            if (ei2 not in alignE):
        #                alignE += [ei2]
        prints = ''
        for each in printers:
            prints += "%d-%d " % (each[0], each[1])
        allout.write(prints + '\n')
    allout.close()
    return 42

print decode(tupleList)