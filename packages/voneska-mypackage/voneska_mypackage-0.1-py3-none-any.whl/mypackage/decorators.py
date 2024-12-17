import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{time.time() - start:.6f} seconds")
        return result

    return wrapper


@timeit
def slow_sum(a, b, *, delay):
    time.sleep(delay)
    return a + b


print(slow_sum(2, 2, delay=1))
