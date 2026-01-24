"""
Python 리스트, 튜플, 딕셔너리 중급자 문제 모음
"""

# ============================================
# 문제 1: 학생 성적 관리 시스템
# ============================================
"""
학생들의 성적을 관리하는 시스템을 만들어보세요.

요구사항:
1. 학생 정보는 딕셔너리로 저장 (이름, 학번, 과목별 점수)
2. 여러 학생의 정보를 리스트에 저장
3. 다음 기능들을 구현:
   - 전체 학생의 평균 점수 계산
   - 특정 과목의 전체 평균 계산
   - 평균 점수가 80점 이상인 학생 찾기
   - 학번으로 학생 검색
"""

students = [
    {"name": "김철수", "student_id": "2024001", "scores": {"수학": 85, "영어": 90, "과학": 78}},
    {"name": "이영희", "student_id": "2024002", "scores": {"수학": 92, "영어": 88, "과학": 95}},
    {"name": "박민수", "student_id": "2024003", "scores": {"수학": 75, "영어": 82, "과학": 80}},
    {"name": "최지은", "student_id": "2024004", "scores": {"수학": 88, "영어": 85, "과학": 90}},
]

# 여기에 코드를 작성하세요

# 전체 학생의 평균 값 계산 
def cal_total_average(students):
  # 전체 학생의 배열이 들어와 이중 나는 scores가 필요해
  total_score = 0
  for student in students:
    for value in student['scores'].values():
      total_score += value
  return total_score / len(students)

# 특정 과목의 전체 평균 값 계산
def subject_cal_total_average(students):
  # students 배열에 scores 가 늘어가도 위 함수가 변경 되지 않고 계산이 가능하게 로직 구성
  # scores에 있는 과목별로 각 점수 합계를 저장할 딕셔너리 형태를 만들다.
  subject_score_sum = {}
  for student in students:
    for key in student['scores'].keys():
      # key를 받아서 과목별 점수 합계를 저장하는 딕셔너리를 만들고 싶어.
      # 각 과목의 초기 합계 점수는 0이야.
      subject_score_sum[key] = 0

  # 전달 되는 배열의 값에서 scores 의 key 값과 "subject_score_sum" 딕셔너리의 key 값에 있는지를 비교하여 있다면 값을 합산.
  subject = [key for key in subject_score_sum.keys()]
  for student in students:
    for key in student['scores'].keys():
      if key in subject:
        subject_score_sum[key] += student['scores'][key]


  # 각 과목의 평균 값 구하기
  subject_average = {}
  # print(f"subject_score_sum : {subject_score_sum}")
  for key, value in subject_score_sum.items():
    subject_average[key] = value/len(subject_score_sum)
  

# 평균 점수가 80점 이상인 학생 찾기
def student_average(students):
  reference_value = 80
  pass_student = {}
  for student in students:
    student_score_sum = 0
    for value in student['scores'].values():
      # 학생별로 점수의 합계를 과목 수로 나우어 평균값을 구하고 
      # 이를 reference_value 와 비교하여 높은지 판단한다. 
      # 학생별로 점수를 어떻게 합칠까? 
      student_score_sum += value
    if student_score_sum/len(student['scores']) > reference_value:
      pass_student[student['name']] = student_score_sum/len(student['scores'])
  print (pass_student)

# 학번으로 학생 검색하기
def search_student_numbers(students, std_num):
  for student in students:
    if std_num in student['student_id']:
      print(student)
      


# ============================================
# 문제 2: 쇼핑몰 주문 관리
# ============================================
"""
온라인 쇼핑몰의 주문을 관리하는 시스템을 만들어보세요.

요구사항:
1. 주문 정보는 튜플로 저장 (주문번호, 상품명, 수량, 단가)
2. 여러 주문을 리스트에 저장
3. 다음 기능들을 구현:
   - 각 주문의 총 금액 계산
   - 전체 주문의 총 매출 계산
   - 가장 많이 팔린 상품 찾기
   - 주문번호로 주문 검색
"""

orders = [
    ("ORD001", "노트북", 2, 1200000),
    ("ORD002", "마우스", 5, 25000),
    ("ORD003", "키보드", 3, 80000),
    ("ORD004", "노트북", 1, 1200000),
    ("ORD005", "마우스", 10, 25000),
]

# 여기에 코드를 작성하세요

orders_keys = ['order_id', 'product_name', 'order_count', 'product_price'] # 주문 필드명
# 공통 작업으로 리스트에 저장된 튜플을 가공하여 딕셔너리 형태로 변경한다.
def tuple_to_dict(orders_keys, orders):
  orders_dict = {}
  # orders_keys 와 orders 를 조합하여 {'order_id': "ORD001", ... } 형태로 만들고 싶다.
  for i, order in enumerate(orders):
    orders_dict[i] = dict(list(zip(orders_keys, order)))
  return orders_dict


