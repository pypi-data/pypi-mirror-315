#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    此脚本旨在处理【zbx Tags】，包括三个主要部分：
        - 首先是【zbx Host Inventory Tags】。
          它主要处理的是 zbx Host Inventory 中的标签字符串，
          这些字符串以
          "key1=value1;key2=value2;key3=value3;key4;" 的形式存在，
          并且得到 zbx 2.0 及以上版本的支持。

        - 其次是【zbx Host Tags】。
          这部分主要涉及在 zbx 中添加、更新和删除【主机标签】(Host Tag)，
          并且这一功能仅在 zbx 5.0 及以上版本中支持。

          (
              需要注意的是，对于主机标签信息（Tags）的处理分为两种情况：
                  - 如果主机是通过【自动发现】功能添加到 zbx 的，
                    则由于 zbx API 的限制，
                    不允许直接对这些自动发现的主机添加 Host Tags（主机标签）。
                    在这种情况下，只能更新 Host Inventory 中的标签信息；

                  - 如果主机不是自动发现类型的，则可以直接添加 Host Tags。
          )

        - 最后是【zbx Item Tags】。
          它主要涉及添加、更新和删除【监控项标签】(Item Tag)，
          这些标签的处理逻辑与处理主机标签（Host Tags）非常相似，
          因此在代码实现中直接继承处理主机标签的类，
          几乎无需额外扩展功能或重写相关方法。
          需要注意的是，
          这一功能仅在 zbx 5.2 及其更高版本中提供支持。

    ***重要的是要了解，虽然脚本聚焦于主机标签的管理任务，
    但它并不直接执行对 zbx 主机的修改操作。

    相反，脚本的作用是生成操作结果，并将这些结果返回给用户。

    用户可以根据这些结果，以及他们具体的需求和场景，
    决定如何进一步使用这些信息。

    因此，该脚本可以被视为一个辅助工具或功能性扩展，
    旨在为开发者或管理员提供更多灵活性和控制能力
    来维护和更新他们的监控系统配置。

    注意：本文档中出现的 "zbx"，如无特殊说明，则指代 "Zabbix"。
         本文档中出现的 "app"，如无特殊说明，则指代 "Application"。
         本文档中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
from collections import UserDict
import sys
from pathlib import Path
from typing import List, Union, Optional, Tuple

# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性：
#     - 如果定义 `__all__`，那么【只有在这个列表中的属性才会被导入】
#     - 如果没有定义 `__all__`，那么默认【导入模块中不以下划线开头的所有属性】
__all__ = [
    "InvTags",
    "HostTags",
    "ItemTags"
]
# 将当前运行的 py 文件所在的上两级目录加入到 py 的【系统路径】中
# 使得在这个【根目录】下的【模块】和【包】可以被当前文件所引用
current_file_path = Path(__file__).absolute()
# 移动到上两级目录以获取【根路径】
root_path = current_file_path.parent.parent
# 将【根路径】作为【系统路径】加入 `sys.path`
sys.path.append(str(root_path))

# 在 py 代码中，`PEP 8` 是一个【编码风格指南】
# 其中 `E402` 错误意味着【模块级别的导入语句没有出现在文件的顶部】
# 对于某个特定的行，可以在该行末尾添加一个特殊的注释
# 来告诉 linter 忽略 `E402` 错误
# 即使用 `# noqa: E402` 告诉代码检查工具忽略此行上的 `E402` 错误
from zbx_utils import tags_to_dict, to_list  # noqa: E402


