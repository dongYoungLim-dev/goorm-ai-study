def totalPagingCount(totalCount, listCount):
  if listCount != 0 and totalCount >= listCount:
    pagingCount = totalCount / listCount;
    return pagingCount
  else:
    return 1;

print(totalPagingCount(20, 140));