# 각 주문의 총 금액 계산
def order_total_price(orders, keys):
  new_orders = tuple_to_dict(keys, orders)
  order_total_price = {}
  for order in new_orders.values():
    order_price = order['product_price']*order['order_count']
    order_total_price[order['order_id']] = order_price
  
  return order_total_price
# 전체 주문의 총 매출 계산 
def orders_total_price(orders, keys):
  order_price_info = order_total_price(orders, keys)

  price = [price for price in order_price_info.values()]
  print(f'{sum(price):,}')

# 가장 많이 팔린 상품 찾기
# =================================
# 딕셔너리로 바꾸지 않고 찾으려면? 
# 판매 수가 가장 높은 수를 찾아야 한다. 
# 주문 수량은 항상 index 2번째 있다.
def best_order(orders):
  order_counts = [order[2] for order in orders]
  for order in orders:
    if max(order_counts) == order[2]:
      print(order)

# 주문번호로 주문 검색
def search_order_num(orders, keys, search_num):
  orders_dict = tuple_to_dict(keys, orders)
  for order in orders_dict.values():
    if search_num == order['order_id']:
      print(order)


# ============================================
# 문제 3: 도서관 도서 관리
# ============================================
"""
도서관의 도서 대출 현황을 관리하는 시스템을 만들어보세요.

요구사항:
1. 도서 정보는 딕셔너리로 저장 (제목, 저자, 출판사, 대출여부)
2. 대출 기록은 튜플로 저장 (도서제목, 대출자명, 대출일)
3. 다음 기능들을 구현:
   - 현재 대출 가능한 도서 목록
   - 특정 저자의 도서 목록
   - 가장 많이 대출된 도서 찾기
   - 대출 기록을 날짜별로 그룹화
"""

books = [
    {"title": "파이썬 프로그래밍", "author": "김개발", "publisher": "IT출판사", "available": False},
    {"title": "데이터 분석 입문", "author": "이데이터", "publisher": "과학출판사", "available": True},
    {"title": "머신러닝 기초", "author": "김개발", "publisher": "IT출판사", "available": False},
    {"title": "웹 개발 실전", "author": "박웹", "publisher": "기술출판사", "available": True},
    {"title": "알고리즘 문제해결", "author": "최알고", "publisher": "과학출판사", "available": False},
]

loan_records = [
    ("파이썬 프로그래밍", "홍길동", "2024-01-15"),
    ("머신러닝 기초", "김철수", "2024-01-15"),
    ("파이썬 프로그래밍", "이영희", "2024-01-20"),
    ("알고리즘 문제해결", "박민수", "2024-01-18"),
    ("파이썬 프로그래밍", "최지은", "2024-01-22"),
]

# 여기에 코드를 작성하세요

# 현재 대출 가능한 도서 목록
def is_available_book(books):
  new_books = []
  for book in books:
    if book['available']:
      new_books.append(book)
    
  print(new_books)

# 특정 저자의 도서 목록
def author_books(books):
  new_books = {}
  authors = set([book['author'] for book in books]) # 저자 목록, set을 이용하여 중복값을 제거한다.

  for author in authors:
    # books를 순회하면서 조건식(if)을 통과하는 요소의 'title' 리스트를 담는 list comprehension 
    # 결과 적으로 new_books 에 "저자": [ 저자의 책 목록 ] 형태로 결과가 출력된다.
    new_books[author] = [book_list['title'] for book_list in books if book_list['author'] == author]    
  print(new_books)

# 가장 많이 대출된 도서 찾기
def best_loan_book(loan_records, books):
  loan_book_titles = [title for title, name, date in loan_records]
  loan_count = {}
  for book in books:
    loan_count[book['title']] = loan_book_titles.count(book['title'])

  # 각 책의 대출 수량과, 많이 빌린 수량이 일치하는 항목을 찾아 출력
  max_count = max(loan_count.values())
  for title, count in loan_count.items():
    if count == max_count:
      print(f"가장 많이 대출된 도서 : {title}")  

best_loan_book(loan_records, books)

# 대출 기록을 날짜별로 그룹화 (날짜 기준 대출 기록의 묶음)
def date_loan_records(loan_records):
  date_record = {} 
  for title, name, _date in loan_records:
    date_record[_date] = [title for title, name, date in loan_records if date == _date] 
  print(date_record)

date_loan_records(loan_records)
# ============================================
# 문제 4: 영화 평점 분석
# ============================================
"""
영화 평점 데이터를 분석하는 시스템을 만들어보세요.

요구사항:
1. 영화 정보는 딕셔너리로 저장 (제목, 장르, 개봉년도)
2. 평점은 튜플로 저장 (영화제목, 사용자명, 평점(1-10))
3. 다음 기능들을 구현:
   - 각 영화의 평균 평점 계산
   - 장르별 평균 평점 계산
   - 가장 높은 평점을 받은 영화 찾기
   - 특정 사용자가 평가한 영화 목록
"""

