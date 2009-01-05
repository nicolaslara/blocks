"""
A decorator to use Python functions in a way similar to Ruby blocks.

=========
 Missing
=========
 * Implement some default ruby ones
 * Add doctests
 * Organize in different files. (decorators.py, defaults.py)
"""

import types

def receive_block(func):
    def decorator(*args):
        if len(args) == 1:
            block, = args
            instance = None
        elif len(args) == 2:
            instance, block = args
            
        # Add block to globals
        scope = func.func_globals #globals()
        scope.update({'block':block})

        #create the function with the new scope
        new_func = types.FunctionType(func.__code__, scope)
        
        if instance:
            return new_func(instance)
        else:
            return new_func()

    return decorator

@receive_block
def external():
    for i in [1,2,3]:
        print block()

print "External"
@external
def _():
    return "a"

@receive_block
def param_external():
    for i in [1,2,3]:
        print block(i)

print "External with param"
@param_external
def _(i):
    return "a " + unicode(i) 


class Array(list):
    @receive_block
    def each(self):
        for i in self:
            print block(i)

    @receive_block
    def collect(self):
        for (i, value) in enumerate(self):
            self[i] = block(value)

    @receive_block
    def handled(self):
        for i in self:
            try:
                block(i)
            except:
                print "This raised an exception"

a = Array([1,2,3,4])

print "Each Square"
@a.each
def _(x):
    return x**2

print "Each"
@a.each
def _(x):
    return x

print "Collect"
@a.collect
def _(x):
    return x**2

print a # a is changed

print "Handled"
@a.handled
def _(x):
    if x != 9:
        raise Exception("this won't work")
    else:
        print "this works"



