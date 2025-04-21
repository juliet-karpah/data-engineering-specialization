#!/usr/bin/env python
# coding: utf-8

# ## Timing Decorator

# In[31]:


# Function decorator that times execution
from time import time

def timer(func):
    # Nested wrapper function
    def wrapper():
        start = time()
        func()
        end = time()
        print(f"Duration: {end-start}")
    return wrapper


# In[32]:


@timer
def sum_nums():
    result = 0
    for x in range(1000000):
        result += x

sum_nums()


# ## Logging Decorator

# In[33]:


def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Ran {func.__name__} with args: {args}, and kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper


# In[34]:


@logger
def add(x, y):
    return x + y

@logger
def sub(x, y):
    return x - y

add(10, 20)
sub(30, 20)


# ## Caching Decorator

# In[35]:


import functools

def cache(func):
    cache_data = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key not in cache_data:
            cache_data[key] = func(*args, **kwargs)
        return cache_data[key]
    return wrapper


# In[36]:


import time
@cache
def expensive_func(x):
    start_time = time.time()
    time.sleep(2)
    print(f"{expensive_func.__name__} ran in {time.time() - start_time:.2f} secs")
    return x



# In[37]:


get_ipython().run_line_magic('time', 'print(expensive_func(1))')


# In[38]:


get_ipython().run_line_magic('time', 'print(expensive_func(1))')


# In[39]:


@cache
def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


# In[40]:


fibonacci(10)


# ## Delay

# In[41]:


import time
from functools import wraps

def delay(seconds):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Sleeping for {seconds} seconds before running {func.__name__}")
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return inner


# In[42]:


@delay(seconds=3)
def print_text():
    print("Hello World")

print_text()

