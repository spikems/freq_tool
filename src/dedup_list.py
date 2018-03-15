#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import simhash
import jieba

def compute(text):
    """
        compute hash for a document by shingles
    """
    #tokens = re.split(r'\W+', text)
    tokens = text.split()

    #logger.debug('%s', ''.join(tokens[:5]))

    phrases = (' '.join(phrase) for phrase in simhash.shingle(tokens, 4))
    #logger.debug('%s', [x for x in phrases])

    hashes = map(simhash.unsigned_hash, phrases)
    return simhash.compute(hashes)

sentence = ['我们 都是 好孩子','我们 都是 孩子','a b c d e f','a b c d e f']
removelist = []
grplist = []
data_h = []  #list of hash val ,所有的hash值
duphash = {} #hash ==> set()
linecnt = 0
index = {} #hash val ==> hash id
data_v = {} #line_id ==>data

for line in sentence:
    hash = compute(line)
    data_h.append(hash)
    if hash in index:
        if hash in duphash:
            duphash[hash].append(linecnt)
        else:
            duphash[hash] = [index[hash]]
            duphash[hash].append(linecnt)
    else:
        index[hash] = linecnt
    data_v[linecnt] = line
    linecnt +=1

print 'duphash',duphash
for key in duphash.keys():
    ids = duphash[key]
    removelist.extend(ids[1:])
    grplist.append(ids)

b=4
k=3
matches = simhash.find_all(data_h, b, k)

marks = {}  # lineid -> groupid
grpindex = {}  # groupid -> [lineids]
groupid = 0

for A, B in matches:
    grpidA, grpidB = -1, -1
    if index[A] in marks:
        grpidA = marks[index[A]]
    if index[B] in marks:
        grpidB = marks[index[B]]
    if grpidA == -1 and grpidB == -1:
        marks[index[A]] = groupid
        marks[index[B]] = groupid
        grpindex[groupid] = set([index[A], index[B]])
        groupid += 1
    elif grpidA == -1:
        marks[index[A]] = grpidB
        grpindex[grpidB].add(index[A])
    elif grpidB == -1:
        marks[index[B]] = grpidA
        grpindex[grpidA].add(index[B])
    else:
        # merge two old groups
        for lid in grpindex[grpidB]:
            marks[lid] = grpidA
            grpindex[grpidA].add(lid)
        grpindex[grpidB].clear()


linecntx = 0
for grp in grpindex.keys():
    if grpindex[grp]:
        ids = [lid for lid in grpindex[grp]]
        ids = sorted(ids, reverse = True)

        linecntx += len(ids[1:])
        #output the first one
        removelist.extend(ids[1:])
        grplist.append(ids)
print 'grplist', grplist

#out put final result
remove = set(removelist)
for lid in range(linecnt):
    if lid not in remove and lid in data_v:
        print data_v[lid]

for grp in grplist:
    if len(grp) > 1:
        print grp
    else:
        print grp[0]










