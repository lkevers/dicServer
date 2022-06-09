#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# dicServer - a multithreaded socket server allowing to query word lists
#
# Author :  Laurent Kevers - University of Corsica
#           kevers_l@univ-corse.fr
#
# This script is a version using the 'multiprocessing' python package
#

# 
# Copyright University of Corsica -- Laurent Kevers (2022)
# 
# kevers_l@univ-corse.fr
# 
# This software is a computer program whose purpose is the querying of word lists.
# 
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and, more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#



import socket, multiprocessing

import time
import sys
import json
import logging

logging.basicConfig(filename='dicServer.log', level=logging.DEBUG)


def extractUnitexForm (line) :
    elems=line.split(',')
    return elems[0]

# Initialisation : loads dictionaries into memory
def load_dictionaries():

    unitex="dic/unitex-lingua"
    languages={
            "cos":"dic/corsican/BibleBilingueCorseFrancais2015_co_TEI_TXT.dic",
            "deu":"%s/de/Dela/dela_utf8.dic"%unitex,
            "eng":"%s/en/Dela/dela-en-public_utf8.dic"%unitex,
            "fra":"%s/fr/Dela/Dela_fr_utf8.dic"%unitex,
            "ita":"%s/it/Dela/mini-delaf_utf8.dic"%unitex,
            "nld":"dic/opentaal-wordlist/full.txt",
            "por":"%s/pt-PT/Dela/Delaf_V2_utf8.dic"%unitex,
            "ron":"dic/romanian/ELRC/Romanian_Wordlist_dict.ro1.sortedU.txt",
            "spa":"%s/es/Dela/delaf_utf8.dic"%unitex
    }

    src_licences={
        "cos":"'A Sacra Bìbbia' corpus (CC BY-NC-SA 4.0)",
        "deu":"Unitex Lexical Resources (LGPLLR)",
        "eng":"Unitex Lexical Resources (LGPLLR)",
        "fra":"Unitex Lexical Resources (LGPLLR)",
        "ita":"Unitex Lexical Resources (LGPLLR)",
        "nld":"Opentaal wordlist (Revised BSD / CC BY 3.0)",
        "por":"Unitex Lexical Resources (LGPLLR)",
        "ron":"Romanian – English parallel wordlists. Created for the European Language Resources Coordination Action (ELRC) by Tufis Dan, Institutul de Cercetari pentru Inteligenta Artificiala 'Mihai Draganescu', Academia Romana (CC-BY 4.0)",
        "spa":"Unitex Lexical Resources (LGPLLR)"
    }
    
    dics={
        "cos":set(),
        "deu":set(),
        "eng":set(),
        "fra":set(),
        "ita":set(),
        "nld":set(),
        "por":set(),
        "ron":set(),
        "spa":set()
    }
    
    totMywords=0
    for lg,path in languages.items() :
        mywords=set()
        if len(path)>0 :
            with open(path) as word_file:
                if "unitex" in path:
                    mywords = set(extractUnitexForm(word).strip().lower() for word in word_file)
                else:
                    mywords = set(word.strip().lower() for word in word_file)
                print("Add %s dictionary... %s elements from %s -- %s"%(lg,len(mywords),path,src_licences[lg]))
                dics[lg]=mywords
        totMywords+=len(mywords)
    print("Dictionaries contain %s entries"%totMywords)

    return dics


# For the word given as parameter
# Returns 'True' if it is present in at least one dictionary
# Else returns 'False'
# Result is returned in a json object
def is_word (word):
    #subprocess.Popen(['notify-send', "is_word %s"%word])
    res=False
    for lg,dic in dics.items():
        if word.strip().lower() in dic :
            res=True
            break
    return json.dumps(res)


# For a word and a language
# Returns 'True' if this word exists in the language dictionary
# Else returns 'False'
# Result is returned in a json object
def is_lg_word (word, lg):
    return json.dumps(word.strip().lower() in dics[lg])


# For a word
# Returns a list with all languages for which the word exists in the language dictionary.
# If the word doesn't exist in any dictionary, returns an empty list
# Result is returned in a json object
def word_languages (word):
    res=list()
    for lg,dic in dics.items():
        if word.strip().lower() in dic :
            res.append(lg)
    return json.dumps(res)


# For a word, and a reduced set of possible languages
# Returns a list with all languages for which the word exists in the language dictionary.
# If the word doesn't exist in any dictionary, returns an empty list
# Result is returned in a json object
def word_possibleLanguages (word, possibleLg):
    res=list()
    for lg in possibleLg:
        if lg in dics:
            dic=dics[lg]
            if word.strip().lower() in dic :
                res.append(lg)
    return json.dumps(res)



def handle(conn, address):
    with conn:
        buff = conn.recv(2048)
        msgu = buff.decode('utf-8').strip()
        logging.debug("Msg: %s"%msgu)
        method="is_word"
        if ("::" in msgu) :
            params=msgu.split("::")
            method=params[0]
            word=params[1]
        else :
            word=msgu
        result=""
        if method == "is_word" :
            result=is_word(word)
        elif method == "is_lg_word" :
            if len(params)==3:
                lg=params[2]
                if lg in dics :
                    result=is_lg_word(word,lg)
                else :
                    result="err_noSuchLg"
            else :
                result="err_wrongNbParams"
        elif method == "word_languages" :
            result=word_languages(word)
        elif method == "word_possibleLanguages" :
            if len(params)==3:
                lgs=params[2].split(",")
                knownLgs=True
                for lg in lgs :
                    if lg not in dics :
                        knownLgs=False
                if knownLgs==True:
                    result = word_possibleLanguages(word,lgs)
                else :
                    result = "err_noSuchLg"
            else :
                result="err_wrongNbParams"
        else:
            result="err_noSuchMethod"
        logging.debug("Res: %s"%result)
        conn.sendall(f"{result}".encode('utf-8'))



host = 'localhost'
port = 1112
nb_workers = 10

print ("Starting")
logging.info("Starting")
print("Will listen on %s:%s"%(host, port))
logging.info("Will listen on %s:%s"%(host, port))
dics=load_dictionaries()
logging.info("Dictionaries loaded")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    with multiprocessing.Pool(nb_workers) as pool:
        while True:
            conn, address = s.accept()
            pool.apply(handle, (conn, address))


