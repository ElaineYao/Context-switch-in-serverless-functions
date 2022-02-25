import time

def Average(lst):
    return sum(lst) / len(lst)

def canary():
    """
    """
    timelapses = []

    for i in range(100):
        s1 = time.time()
        s2 = time.time()
        timelapses.append( s2 - s1 )

    print(str(timelapses))
    print("\nAverage value: "+str(Average(timelapses)))
    # return {'timelapses': str(timelapses)}

if __name__ == "__main__":
    canary()