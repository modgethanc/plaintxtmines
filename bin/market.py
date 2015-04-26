#!/usr/bin/python

def toKyno(res): # takes in a resource line, returns kynoti, taken, and leftover

  kynoti = 0
  out = [0,0,0,0,0,0,0,0,0]
  print res
  i = 0
  bump = 0
  while i < 8:
    mangle = []
    mangle.extend(res)
    print mangle
    if change(i, mangle) != 8:
      i += 1
    else:
      bump, out[i] = divmod(int(res[i])+bump,8)
      print bump
      if i < 7:
        bump += int(res[i+1])
      i += 1

  #print resources
  kynoti = out.pop(8)
  return kynoti, out, res

def change(i, res):
  #print res
  if i == 7:
    if int(res[i])/8 > 0:
    #  return i, True
      return i+1
    else:
    #  return i, False
      return i
  elif int(res[i])/8 == 0:
    return i
  else:
    res[i+1] += int(res[i])/8
    if int(res[i+1])/8 == 0:
      #return i, False
      return i
    else:
      #print res
      return change(i+1, res)
