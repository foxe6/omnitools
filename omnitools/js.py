import json
from typing import *


__ALL__ = ["jo", "jl", "dumpobj"]


def jd(o: Any, **kwargs) -> str:
    return json.dumps(o, **kwargs)


def jl(s: str, **kwargs) -> Any:
    return json.loads(s, **kwargs)


def _dumpobj(obj: Any, isObj: bool = False, indent: int = -1, indent_scale: int = 4) -> str:
    do_indent = True if indent >= 0 else False
    if indent >= 0 and indent % indent_scale != 0:
        raise Exception(f"indent {indent} is not multiples of indent_scale {indent_scale}")
    try:
        if not isinstance(obj, (tuple, list, dict, bool)):
            return jd(obj)
        raise
    except:
        from .xtypes import Obj
        if isinstance(obj, (bytes, bool)):
            return str(obj)
        elif isinstance(obj, (tuple, list)):
            tmp = "[" if isinstance(obj, list) else "("
            if do_indent:
                tmp += "\n"
                indent += indent_scale
            for i, item in enumerate(obj):
                if i:
                    tmp += ","
                    if do_indent:
                        tmp += "\n"
                    else:
                        tmp += " "
                if do_indent:
                    if not isinstance(item, Obj):
                        tmp += " "*indent
                tmp += _dumpobj(item, indent=indent, indent_scale=indent_scale)
            if do_indent:
                tmp += "\n"
                tmp += " "*(indent-indent_scale)
            tmp += "]" if isinstance(obj, list) else ")"
            return tmp
        elif isinstance(obj, dict):
            col = ": "
            tmp = "Obj({" if isObj else "{"
            tmp += "\n"
            if do_indent:
                indent += indent_scale
            else:
                tmp = "{"
            for i, (k, v) in enumerate(obj.items()):
                if i:
                    tmp += ","
                    if do_indent:
                        tmp += "\n"
                    else:
                        tmp += " "
                if do_indent:
                    tmp += " "*indent
                tmp += f'''{_dumpobj(k)}{col}{_dumpobj(v, indent=indent, indent_scale=indent_scale)}'''
            if do_indent:
                tmp += "\n"
                tmp += " "*(indent-indent_scale)
            tmp += "}"
            if isObj:
                tmp += ")"
            return tmp
        elif isinstance(obj, Obj):
            return obj.dump(indent_scale=indent_scale)
        else:
            return f'''{type(obj).__name__}({str(obj)})'''


def dumpobj(obj: Any, isObj: bool = False, indent_scale: int = 0) -> str:
    import inspect
    stack = [a[3] for a in inspect.stack()]
    dumpobjsize = len([_ for _ in stack if _ == inspect.stack()[1][3]])
    dumpsize = len([_ for _ in stack if _ == "dump"])
    indent = -1 if indent_scale <= 0 else 0
    dumps = _dumpobj(obj, isObj, indent, indent_scale)
    if dumpobjsize >= 2 and dumpobjsize == dumpsize:
        dumpobjsize += 1
        import textwrap
        return textwrap.indent(dumps, " "*dumpobjsize*indent_scale)
    elif dumpobjsize-1 >= 2 and dumpobjsize > dumpsize:
        import textwrap
        dumps = textwrap.indent(dumps, " "*dumpobjsize*indent_scale)
        return dumps
    else:
        return dumps


