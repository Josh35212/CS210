"""A decorator that traces calls/returns of a recursive function.

Usage:
  from tracer import trace

  @trace()
  def my_recursive_function(m, n):
      ...

Calls and returns of my_recursive_function will be written to the standard error stream.

Limitations:  Not suitable for multi-threaded programs or anything else without a simple
call-return structure on a single stack.  For example, may be a mess with generators.
"""

import sys
from functools import wraps
from io import IOBase

ARG_REP_LIMIT = 10  # Limit length of representation of any single argument

class DecorationSyntaxError(NameError):
    pass

def trace(log_to=sys.stderr, call_stack = []):
    """Use as @trace() or @trace(SEPARATE_STACK).
    Returns a decorator that shows call-stack at entry
    and just before return.
    Note call_stack will be aliased in traces of different functions
    (intentionally!) unless a different output stream is specified.
    """
    # Check for user accidentally writing @trace instead of @trace()
    if not isinstance(log_to, IOBase):
        raise DecorationSyntaxError("@trace should be @trace() with parentheses")

    def trace_wrapper(func):
        # FIXME: Should we associate a different call-stack with each output destination?
        @wraps(func)
        def trace_guts(*args, **kwargs):
            nonlocal call_stack
            nonlocal log_to
            level = len(call_stack)
            arg_vals = ", ".join(arg_str(arg) for arg in args)
            called_like = f"{func.__name__}({arg_vals})"
            if level > 0:
                print("│   " * (level - 1) + "├───", file=log_to, end="")
            print(f"{called_like}", file=log_to)
            call_stack.append(called_like)  # On entry
            retval = func(*args, **kwargs)
            call_stack.pop() # On exit
            # Omit printing "None" as a return value
            if retval is None:
                return None
            # Otherwise we print the return value
            if level > 0:
                print("│   " * level, file=log_to, end="")
            print(f"{retval}", file=log_to)
            return retval
        return trace_guts
    return trace_wrapper

def arg_str(arg: object) -> str:
    """Represent argument succinctly, abbreviating if necessary"""
    raw = str(arg)
    # Is it too long?
    if len(raw) > ARG_REP_LIMIT:
        return "_"
    return raw


# With a single call, tracing fact produces a
# display like this:
# fact(4)
# ├───fact(3)
# │   ├───fact(2)
# │   │   ├───fact(1)
# │   │   │   1
# │   │   2
# │   6
# 24
@trace()
def fact(n: int) -> int:
    if n > 1:
        return n * fact(n-1)
    else:
        return 1

# GCD follows a similar indentation pattern to
# fact, but it's a true tail-call, returning a result
# unchanged all the way up the call chain:
# gcd(18, 24)
# ├───gcd(24, 18)
# │   ├───gcd(18, 6)
# │   │   ├───gcd(6, 0)
# │   │   │   6
# │   │   6
# │   6
# 6
@trace()
def gcd(m: int, n: int) -> int:
    if n > 0:
        return gcd(n, m % n)
    return m


# With fibonacci we can see a more typical example
# that is not simply tail-recursive, but has multiple
# recursive calls.  The idea is to make it easy to see how
# results of calls are combined in the recursive case.  We
# can also see how redundant these calls are, suggesting that
# a memoized or dynamic programming implementation would be
# much more efficient:
#
# fib(4)
# ├───fib(3)
# │   ├───fib(2)
# │   │   ├───fib(1)
# │   │   │   1
# │   │   ├───fib(0)
# │   │   │   0
# │   │   1
# │   ├───fib(1)
# │   │   1
# │   2
# ├───fib(2)
# │   ├───fib(1)
# │   │   1
# │   ├───fib(0)
# │   │   0
# │   1
# 3

@trace()
def fib(m: int) -> int:
    if m > 1:
        return fib(m-1) + fib(m-2)
    else:
        return m

# Test of recognizing incorrect syntax in decoration
# @trace
# def fib(m: int) -> int:
#     if m > 1:
#         return fib(m-1) + fib(m-2)
#     else:
#         return m


if __name__ == "__main__":
    print("Tracing factorial(4)")
    print(fact(4))
    print("Tracing recursive fibonacci(4)")
    print(fib(4))
