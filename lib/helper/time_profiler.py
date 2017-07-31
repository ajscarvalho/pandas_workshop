# -*- coding: utf-8 -*-

from datetime import datetime


reports = {
    'callCnt': {},
    'accTime': {},
    'maxTime': {}
}


def time_profiler(fn=None, log=None):
    """profiles the time it takes for a function call to execute, logging it to stdout or to the specified log object

    Usage::

        def fn(...):
            ...
        fn = time_profile(fn, log=Log())

    If you are using Python 2.4, you should be able to use the decorator
    syntax::

        @time_profile(log=Log())
        def fn(...):
            ...

    or just ::

        @time_profile
        def fn(...):
            ...

    """
    if fn is None:  # @profile() syntax -- we are a decorator maker
        def decorator(fn):
            return time_profiler(fn, log=log)
        return decorator

    # @profile syntax -- we are a decorator.
    
    # We cannot return fp or fp.__call__ directly as that would break method
    # definitions, instead we need to return a plain function.

    def new_fn(*args, **kw):
        before = datetime.now()
        result = fn(*args, **kw)
        delta = datetime.now() - before
        print_delta(delta, log)
        return result


    def print_delta(delta, log):
        message = ' - ' + fn.__name__ + ' call took '
        if delta.seconds: message += str(delta.seconds)
        if delta.microseconds: message += "." + str(delta.microseconds).zfill(6)
        message += " seconds to complete."
        
        if log: log.info(message)
        else: print (message)
        

    new_fn.__doc__ = fn.__doc__
    new_fn.__name__ = fn.__name__
    new_fn.__dict__ = fn.__dict__
    new_fn.__module__ = fn.__module__
    
    return new_fn




def mass_profiler(fn=None):
    """profiles the impact of function calls by trackin the time each function takes to run 
        and how much time it takes to run. 

    Usage::

        def fn(...):
            ...
        fn = mass_profile(fn)

    If you are using Python 2.4, you should be able to use the decorator syntax::

        @mass_profile
        def fn(...):
            ...
    """
    if fn is None:  # @profile() syntax -- we are a decorator maker
        def decorator(fn):
            return mass_profiler(fn)
        return decorator

    # @profile syntax -- we are a decorator.

    def new_fn(*args, **kw):
        before = datetime.now()
        result = fn(*args, **kw)
        delta = datetime.now() - before
        register_delta(delta.total_seconds())
        return result


    def register_delta(delta):
        fnName = fn.__name__ 
        #print (fn.__self__)
        classes =''
        key = classes + "::" + fnName
        if reports['callCnt'].get(key) is None:
            reports['callCnt'][key] = 1
            reports['accTime'][key] = delta
            reports['maxTime'][key] = delta
        else:
            reports['callCnt'][key]+= 1
            reports['accTime'][key]+= delta
            reports['maxTime'][key] = max(delta, reports['maxTime'][key])
        

    new_fn.__doc__ = fn.__doc__
    new_fn.__name__ = fn.__name__
    new_fn.__dict__ = fn.__dict__
    new_fn.__module__ = fn.__module__
    
    return new_fn


def print_report():
	for key in reports['callCnt']:
		print ("\n{}:\n\tCalls    : {}\n\tAvg Time: {}\n\tMax Time: {}\n\tAcc Time: {}\n".format(
			key, 
			reports['callCnt'][key], 
			reports['accTime'][key] / reports['callCnt'][key],
			reports['maxTime'][key],
			reports['accTime'][key]	
		))