import time



def my_timer(func):
    def wrapper():
        start_time = time.time()
        result = func() # 执行传进来的函数
        print(f"耗时：{time.time()-start_time:.2f}s")
        return result
    return wrapper

@my_timer
def slow_function():
    time.sleep(1)
    return "done"



slow_function = my_timer(slow_function)
slow_function()


