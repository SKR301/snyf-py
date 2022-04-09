import multiprocessing

p = []

def process1(p):
    while True:
        print('1>',p)

def prin(p):
    print('!!!!!!!!!!!!!!!!!',p)

def process2(p):
    while True:
        p.append(2)
        prin(p)

if __name__=='__main__':
    p1 = multiprocessing.Process(target=process1, args=(p,))
    p2 = multiprocessing.Process(target=process2, args=(p,)) 
    p2.start()
    p1.start()