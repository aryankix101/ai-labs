import sys

def is_prime(x):
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

def problem_7():
    i = 0
    prime = 2
    while i < 10000:
        prime+=1
        if is_prime(prime):
            i+=1
    print(prime)

def problem_1():
    print(sum([i for i in range(1000) if i % 3 == 0 or i % 5 == 0]))

def problem_2():
    start1, start2 = 1, 2
    adder = 0
    sum_even = [2]
    while adder <= 4000000:
        adder = start1 + start2
        if adder%2==0:
            sum_even.append(adder)
        start1 = start2
        start2 = adder
    print(sum(sum_even))

def problem_3():
    i = 2
    num = 600851475143
    while i < num:
        if num%i==0:
            num = num/i
            i = 1
        i+=1
    print(int(num))

def problem_4():
    palindromes = []
    for i in range(100, 1000):
        for x in range(100, 1000):
            product = (i*x)
            product_str = str(product)
            if product_str==product_str[::-1]:
                palindromes.append(product)
    
    print(max(palindromes))

def problem_8():
    num = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
    maximum = 0
    for i in range(0, len(num)-12):
        numbers = []
        for c in num[i:i+13]:
            numbers.append(c)
        numbers = [int(numbers[j]) for j in range(len(numbers))]
        value = 1
        for k in numbers:
            value *= k
        if value > maximum:
            maximum = value
    print(maximum)

def problem_9():
    value = 0
    for c in range(0, 1001):
        for b in range(0, c):
            for a in range(0, b):
                if a + b + c == 1000:
                    if a**2 + b**2 == c**2:
                        value = a * b * c
                        break
    print(value)

problem_7()
problem_1()
problem_2()
problem_3()
problem_4()
problem_8()
problem_9()