movies = [
    {"title": "인셉션", "genre": "SF", "year": 2010},
    {"title": "다크나이트", "genre": "액션", "year": 2008},
    {"title": "인터스텔라", "genre": "SF", "year": 2014},
    {"title": "어벤져스", "genre": "액션", "year": 2012},
]

ratings = [
    ("인셉션", "user1", 9),
    ("인셉션", "user2", 10),
    ("인셉션", "user3", 8),
    ("다크나이트", "user1", 10),
    ("다크나이트", "user2", 9),
    ("인터스텔라", "user1", 9),
    ("인터스텔라", "user3", 10),
    ("어벤져스", "user2", 8),
    ("어벤져스", "user3", 7),
]

# 여기에 코드를 작성하세요


# ============================================
# 문제 5: 회사 직원 관리
# ============================================
"""
회사의 직원 정보를 관리하는 시스템을 만들어보세요.

요구사항:
1. 직원 정보는 딕셔너리로 저장 (이름, 부서, 직급, 연봉)
2. 프로젝트 참여 기록은 튜플로 저장 (직원이름, 프로젝트명, 참여기간(월))
3. 다음 기능들을 구현:
   - 부서별 평균 연봉 계산
   - 프로젝트에 가장 많이 참여한 직원 찾기
   - 특정 프로젝트에 참여한 직원 목록
   - 직급별 직원 수 계산
"""

employees = [
    {"name": "김대리", "department": "개발팀", "position": "대리", "salary": 45000000},
    {"name": "이과장", "department": "개발팀", "position": "과장", "salary": 55000000},
    {"name": "박차장", "department": "마케팅팀", "position": "차장", "salary": 60000000},
    {"name": "최부장", "department": "개발팀", "position": "부장", "salary": 75000000},
    {"name": "정대리", "department": "마케팅팀", "position": "대리", "salary": 42000000},
]

project_participation = [
    ("김대리", "웹사이트 개편", 6),
    ("이과장", "웹사이트 개편", 8),
    ("김대리", "모바일 앱 개발", 4),
    ("박차장", "브랜드 리뉴얼", 12),
    ("최부장", "웹사이트 개편", 3),
    ("정대리", "브랜드 리뉴얼", 10),
    ("이과장", "모바일 앱 개발", 6),
]

# 여기에 코드를 작성하세요


# ============================================
# 문제 6: 통합 문제 - 온라인 강의 플랫폼
# ============================================
"""
온라인 강의 플랫폼의 데이터를 종합적으로 관리하는 시스템을 만들어보세요.

요구사항:
1. 강의 정보: 딕셔너리 (강의명, 강사명, 카테고리, 가격, 수강생수)
2. 수강 기록: 튜플 (학생명, 강의명, 수강일, 완료여부)
3. 리뷰 정보: 딕셔너리 (강의명, 학생명, 평점, 리뷰내용)
4. 다음 기능들을 구현:
   - 카테고리별 평균 가격
   - 완료율이 80% 이상인 강의 찾기
   - 각 강의의 평균 평점 계산
   - 가장 많은 수강생을 보유한 강사 찾기
   - 특정 학생이 수강한 모든 강의 목록과 총 결제금액
"""

courses = [
    {"name": "파이썬 기초", "instructor": "김강사", "category": "프로그래밍", "price": 50000, "students": 150},
    {"name": "데이터 분석", "instructor": "이강사", "category": "데이터", "price": 80000, "students": 200},
    {"name": "웹 개발", "instructor": "김강사", "category": "프로그래밍", "price": 70000, "students": 180},
    {"name": "머신러닝", "instructor": "박강사", "category": "데이터", "price": 100000, "students": 120},
]

enrollments = [
    ("학생1", "파이썬 기초", "2024-01-01", True),
    ("학생1", "데이터 분석", "2024-01-05", True),
    ("학생2", "파이썬 기초", "2024-01-02", True),
    ("학생2", "웹 개발", "2024-01-10", False),
    ("학생3", "머신러닝", "2024-01-15", True),
    ("학생1", "웹 개발", "2024-01-20", False),
]

reviews = [
    {"course": "파이썬 기초", "student": "학생1", "rating": 5, "content": "초보자에게 좋은 강의"},
    {"course": "파이썬 기초", "student": "학생2", "rating": 4, "content": "기초를 잘 설명해줌"},
    {"course": "데이터 분석", "student": "학생1", "rating": 5, "content": "실무에 도움이 됨"},
    {"course": "머신러닝", "student": "학생3", "rating": 4, "content": "내용이 깊이있음"},
]

# 여기에 코드를 작성하세요
