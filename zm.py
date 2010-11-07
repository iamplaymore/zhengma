#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        zm.py
#created:        2010-11-07

import re

def init_words():
    'open file and get pure chinese words, reserving their order'
    f=open("char_word.txt")
    words=f.readlines() 
    for i in range(len(words)):
        words[i]=words[i].strip()
    f.close()
    return words

def init_code():
    '''get code for each character; each code is 2 byte long'''
    f=open("zm6char.txt")
    words=f.readlines()
    chars={}
    for w in words:
        w=w.strip()
        char=w.split(';')[0]
        code=w.split(';')[-1]
        chars[char]=code
    return chars

def init_stad():
    words=[]
    codes=[]
    f=open("sz.txt") 
    lines=f.readlines() 
    f.close()

    for line in lines:
        word,code=line.split()
        words.append(word)
        codes.append(code)

    return (words, codes)

       

print "init words list"
char_words=init_words()

print "init gocima list"

goucima=init_code()

print "init standard list" 
(g_words, g_codes)=init_stad()


def byte2words(s):
    '''split utf8 chinise string to single chars'''
    words=[]
    for i in range(len(s)/3):
        char=s[i*3:(i+1)*3]
        words.append(char)
    return words
 
def gen_code(words):
    '''generate zhengma code for a given chinese words, the length of which is more than 2 chars'''
    chs=byte2words(words)
    length=len(chs)
    if length<=1:
        return ""
    if length==2:
        try: return goucima[chs[0]][:2]+goucima[chs[1]][:2]
        except: print words, "2s error!"

    elif length==3:
        try: return goucima[chs[0]][0]+goucima[chs[1]][:2]+goucima[chs[2]][:2]
        except: print words, "3s error!"

    elif length==4:
        try: return goucima[chs[0]][0]+goucima[chs[1]][0]+goucima[chs[2]][0]+goucima[chs[3]][:2]
        except: print words, "4s error!"
    elif length>=5:
        try:
            return goucima[chs[0]][0]+goucima[chs[1]][0]+goucima[chs[2]][0]+goucima[chs[3]][0]+goucima[chs[4]][0]
        except: print words, "5s error!"


def search_standard(word):
    word=word.strip()
    result=[]
    cnt=g_words.count(word)
    if not cnt:
        return [] 
    index=0
    while True:
        
        try:
            index=g_words.index(word, index)
            result.append(g_codes[index])
            index+=1
            
        except:
            break

    if len(result)<=1:
        return result
    else:
        result=list(set(result))
        result.sort(cmp=lambda x, y: len(x)-len(y))
        return result

def search_all(word):
    
    code=search_standard(word)
    gen=gen_code(word)
    if gen:
        if gen not in code:
            code.append(gen)
    return code

length=len(char_words)
print "processing %d words..." % length
count=0
output=open("myzm.txt","w")
for word in char_words:
    count+=1

    if count % 1000 ==0:
        print "%d of %d...%d%%..." % (count, length, int(100*count/length))

    code=search_all(word)
    for i in range(len(code)):
        output.write("%s %s\n" % (code[i], word))
output.close()
    
