def problem_12():
    l = 0 
    n = 0 
    divisors = 0 
    while divisors <= 500:
        divisors = 0
        l += 1
        sum_triangle = sum([x for x in range(1, l+1)])
        n = sum_triangle
        y = 1
        while y <= n**0.5:
            if n % y == 0:
                divisors += 1
            y += 1
        divisors *= 2
    print("Problem 12: " + str(n))

def problem_14():
    dic = {n: 0 for n in xrange(1,1000000)}
    dic[1] = 1
    dic[2] = 2
    for n in xrange(3,1000000,1):
        counter = 0
        original_number = n
        while n > 1:
            if n < original_number:
                dic[original_number] = dic[n] + counter
                break
            if n%2 == 0:
                n = n/2
                counter += 1
            else:
                n = 3*n+1
                counter += 1
    print(dic.values().index(max(dic.values()))+1)
problem_12()