#!/usr/bin/python
#-*- coding: utf-8 -*-

import types

def fib():
 a = 1
 b = 2
 yield a
 yield a
 yield b
 while True:
  yield a+b
  a,b = b,a
  b = a+b

def fib2():
 a,b = 1,1
 while 1:
  yield a
  a, b = b, a+b

if type(fib()) == types.GeneratorType:
 print "fib() is generator)"
 counter=0
 for n in fib():
  print n
  counter +=1
  if counter == 10:
   break


