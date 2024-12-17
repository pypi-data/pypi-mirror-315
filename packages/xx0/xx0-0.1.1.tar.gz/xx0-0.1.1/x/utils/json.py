import json
from typing import Any

def str(obj: Any) -> str:
    """对象转换为 JSON 字符串

    Examples:
        >>> class Person:
        ...     def __init__(self, 姓名: str, 年龄: int):
        ...         self.姓名 = 姓名
        ...         self.年龄 = 年龄
        >>> 小明 = Person("小明", 18)
        >>> print(str(小明))
        {"姓名": "小明", "年龄": 18}
    """
    try:
        if hasattr(obj, '__dict__'):
            return json.dumps(obj.__dict__, ensure_ascii=False)
        return json.dumps(obj, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"无法将对象转换为JSON字符串: {str(e)}")
