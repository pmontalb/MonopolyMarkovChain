from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import cpu_count


def multiprocess_map(func, args, n_processors=cpu_count()):
    p = Pool(n_processors)
    return p.map(func, args)