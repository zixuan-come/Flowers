



def countdown(n):
    for i in range(n, 0, -1):
        yield i



for num in countdown(5):
    print(num)



