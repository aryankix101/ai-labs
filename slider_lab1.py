import time

start=time.time()

def print3():
    print()
    print("Steps: ")
    print("Construction time: " + str(round((time.time()-start), 1)) +"s")


if __name__ == '__main__':
    print3()