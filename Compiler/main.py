import sys


column = 0
init = 0
prox = 0


for x in sys.argv:
    print(x)

file = open(sys.argv[1],'r')

buff1 = file.read(512)
buff1 = repr(buff1)

for x in buff1:
    print(x,end='')


