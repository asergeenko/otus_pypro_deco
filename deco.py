from functools import update_wrapper

def disable(func):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return func


def decorator(dec):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''
    def wrapper(func):
        return update_wrapper(dec(func),func)

    return update_wrapper(wrapper,dec)


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''

    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args,**kwargs)

    wrapper.calls = 0
    return update_wrapper(wrapper,func)


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''

    def wrapper(x, *args):
        return x if not args else func(x, wrapper(*args))

    return update_wrapper(wrapper,func)


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''

    def wrapper(*args, **kwargs):
        key = (func,args,tuple(kwargs.items()))
        if key not in wrapper.results:
            wrapper.results[key]= func(*args, **kwargs)
            update_wrapper(wrapper, func)
        return wrapper.results[key]
    wrapper.results = {}
    return update_wrapper(wrapper,func)


def trace(tab):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    def decorator(func):
        def wrapper(*args,**kwargs):
            args_str = ','.join([ str(arg) for arg in args ])
            kwargs_str = ','.join([ '%s=%s'%(key, str(value)) for key, value in kwargs ])            
            if args_str and kwargs_str:
                full_str = args_str + ',' + kwargs_str
            else:
                full_str = args_str + kwargs_str
            decorator.depth += 1
            print (tab * decorator.depth,'-->', func.__name__, '(%s)'%(full_str,))
            result = func(*args,**kwargs)
            print (tab * decorator.depth,'<--', func.__name__, '(%s)'%(full_str,),'==',result)
            decorator.depth -= 1   
            return result
             
        return update_wrapper(wrapper,func)
    decorator.depth = 0
    return decorator

@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b

#memo = disable

@countcalls
@trace("####")
@memo
def fib(n):
    '''
    Returns n-th Fibonacci number
    :param n: int
    :return: n-th Fibonacci number
    '''
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print (foo(4, 3))
    print (foo(4, 3, 2))
    print (foo(4, 3))
    print ("foo was called", foo.calls, "times")

    print (bar(4, 3))
    print (bar(4, 3, 2))
    print (bar(4, 3, 2, 1))
    print ("bar was called", bar.calls, "times")

    print (fib.__doc__)
    fib(5)
    print (fib.calls, 'calls made')


if __name__ == '__main__':
    main()
