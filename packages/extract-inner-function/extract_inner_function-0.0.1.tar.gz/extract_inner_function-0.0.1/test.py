def outer():
    def inner1():
        print("from inner1")

    def inner2(a, b):
        print("from inner2", a, b)

        def inner3(*args, **kwargs):
            print(f"{args=} {kwargs=}")

    print("from outer")

from src.extract_inner_function import extract_inner_function

func = extract_inner_function(
    outer_func=outer, 
    inner_func_name="inner3", 
    print_inner_func=True,
)

func(1, 2, a=6, b=7)

# def inner3(*args, **kwargs):
#     print(f"{args=} {kwargs=}")

# args=(1, 2) kwargs={'a': 6, 'b': 7}