#!/usr/bin/python

import os
import random
import gibber

def newEmpress():
    empressfile = open('../data/empress.txt', 'w+')

    empressfile.write('0\n') # 0 next grovel window
    empressfile.write("0,0,0,0,0,0,0,0\n") # 1 tithed total
    empressfile.write('\n') # 2 favorite

### output

def openEmpress():
    empressfile = open('../data/empress.txt', 'r')
    empressdata = []
    for x in empressfile:
        empressdata.append(x.rstrip())
    empressfile.close()

    return empressdata

def getGrovel():
    return openEmpress()[0].rstrip()

def getTithed():
    return openEmpress()[1].rstrip().split(',')

def getFavorite():
    return openEmpress()[2].rstrip()

### input

def writeEmpress(empressdata):
    empressfile = open('../data/empress.txt', 'w')
    for x in empressdata:
        empressfile.write(str(x) + "\n")
    empressfile.close()

def updateGrovel(time):
    empressdata = openEmpress()
    empressdata[0] = time
    writeEmpress(empressdata)

    return time

def acceptTithe(res):
    held = getTithed()

    i = 0
    for x in res:
        r = int(held[i]) + int(x)
        held[i] = str(r)
        i += 1

    empressdata = openEmpress()
    empressdata[1] = ','.join(held)
    writeEmpress(empressdata)

    return res

def removeTithe(res):
    held = getTithed()

    i = 0
    for x in res:
        r = int(held[i]) - int(x)
        held[i] = str(r)
        i += 1

    empressdata = openEmpress()
    empressdata[1] = ','.join(held)
    writeEmpress(empressdata)

    return res

def setFavorite(player):
    empressdata = openEmpress()
    empressdata[2] = player
    writeEmpress(empressdata)
    
    return player

### actions

def processPayment(res):
  pay = [0,0,0,0,0,0,0,0]
  i = 7

  while i >= 0:
    index, amount = payout(i,res[i])
    pay[index] += amount
    i -= 1

  return pay

def payout(index, amount):
  held = getTithed()

  if int(held[index]) >= int(amount):
    #print index, amount
    return index, int(amount)
  elif index == 0:
    return 0, 0
  else:
    return payout(index-1, amount*8)

def speak():
    return gibber.sentence()

#if not os.path.isfile("../data/empress.txt"):
#    newEmpress()
