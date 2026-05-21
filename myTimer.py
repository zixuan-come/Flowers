import time

def my_timer(unit="s"):
    def decorate(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            function = func(*args, **kwargs)
            print(f"消耗时间：{time.time() - start}{unit}")
            return function
        return wrapper
    return decorate


@my_timer(unit="s")
def add(a, b):
    return a+b


ret = add(1, 2)
print(ret)






# import time
#
#
# def my_timer(unit="s"):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             start_time = time.time()
#             result = func(*args, **kwargs) # 执行传进来的函数
#             elapsed = time.time()-start_time
#             if unit == "ms":
#                 print(f"耗时：{elapsed*1000:.2f}ms")
#             else:
#                 print(f"耗时：{elapsed :.2f}s")
#             return result
#         return wrapper
#     return decorator
#
# @my_timer(unit="s")
# def slow_function(*args, **kwargs):
#     time.sleep(1)
#     return "done"
#
#
# slow_function()
#
