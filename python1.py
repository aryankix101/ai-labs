def sleep_in(weekday, vacation):
  return not weekday or vacation
def monkey_trouble(a_smile, b_smile):
  return a_smile and b_smile or not a_smile and not b_smile
def sum_double(a, b):
  return 2*(a+a) if a==b else a+b
def diff21(n):
  return 2*abs((21-n)) if n>21 else abs(21-n)
def parrot_trouble(talking, hour):
  return talking and (hour < 7 or hour > 20)
def makes10(a, b):
  return True if a ==10 or b == 10 or a+b==10 else False
def near_hundred(n):
  return True if abs(100-n)<=10 or abs(200-n)<=10 else False
def pos_neg(a, b, negative):
  return True if (negative and a < 0 and b < 0) or (not negative and a < 0 and b > 0) or (not negative and a > 0 and b < 0) else False
def hello_name(name):
  return 'Hello ' + name + '!'
def make_abba(a, b):
  return a + b + b + a
def make_tags(tag, word):
  return '<' + tag + '>' + word + '</' + tag + '>'
def make_out_word(out, word):
  return out[0:len(out)/2] + word + out[len(out)/2:]
def extra_end(str):
  return str[-2:] * 3
def first_two(str):
  return str if len(str) < 2 else str[0:2]
def first_half(str):
  return str[:len(str) // 2]
def without_end(str):
  return str[1:-1]
def first_last6(nums):
  return True if str(nums[0])=='6' or str(nums[-1])=='6' else False
def same_first_last(nums):
  return True if len(nums)>=1 and nums[0]==nums[-1] else False
def make_pi(n):
  return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3 , 5 ][0:n]
def common_end(a, b):
  return True if a[0]==b[0] or a[-1]==b[-1] else False
def sum3(nums):
  return sum(nums)
def rotate_left3(nums):
  return nums[1:] + nums[:1]
def reverse3(nums):
    return nums[::-1]
def max_end3(nums):
  return [max(nums[0], nums[-1]) for item in nums]
def cigar_party(cigars, is_weekend):
  return False if cigars < 40 or (cigars > 60 and not is_weekend) else True
def date_fashion(you, date):
  return 2 if you >= 8 and date > 2 or date >= 8 and you > 2 else (0 if you <= 2 or date <=2 else 1)
def squirrel_play(temp, is_summer):
  return True if (temp >=60 and temp <=90)  or (temp>90 and temp<=100 and is_summer) else False
def caught_speeding(speed, is_birthday):
  return 0 if is_birthday and speed <= 65 else(1 if is_birthday and (speed > 65 and speed <= 85) else(2 if is_birthday else(0 if speed <= 60 else(1 if speed > 60 and speed <= 80 else(2 if speed >= 81 else 0)))))
def sorta_sum(a, b):
  return 20 if 10 <= a+b <= 19 else a+b
def alarm_clock(day, vacation):
  return "7:00" if 1 <= day <= 5 and not vacation else("off" if vacation and (day==0 or day==6) else "10:00")
def love6(a, b):
  return True if (a==6 or b==6) or abs(a-b)==6 or a+b==6 else False 
def in1to10(n, outside_mode):
  return True if (outside_mode and (n<=1 or n>=10)) or not outside_mode and 1 <= n <= 10 else False
 