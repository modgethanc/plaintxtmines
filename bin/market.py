#!/usr/bin/python

def toKyno(resources):

  kynoti = 0
  resources.append(0)

  i = 0
  while i < 8:
    bump, resources[i] = divmod(int(resources[i]),8)
    bump += int(resources[i+1])
    resources[i+1] = bump
    i += 1

  print resources
  kynoti = resources.pop(8)
  return kynoti, resources

def kynoSum(kynoti, res):
  return
