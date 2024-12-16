#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import List, Union

# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性：
#     - 如果定义 `__all__`，那么【只有在这个列表中的属性才会被导入】
#     - 如果没有定义 `__all__`，那么默认【导入模块中不以下划线开头的所有属性】
__all__ = [
    "tags_to_dict",
    "to_list"
]


def tags_to_dict(inv_tag: str) -> dict:
    """
        `inv_tags` 代表的意思是 "Zabbix Host Inventory Tags"。

        解析 zbx 主机清单标签字符串，
        并将其转换为字典形式的过程包含以下几个步骤：
            - 首先，输入的标签字符串应该由【键值对】组成，
              其中键和值之间默认使用等号 "=" 分隔，
              各个键值对则通过英文分号 ";" 或者中文 "；" 分隔开来。

            - 其次，如果输入不是字符串类型，则会抛出异常，
              并且在解析过程中空的键值对会被忽略。

              此外，该函数不会处理嵌套或复杂结构的标签字符串，
              它仅支持简单的一层键值对结构。

            - 最后，如果在标签字符串中存在重复的键，
              则后面出现的值会覆盖前面出现的同名键的值。

        示例：
            >>> tags = tags_to_dict(
            >>>     inv_tags="key1=value1;key2=value2;key3"
            >>> )
            >>> print(tags)
            {"key1": "value1", "key2": "value2", "key3": ""}

    :param inv_tag: 一个表示主机清单标签的字符串，
    格式为 "key=value" 键值对，
    键值对之间用英文或中文分号分隔。
    :return: 一个字典，其中包含从输入字符串解析得到的键值对。
    :raises TypeError: 当 `inv_tag` 不是字符串时抛出。
    """
    # 此处排除 `None` 和空字符串的情况（即 `""`）
    if not inv_tag:
        return {}
    if not isinstance(inv_tag, str):
        raise TypeError(
            "主机清单标签内容必须是字符串。"
        )
    split_tags = (
        item.partition(r"=")[::2]
        for item in re.split(r"[;；]", inv_tag)
        if item
    )
    return {
        k.strip(): v.strip()
        for k, v in split_tags
    }


def to_list(
        value: Union[str, List[str], None]) -> list:
    """
        将输入转换为【列表】。

        如果输入是字符串，则返回包含此字符串的列表；

        如果输入是 None，则返回空列表；

        如果输入已经是列表，则直接返回。

    :param value: 要转换的输入，
    可以是字符串或者已经是列表。
    :return: 列表形式的结果。
    """
    if isinstance(value, str):
        return [value]
    elif isinstance(value, list):
        return value
    elif value is None:
        return []
    else:
        raise TypeError(
            f"期望得到 str、List[str] 或 None 类型；"
            f"实际得到的是 {type(value).__name__}。"
        )
