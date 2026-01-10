import os
import sys

def dirSearch(startPath):
  filenames = os.listdir(startPath) # 시작 dir path 를 전달 하면 기준으로 하위 directory list 를 반환한다.
  print(type(filenames)) # list 출력
  for filename in filenames:
    ext = os.path.splitext(filename)[-1] # splitext() 를 사용하면 파일명 과 확장자를 tuple 형식으로 반환해준다. a.txt => ('a', '.txt') 거기에 [-1] 해주면 list 마지막 요소가 선택이 되어 ext에는 확장자만 담기게 된다.
    if ext == '.py':
      full_filePath = os.path.join(startPath, filename)
      print(full_filePath)

# dirSearch('/Users/dymacpro/myProject/myDev/My/goorm-ai-study/260110')




def treeDirSearch(startPath):
  filenames = os.listdir(startPath)
  for filename in filenames:
    full_filename = os.path.join(startPath, filename)
    if os.path.isdir(full_filename):
      treeDirSearch(full_filename)
    else:
      ext = os.path.splitext(full_filename)[-1]
      if ext == '.py':
        print(full_filename)


if __name__ == '__main__': # 매직 메소드 __name__ 은 작성한 .py 내부에서는 __name__ == __main__ 으로 나오고, .py 파일을 다른 파일에서 import 시켜 사용하는 
  # 경우 해당 파일 이름이 나오게 된다. 즉 .py 내부에서만 동작시키고 싶은 실행문이 있다면 if __name__ == '__main__' 검사하여 일치하는 경우에만 실행되게 한다.
  if len(sys.argv) != 2:
    print('사용법: python3 07_sub_dir_search.py <검색할_디렉터리>')
    sys.exit()

  search_dir = sys.argv[1]
  if os.path.exists(search_dir): # os.path.exists() 메소드는 전달되는 위치에 directory 가 존재 하는지 확인하는 메소드
    treeDirSearch(search_dir)
  else:
    print(f"검색한 Directory는 없습니다. {search_dir}")

# treeDirSearch('/Users/dymacpro/myProject/myDev/My/goorm-ai-study')