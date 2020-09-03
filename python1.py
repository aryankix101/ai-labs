import sys

if sys.argv[1]=='A':
    print(sys.argv[2]+sys.argv[3]+sys.argv[4])

if sys.argv[1]=='B':
    print(sum([int(int_arg) for int_arg in sys.argv[2:]]))

if sys.argv[1]=='C':
    print(sum([int(int_arg) for int_arg in sys.argv[2:] if int(int_arg)%3==0]))

if sys.argv[1]=='D':
    values = []
    count = 0
    n1, n2 = 1, 1
    while count < int(sys.argv[2]):
        values.append(n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth
        count += 1
    print(values)

if sys.argv[1]=='E':
    values = []
    for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
        temp = 0
        temp = i**2 - 3*i + 2
        values.append(str(temp))
    print(', '.join(values))

if sys.argv[1]=='F':
    x, y, z = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    if (x + y <= z) or (x + z <= y) or (y + z <= x) :
        print("Invalid triangle.")
    else:
        p = (x+y+z)/2
        area = (p*(p-x)*(p-y)*(p-z))**0.5
        print(area)

#Currently returns a dictionary, is that ok? Document said list...
if sys.argv[1]=='G':
    chars = {
        'a': 0,
        'e': 0,
        'i': 0,
        'o': 0,
        'u': 0
    }
    for c in sys.argv[2].lower():
        if c in chars:
            chars[c]+=1
    
    print(chars)