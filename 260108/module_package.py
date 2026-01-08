# .py 내부에 구현된 기능들을 module라고 하고, 그리고 module들을 묶인 그룹을 package라 한다. 
# package 와 module의 집합체를 ilbrary라고 한다.


import random  # module를 가지고 와서 사용하는 방법 import 키워드를 이용하여 사용하고자 하는 module 명을 입력해준다.
# 이후 random module 의 기능을 사용가능하다.
# random module의 기능을 사용하기 위해서 항상 random.{기능명} 을 작성해줘야 하는데 별칭(alias) 지정이 가능하다.
# alias 지정을 as 키워드로 가능하며 
# import random as rd 형식으로 지정 가능하다. 이후 rd.{기능명} 으로 사용이 가능하다.


# 만약 모듈의 전체 기능이 아니라 특정 기능만 가지고 와서 사용하고 싶은경우
from random import shuffle # from {module 명} import {기능 명} 
# 이때 주위 할 점은 이전에 동일 이름으로 구현된 요소가 있다면 덮어 쓰기가 되니 주위가 필요하다. 이를 방지하기 위해서 기능도 alias로 별칭을 지정하여 사용한다.
# from random import shuffle as sf 로 별칭을 주고 이후로 sf로 사용이 가능하다.
# 별칭 alias 명은 임의로 지정 할 수 있지만 관례로 전해 내려오는 별칭 명으로 사용하는게 좋다. (다른 사람이 내 코드를 보았을때 유추가 가능하다.)

# 파이썬 데이터 분석 module 중 자주 사용되는 모듈 (범용적으로 사용되는 별칭 명)
# import numpy as np -> 과학 계산을 위한 패키지
# import pandas as pd -> 데이터 분석을 할 때 가장 많이 쓰이는 module
# import matplotlib.pypiot as plt -> 시각화를 위한 module
# import seaborn as sns -> 시각화를 위한 module, matplotlib 을 더 쉽게 사용할 수 있도록 도와주는 패키지
# import random as rd -> 난수 생성 관련 모듈