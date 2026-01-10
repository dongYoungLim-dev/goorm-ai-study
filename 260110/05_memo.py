import sys

print(sys.argv)

option = sys.argv[1]

# print(option)
# print(memo)

if option == '-a':
  memo = sys.argv[2]

  f = open('memo.txt', 'a');
  f.write(memo)
  f.write('\n')
  f.close()
elif option == '-v':
  f = open('memo.txt')
  readMemo = f.read()
  f.close()
  print(readMemo)