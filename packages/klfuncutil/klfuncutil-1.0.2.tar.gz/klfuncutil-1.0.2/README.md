# Functional Programming Utilities
"Functional Programming" distinguishes between:

1. Data
2. Functions
3. Actions

## Working with data
Data should be treated as immutable.
For example, if an element is added to a list,
a new "list" object is created. The source remains
unchanged. This corresponds to the behavior of strings in Python.
The situation is different with the "Collection" objects in Python.
The classes:
- list
- dict

can be changed "in place". "tuple" and "set" cannot, however.
The module "collection.py" provides the functions:
- append_element
- append_collection
- remove_element

which can be used to edit:
- list
- dict
- tuple

in the same way. The source remains
unchanged in each case. The result is always a new object of the same class as the source.

## Working with functions and iterators
Functions - or "pure functions" are used to implement
business rules. The result depends only on the
input parameters of the function. The iterators, which are also frequently used in
functional programming, lead to surprising effects.

Example:
```
def get_even_num(list_of_numbers):
return filter(lambda x: x % 2 == 0, list_of_numbers)

# Create iterator; return even numbers only
coll_even_num = get_even_num([1,2,3,4,5,6,7,8])
# get sum; sum is a "pure function"
print(sum(coll_even_num))
print(sum(coll_even_num))
```
The output is:
```
20
0
```
The result is quickly explained: the function "sum" used up the iterator "coll_even_num" with the first call. With the second call, this iterator no longer returns any values ​​- the result is "0".
If you run the example shown above with an object of the class "list", a different result is returned:

```
def get_even_num_as_list(list_of_numbers):
return list(filter(lambda x: x % 2 == 0, list_of_numbers))

# Create iterator; return even numbers only
coll_even_num = get_even_num([1,2,3,4,5,6,7,8])
# get sum; sum is a "pure function"
print(sum(coll_even_num))
print(sum(coll_even_num))
```
The output is:
```
20
20
```

An important feature of Python is generic algorithms.
These (like the "sum" function) can work with different input data such as:
- tuple
- list
- iterator

The "iterator.py" module provides the "decorators":
- restartable_t
- restartable_m

These can be used on functions that return "iterators".
The "decorator" is used to package the "iterator" in a class that returns a new "iterator" every time the function ``__iter__()`` is called. "restartable_t" and "restartable_m" use different methods to
get a new "iterator":
- "restartable_t" calls the function that created the original "iterator" again.
- "restartable_m" uses the "itertools.tee" function internally.

"restartable_t" and "restartable_m" cannot, of course, perform miracles - they merely compensate for the unexpected behavior of the "iterator". "restartable_t" does this at the expense of runtime - "restartable_m" at the expense of storage space.

Example:
```
from klfuncutil.iterator import restartable_t

@restartable_t
def get_even_num(list_of_numbers):
return filter(lambda x: x % 2 == 0, list_of_numbers)

# Create iterator; return even numbers only
coll_even_num = get_even_num([1,2,3,4,5,6,7,8])
# getsum; sum is a "pure function"
print(sum(coll_even_num))
print(sum(coll_even_num))
```
The output is:
```
 20
 20
```

## Repro
https://github.com/nuuk42/klfuncutil.git

## Installation
Use: pip install klfuncutil

## History