# 类继承自 `collections.UserDict`
# 此类是 py 中对【字典类型】的【用户友好封装】的类
# 其拥有所有【标准字典】类型的【方法】和【属性】
class InvTags(UserDict):
    """
        处理 Host inventory 中的 `tag` 字段需要注意以下几个要点：
            - 首先，对于使用低版本如 zbx 3.0/4.0 的 Host，
              由于不支持 Host tag 功能；
              或者是在 zbx 5.0/6.0 等高版本中，
              由于自动发现主机不支持直接设置 Host Tags，
              故作为权宜之计可以在 Host inventory 的 `tag` 字段中
              设置相应的 tags。

              这些 Host inventory tags 应该遵循特定的格式规范，
              即以英文或者中文分号分隔的 "k=v" 或 "k" 形式的字符串，
              例如："key1=val1;key2;key3=val3;key4"。

            - 其次，在高版本的 zbx 中（zbx 5.0 及以上），
              虽然 Host 支持直接设置 tag 功能，
              但是 Host inventory 中的 tag 功能仍然被保留下来。

        在这些版本中，虽然以直接在 Host 上设置 tags 为主要方式，
        但用户仍可以选择使用传统的 Host inventory tags 方式来设置标签。

        用法：
            - 创建 `InvTags` 对象：
                >>> tags = InvTags(
                >>>     "env=prod;region=east;"
                >>> )
                >>> print(tags)
                "env=prod;region=east;"

            - 添加新标签或修改现有标签：
                >>> tags["new_key"] = "value"
                >>> print(tags)
                "env=prod;region=east;new_key=value;"

            - 删除一个标签：
                >>> del tags["env"]
                >>> print(tags)
                "region=east;new_key=value;"

            - 若键值为 None，则只输出键名：
                >>> tags["only_key"] = None
                >>> print(tags)
                "region=east;new_key=value;only_key;"

            - 获取某个键对应的值：
                >>> value = tags.get("region")
                >>> print(value)
                "east"

            - 抛出 TypeError 异常，如果尝试设置非法类型作为 value：
                >>> tags["invalid"] = 123
                TypeError: 主机清单标签内容必须是字符串，但接收到: int。

            - 当 `InvTags` 为空时, `__str__` 方法返回空字符串：
                >>> empty_tags = InvTags()
                >>> print(empty_tags)

    """

    def __init__(self, inv_tag=None) -> None:
        """
            调用父类（即 `UserDict`）的初始化方法初始化基础字典结构，
            使用自定义函数 `tags_to_dict` 处理传入参数 `inv_tag`。

        :param inv_tag:
        """
        super().__init__(
            tags_to_dict(inv_tag=inv_tag)
        )

    def __setitem__(self, key, item) -> None:
        """
            定义【对字典项赋值】时要执行的方法
            （即当使用诸如 `tags[key] = item` 时会调用此方法），
            这里重写父类 `UserDict` 中相应的方法。

        :param key:
        :param item:
        :return:
        """
        # 在向字典中插入新项之前
        # 检查待插入项是否为【字符串类型】
        # 如果待插入项不符合条件，则会抛出异常
        if not isinstance(item, str) \
                and item is not None:
            raise TypeError(
                f"主机清单标签内容必须是字符串，"
                f"但接收到: {type(item).__name__}。"
            )
        # 如果项目检查通过
        # 则调用父类 `UserDict` 的 `__setitem__` 方法
        # 将【键值对】添加到字典中
        super().__setitem__(key, item)

    def __str__(self) -> str:
        """
            将字典对象转换为特定格式的字符串表示。

            此方法重写字典类的 `__str__` 方法，
            用于生成一个包含所有键值对的字符串，
            其中键值对以 "key=value" 的形式表示，
            如果值为空，则仅显示键名。

            各个键值对之间通过英文分号进行分隔。

            如果字典非空，生成的字符串末尾会附加一个分号。

            这种格式特别适用于需要将键值对作为参数
            传递给一些命令行工具或脚本时，
            提供一种简洁明了的表现方式。

        :return: 表示字典中所有键值对的字符串，
        如果字典为空，则返回空字符串。
        """
        # 当创建继承自 `collections.UserDict` 的类后
        # 会出现从 `UserDict` 类继承来的【`self.data`】
        # 它会自动提供一个称为【`data`】的属性以用于存储所有键值对
        # 任何对字典操作的方法都会影响到 `self.data`
        tags = r";".join(
            f"{k}={v}"
            if v else k
            for k, v in self.data.items()
        )
        return tags + r";" if self.data else ""


