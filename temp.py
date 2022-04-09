import multiprocessing

def f1(d):
    while True:
        print(d)

def f2(d):
    while True:
        d[1] = d[1] + [4]

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    d = manager.dict()
    d[1] = []
    p1 = multiprocessing.Process(target=f1,args=(d,))
    p2 = multiprocessing.Process(target=f2,args=(d,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()