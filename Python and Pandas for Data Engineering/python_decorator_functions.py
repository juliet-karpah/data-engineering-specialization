
from time import time
from functools import wraps, lru_cache
from datetime import timedelta, datetime

def timer(func):
    # Nested wrapper function
    def wrapper():
        start = time()
        func()
        end = time()
        print(f"Duration: {end-start}")
    return wrapper



@timer
def sum_nums():
    result = 0
    for x in range(1000000):
        result += x

sum_nums()


def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Ran {func.__name__} with args: {args}, and kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper


@logger
def add(x, y):
    return x + y

@logger
def sub(x, y):
    return x - y

add(10, 20)
sub(30, 20)


def cache(func):
    cache_data = {}
    wraps(func)
    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key not in cache_data:
            cache_data[key] = func(*args, **kwargs)
        return cache_data[key]
    return wrapper

@cache
def expensive_func(x):
    start_time = time.time()
    time.sleep(2)
    print(f"{expensive_func.__name__} ran in {time.time() - start_time:.2f} secs")
    return x



@cache
def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


fibonacci(10)

def delay(seconds):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Sleeping for {seconds} seconds before running {func.__name__}")
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return inner

@delay(seconds=3)
def print_text():
    print("Hello World")

print_text()


## Challenge to add lru cache to the previous cache decorator provided by the instructor.

def cache(duration, max_size):
    """
    This decorator function uses the LRU caching strategy to store results from a decorated function. 
    The argument duration is used to determine when the cache expires and max_size is used to determine the maximum amount of 
    items a cache can hold before it expels the least recently accessed data point. 

    Parameter duration: The number of seconds to wait before invalidating the cache.
    Precondition: It is a int

    Parameter max_size: The maximum number of items that the cache can hold. By default max_size is 128.
    Precodition: max_size is an int. 
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=max_size)(func)
        func.lifetime = timedelta(seconds=duration)
        func.expiration = func.lifetime + datetime.utcnow()
    
        wraps(func)
        def wrapper_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
            func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapper_func
    return wrapper_cache

@cache(2,16)
def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)