"""
    在 zbx 5.0/6.0 版本中，
    主机标签（Host Tags）是为了更好地
    组织和识别主机而引入的一种【元数据】。

    一个标签包含【键】（key）和【值】（value）对，
    这对于过滤和搜索特定的主机非常有用。

    在 zbx 的界面或 API 中，
    一个完整的主机标签可能会以这样的格式显示：
        [
            {
                "tag": "Environment",
                "value": "Production"
            },
            {
                "tag": "Role",
                "value": "WebServer"
            }
        ]

    每个对象代表一个标签，其中包含两部分：
        - "tag" : 这是【键名】，表示【标签名称】。

        - "value" : 这是与键名相关联的【值】。
"""


class HostTags:
    """
        主机标签的添加仅限于手动配置的主机（不包含自动发现主机），
        并且需要满足特定的 zbx 版本要求。

        在 zbx 5.0/6.0 版本中，Host 支持 tag 功能。

        与此相关的类和方法主要负责对 Host tag 进行新增和删除操作。

        这些操作使得对于 Host 的标签管理更加灵活有效，
        可以根据需要轻松添加或移除特定的标签信息。

        这是与旧版本相比的一大改进，
        为用户提供更高级的配置选项和更细致的资源管理能力。

        示例:
            >>> tags = [
            >>>     {
            >>>         "tag": "webserver",
            >>>         "value": "nginx",
            >>>         "automatic": True
            >>>     },
            >>>     {
            >>>         "tag": "database",
            >>>         "value": "mysql"
            >>>     }
            >>> ]
            >>> host_tags = HostTags(tags)

            - 获取格式化后的标签列表：
                >>> print(
                >>>     host_tags.filtered_tags
                >>> )
                [
                    {
                        "tag": "webserver",
                        "value": "nginx"
                    },
                    {
                        "tag": "database",
                        "value": "mysql"
                    }
                ]

            - 检查是否存在特定名称的标签：
                >>> print(
                >>>     host_tags.has_tag(tag_name="webserver")
                >>> )
                True

            - 添加一个新的标签：
                >>> print(
                >>>     host_tags.add_tag("cache", "redis")
                >>> )
                [
                    {
                        "tag": "webserver",
                        "value": "nginx"
                    },
                    {
                        "tag": "database",
                        "value": "mysql"
                    },
                    {
                        "tag": "cache",
                        "value": "redis"
                    }
                ]

            - 删除一个特定名称的标签：
                >>> print(
                >>>     host_tags.delete_tag("database")
                >>> )
                [
                    {
                        "tag": "webserver",
                        "value": "nginx"
                    },
                    {
                        "tag": "cache",
                        "value": "redis"
                    }
                ]
    """

    def __init__(self, tags: Optional[List[dict]]) -> None:
        """
            初始化 zbx 主机标签对象实例。

        :param tags: 用于接收一个字典列表，
        每个字典代表一个标签。
        """
        self._tags = tags

    @property
    def filtered_tags(self) -> List[dict]:
        """
            此函数用于构建更新 zbx 主机信息所需的数据结构。

            关于去除 Host tag 字典中 "automatic" 键：
                一个 Host 的 tag 字典可能包含三个关键字段：
                "tag"、"value" 以及 "automatic"。

                当通过 zbx API 操作 Host tag 时，
                `tag` 字典中不能包含 "automatic" 字段，
                否则操作会因错误而失败。

                (
                    在 zbx 6.0 版版本中，
                    一个主机的标签中的 "automatic" 字段表示
                    该标签是否是【自动添加】的。

                    如果 "automatic" 的值为 `True`，
                    这意味着该标签是由系统自动识别或通过某些规则、
                    模板或发现规则自动分配给主机的，
                    而不是由用户手动添加。

                    自动标签允许 zbx 根据主机的某些属性
                    或者监控数据自动生成和分配标签，
                    这样能够使得对主机进行分类和管理更加便捷，
                    并且可以在触发器、报警通知等地方
                    使用这些标签来实现更细粒度的控制。

                    例如，在监控服务器时，
                    zbx 可能会根据服务器上运行的服务（比如 Nginx、Apache 等）
                    自动添加相应的标签（如 "webserver": "nginx"），
                    将其作为服务类型识别并将其与其他相关监控项关联起来。

                    这样做有助于更有效地组织和过滤监控目标以及相关报警信息。
                )

        :return:
        """
        return [
            {
                k: v
                for k, v in tag.items()
                if k != "automatic"
            }
            for tag in self._tags
            if self._tags
        ]

    def has_tag(
            self,
            tag_name: str
    ) -> bool:
        """
            检查当前 Host Tags 列表中是否存在指定的标签。

        :param tag_name: 要检查的标签名称。
        :return: 如果指定的标签存在于 Host Tags 中，
        则返回 True；否则返回 False。
        """
        return any(
            tag.get("tag") == tag_name
            for tag in self._tags
        )

    def _set_tag(
            self,
            name: str,
            value: Union[str, int, None]) -> None:
        """
            设置指定标签的值。

            如果标签存在且值与当前不同，则更新该标签的值；
            如果标签不存在，则不执行任何操作。

        :param name: 标签名称。
        :param value: 要设置的新值，
        可以是字符串、整数或 None。
        """
        for tag in self._tags:
            if tag.get("tag") == name:
                if tag.get("value") != value:
                    tag["value"] = value
                break

    @staticmethod
    def _prepare_tags(
            tag_name: Union[str, List[str]],
            tag_value: Union[str, int, List[Union[str, int]], None]
    ) -> List[Tuple[str, Union[str, int]]]:
        """
            准备标签名称和值用于更新或添加。

            首先将标签名称和值转换为列表形式，
            并确保它们的数量相匹配。

            如果数量不一致，则抛出 `TypeError` 异常。

        :param tag_name: 单个标签名称或多个标签名称列表。
        :param tag_value: 单个标签值或多个标签值列表。
        :return: 返回一个包含 `(名称, 值)` 元组的列表。
        """
        tag_names = to_list(tag_name)
        tag_values = to_list(tag_value)
        if len(tag_names) != len(tag_values):
            raise TypeError(
                f"请确保传入的标签名称和值的数量是匹配的。"
                f"发现传入的标签名称 {tag_names} "
                f"和对应的值 {tag_values} 数量不一致，"
                f"请检查后再试。"
            )
        return list(zip(tag_names, tag_values))

    def update_tag(
            self,
            tag_name: Union[str, List[str]],
            tag_value: Union[str, int, List[Union[str, int]], None]
    ) -> List[dict] or None:
        """
            更新一个或多个标签的值，并返回更新后的标签列表。

            如果传入的是单个标签名称和值，将只更新该标签；
            如果传入的是列表形式的多个名称和值，
            将逐一更新这些标签。

            请注意，此函数仅用于更新字典中已存在的键。

            如果传入的键原本不在标签字典中，
            该函数并不会自动添加这些新键，而是会忽略它们并抛出错误信息。

            这样的设计是为了将其功能与 "add_tag" 函数区分开来。

            此外，"更新" 的操作意味着只修改现有信息，
            而不添加新信息。

            如果需要新增标签，请使用 "add_tag" 函数。

        :param tag_name: 单个或多个要更新的标签名称。
        :param tag_value: 相应要更新的单个或多个值。
        :return: 更新后得到的标签字典列表，
        或者在没有需要更新的情况下返回 None。
        """
        existing_tags = {
            tag.get("tag")
            for tag in self._tags
        }
        not_in_tags = {
            tag
            for tag in to_list(value=tag_name)
            if tag not in existing_tags
        }
        if not_in_tags:
            raise TypeError(
                f"以下需要更新的键并不在原标签列表中："
                f"\"{','.join(not_in_tags)}\"。"
            )
        zipped_tags = self._prepare_tags(
            tag_name=tag_name,
            tag_value=tag_value
        )
        for name, value in zipped_tags:
            self._set_tag(
                name=name,
                value=value
            )
        return self.filtered_tags

    def add_tag(
            self,
            tag_name: Union[str, List[str]],
            tag_value: Union[str, int, List[Union[str, int]], None]
    ) -> List[dict]:
        """
            向 Host Tags 对象中添加一个或多个新的标签，
            并返回更新后得到的标签字典列表。

            若给定名称的标签已存在，则只更新其对应值；
            若不存在，则在 Host Tags 中新增该名称和对应值组成的新标签项。

        :param tag_name: 要添加或更新的单个或多个标签名称，
        可以是字符串也可以是字符串列表形式。
        :param tag_value:
        设置给相应标签名称(tag_name)的值，
        可以是字符串、整数，或者它们的组合组成的列表。
        :return: 添加新标签后的 Host Tags 的字典列表。
        """
        zipped_tags = self._prepare_tags(
            tag_name=tag_name,
            tag_value=tag_value
        )
        existing_tags = {
            tag.get("tag")
            for tag in self._tags
        }
        for name, value in zipped_tags:
            if name in existing_tags:
                self._set_tag(
                    name=name,
                    value=value
                )
            else:
                self._tags.append(
                    {
                        "tag": name,
                        "value": value
                    }
                )
        return self.filtered_tags

    def delete_tag(
            self,
            tag_name: Union[str, List[str]]
    ) -> List[dict]:
        """
            从 Host Tags 中删除指定的标签，
            并返回更新后的标签字典列表。

        :param tag_name: 要删除的标签名称。
        :return: 删除指定标签后的 Host Tags 列表。
        """
        # 集合比列表查找快因为集合用哈希表
        # 时间复杂度 O(1)，而列表 O(n)
        # 大量删除时，使用集合提升性能
        tag_set = set(to_list(tag_name))
        self._tags = list(
            filter(
                lambda tag: tag.get("tag") not in tag_set,
                self._tags
            )
        )
        return self.filtered_tags


