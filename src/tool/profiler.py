import resource
import timeit
import time
import threading

MEMORY_USAGE_PROFILE_INTERVAL = 0.005


def profile(func, args: tuple=None, kwargs: dict=None):
    """
    Profile the memory and runtime of a function
    """

    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_memory = 0
    start_time = time.time()

    th = threading.Thread(target=func, args=args, kwargs=kwargs)
    th.start()

    while th.is_alive():
        time.sleep(MEMORY_USAGE_PROFILE_INTERVAL)
        delta_memory = resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss - start_memory
        if delta_memory > max_memory:
            max_memory = delta_memory

    end_time = time.time()
    print("-------------------------------------------")
    print("Stats of {}:\nMax Memory: {} MB\nRuntime: {} seconds".format(
        func.__name__, round(max_memory/1000, 2), round(end_time - start_time, 2)))
    print("-------------------------------------------")

    return 
