'''
Created on Sep 29, 2015

@author: olivier
Program to generate random names with a given number of letters
'''
import random
import string
import enchant


alpha = list(string.lowercase)
voyels = ['a','e','i','o','u']
d = enchant.Dict("en_US")
for i in voyels:
    alpha.remove(i)
def generate_name(n):
    name = ''
    for i in range(1,n+1):
        if i % 2 != 0:
            name += alpha[int(random.random()*len(alpha))]
        else:
            name += voyels[int(random.random()*len(voyels))]
        if i == 1:
            name = name.upper()
    if d.check(name):
        print name
            
for i in range(30000):
    generate_name(6)