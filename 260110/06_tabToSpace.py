import sys

src = sys.argv[1]
dit = sys.argv[2]

f = open(src)
tab_txt = f.read()
f.close()
  
space_txt = tab_txt.replace("\t"," "*4);

f = open(dit, 'w')
f.write(space_txt)
f.close()
