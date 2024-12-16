from typing import Callable
import re
import inspect
import types
from textwrap import dedent

def extract_inner_function(
    outer_func: Callable,
    inner_func_name: str,
    print_inner_func: bool = False
) -> Callable:
    """
    Extract inner function from outer function

    Args:
        outer_func (Callable): outer function we wish to extract inner function from
        inner_func_name (str): name of inner function we wish to extract
        print_inner_func (bool): if True, prints inner function code using print()
    """
    # get entire source code using inspect module
    outer_func_src: str = inspect.getsource(outer_func) + "    _: int"

    # extracting inner code
    inner_func_src: str = ""
    inner_func_indent: str = ""
    continue_matching: bool = False
    for func_line in outer_func_src.split("\n"):

        # find first line of inner func
        if f"def {inner_func_name}(" in func_line:
            continue_matching = True
            inner_func_indent = func_line.split("def")[0]
            inner_func_src += func_line + "\n"

        # add all other lines, til indentation mismatch
        elif continue_matching:
            # get indent level of this line
            try:
                func_line_indent = re.findall("^ +", func_line)[0]
            except:
                func_line_indent = ""
            
            # if indent level >= inner_func_indent, inner func has ended
            if len(func_line_indent) > len(inner_func_indent):
                inner_func_src += func_line + "\n"
            else:
                break

    inner_func_src = dedent(inner_func_src)

    if print_inner_func:
        print(inner_func_src)

    # compile inner code into code object
    code_obj = compile(inner_func_src, '<string>', 'exec')

    # use FunctionType to convert it into a real function
    func: Callable = types.FunctionType(code_obj.co_consts[0], locals())

    return func
