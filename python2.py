def string_times(str, n):
  return str * n

def front_times(str, n):
  return str[0:3] * n

def string_bits(str):
  return str[0::2]

def string_splosion(str):
  return ''.join(str[:idx] for idx in range(len(str)+1))

def last2(str):
  return sum([1 for i in range(len(str)-2) if str[-2:]==str[i:i+2]])

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[0:4]

def array123(nums):
  return bool([1 for i in range(len(nums)-2) if nums[i:i+3]==[1, 2, 3]])

def string_match(a, b):
  return sum([1 for i in range(len(a)-1) if a[i:i+2]==b[i:i+2]])

def make_bricks(small, big, goal):
  return (goal%5)<=small and goal<=big*5+small

def lone_sum(a, b, c):
  return sum([i for i in [a, b, c] if [a, b, c].count(i)==1])

def lucky_sum(a, b, c):
  return (a!=13) * a + (a!=13 and (b!=13) * b) + (a!=13 and b!=13 and (c!=13) * c)

def no_teen_sum(a, b, c):
  return (a not in [*range(13, 15), *range(17, 20)])*a + (b not in [*range(13, 15), *range(17, 20)])*b + (c not in [*range(13, 15), *range(17, 20)])*c

def round_sum(a, b, c):
  return ((a+5)//10)*10 + ((b+5)//10)*10 + ((c+5)//10)*10

def close_far(a, b, c):
  return (abs(b-a)<=1 and abs(c-a)>=2 and abs(c-b)>=2) or (abs(c-a)<=1 and abs(b-a)>=2 and abs(b-c)>=2)

def make_chocolate(small, big, goal):
  return goal-(big*5) if (goal >= big*5) and (small >= goal - big*5) else(goal%5 if (goal < big*5) and (small >= goal % 5) else -1)

def double_char(str):
  return ''.join([c*2 for c in str])

def count_hi(str):
  return str.count('hi')

def cat_dog(str):
  return str.count('cat')==str.count('dog')

def count_code(str):
  return sum([1 for i in range(len(str)-3) if str[i:i+2]=='co' and str[i+3]=='e'])

def end_other(a, b):
  return b.lower().endswith(a.lower()) or  a.lower().endswith(b.lower())

def xyz_there(str):
  return str.count('xyz') > str.count('.xyz')

def count_evens(nums):
  return sum([1 for i in nums if i%2==0])

def big_diff(nums):
  return max(nums)-min(nums)

def centered_average(nums):
  return (sum(nums)-max(nums)-min(nums))//(len(nums)-2)

def sum13(nums):
  return sum([nums[idx] for idx in range(len(nums)) if (idx==0 and nums[idx]!=13) or nums[idx]!=13 and nums[idx-1]!=13])

def sum67(nums):
  sum = 0
  cancel = False
  for i in nums:
    if i == 6:
      cancel = True
    if not cancel:
      sum += i
    if i == 7:
      cancel = False
  return sum
  
def has22(nums):
  return any([True for i in range(len(nums)-1) if nums[i:i+2] == [2,2]])