"""
    zbx 5.0/6.0 版本中 item tag 的格式要求是相对简单的。

    在 zbx 中，
    item tag 被用来帮助组织和管理监控项（items）、
    触发器（triggers）、事件（events）等。

    在 zbx 5.0/6.0 中，当创建或编辑一个监控项时，
    可以为其添加 tag。

    tag 由两个部分组成：
        - 【Tag 名称】：这是标识 tag 的键或者名称。
          例如，"Service"、"Environment" 等。

        - 【Tag 值】：这是与 tag 名称关联的值。

    例如，对于 "Service"，
    值可以是 "WebServer"、"Database" 等；

    对于 "Environment"，
    值可以是 "Production"、"Testing" 等。

    在 zbx 的前端界面中，
    添加 tag 的地方通常有两个字段：
    "Tag" 和 "Value"。

    当为 item 添加 tag 时，应该遵循如下格式：
        {
            "tag": <Tag 名称>,
            "value": <Tag 值>
        }

    示例：
        {
            "tag": "Service",
            "value": "WebServer"
        }
        {
            "tag": "Environment",
            "value": "Production"
        }
        {
            "tag": "Role",
            "value": "Frontend"
        }

    这些 tags 可以用来过滤和搜索监控项、触发器或者事件，
    并且可以在不同的报告和视图中使用。
"""


class ItemTags(HostTags):
    """
        代表与【监控项】关联的标签的类，派生自 `HostTags` 类。

        `ItemTags` 的结构和操作方式与 `HostTags` 高度相似，
        因此它直接继承自 `HostTags`。

        该类中的方法基本不需要修改，
        因为它们已经很好地适应 `ItemTags` 的需求。
    """

    def __init__(self, item_tags: Optional[List[dict]]) -> None:
        """
        :param item_tags:
        """
        super().__init__(tags=item_tags)
