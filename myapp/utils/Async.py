import concurrent.futures
from typing import Callable, Tuple, Any, List, Dict

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=6)

def make_async(func: Callable[..., Any]) -> Callable:
    def wrapper(*args, **kwargs):
        return _executor.submit(func, *args, **kwargs)
    return wrapper

# call with func([
#    (func1, (1, 3), {}), #or
#    (func2, (), {"arg1"=1, "arg2"=3}), 
# ])
def run_async_functions(funcs:List[Tuple[Callable[..., Any], Tuple[Any], Dict[str, Any]]]) -> Tuple[Any]:
    futures = []
    for func, args, kargs in funcs:
        future = _executor.submit(func, *args, **kargs)
        futures.append(future)
    
    result = []
    for f in concurrent.futures.as_completed(futures):
        try:
            result.append(f.result)
        except Exception as e:
            result.append(e)
    return result