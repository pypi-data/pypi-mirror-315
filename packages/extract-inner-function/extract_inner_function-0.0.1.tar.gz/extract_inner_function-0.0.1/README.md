
# extract_inner_function

A simple package to extract inner functions in Python

# Context

Normally, inner functions are accessible only inside the function itself, and we cannot do this

```python
def outer():
    def inner1(a, b):
        # this can be accessed only inside of outer()
```

But there is actually a (hacky) way to extract inner functions

Disclaimer - this package is for fun. Try not to use in prod

# installation

```
pip install extract_inner_function
```

# quickstart

```python
def outer():
    def inner1():
        print("from inner1")

    def inner2(a, b):
        print("from inner2", a, b)

        def inner3(*args, **kwargs):
            print(f"{args=} {kwargs=}")

    print("from outer")

from extract_inner_function import extract_inner_function

func = extract_inner_function(
    outer_func=outer, 
    inner_func_name="inner3", 
    print_inner_func=True,
)

func(1, 2, a=6, b=7)

# def inner3(*args, **kwargs):
#     print(f"{args=} {kwargs=}")

# args=(1, 2) kwargs={'a': 6, 'b': 7}
```

^ notice that we are able to extract the inner function here

# so when should we use this package?
- if the existing codebase contains lots of inner functinos
- you wish to do unit testing on these inner functions
- you don't have time to (or cannot be bothered to) refactor the codebase
