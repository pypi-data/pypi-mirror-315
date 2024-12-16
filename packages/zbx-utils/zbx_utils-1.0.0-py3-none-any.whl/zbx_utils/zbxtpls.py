#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    此脚本旨在执行与【主机模板】相关的一系列操作。

    这些操作主要包括【添加新模板】、
    【删除现有模板】以及【替换当前模板】。

    通过使用此脚本，
    用户能够高效地管理 zbx 服务器上的主机模板，
    从而优化监控配置过程。

    ***重要的是要了解，虽然脚本聚焦于主机模板的管理任务，
    但它并不直接执行对 zbx 主机的修改操作。

    相反，脚本的作用是生成操作结果，并将这些结果返回给用户。

    用户可以根据这些结果，以及他们具体的需求和场景，
    决定如何进一步使用这些信息。

    因此，该脚本可以被视为一个辅助工具或功能性扩展，
    旨在为开发者或管理员提供更多灵活性和控制能力
    来维护和更新他们的监控系统配置。

    注意：本文档中出现的 "zbx"，如无特殊说明，则指代 "Zabbix"。
         本文档中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import sys
from pathlib import Path
import logging
from zabbix_api import ZabbixAPI, ZabbixAPIException
from typing import List, Dict, Optional, Union

# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性：
#     - 如果定义 `__all__`，那么【只有在这个列表中的属性才会被导入】
#     - 如果没有定义 `__all__`，那么默认【导入模块中不以下划线开头的所有属性】
__all__ = [
    "ZbxTpls"
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
from zbx_utils import to_list  # noqa: E402


class ZbxTpls:
    def __init__(
            self,
            server: str,
            user: str,
            passwd: str,
            timeout: int = 120,
            **kwargs) -> None:
        """
            初始化 `ZbxTpls` 类的新实例。

            参数:
                - `server`: zbx 服务器的 URL。

                - `user`: 用于登录 zbx 的用户名。

                - `passwd`: 用于登录 zbx 的密码。

                - `timeout`: 超时时间，默认为 `120` 秒。

                - `zapi`: 如果提供，
                  应该是一个已存在的 `ZabbixAPI` 实例。

            请注意，此初始化方法提供灵活性，
            它既可以通过接收用户名、
            密码等参数来创建 `ZabbixAPI` 实例，
            也可以直接接收一个现有的 `ZabbixAPI` 实例。

            这种设计考虑到实际应用中的需求，
            因为在多个场景下可能已经存在一个 `ZabbixAPI` 实例，
            在这种情况下无需重新创建新的实例，从而节省资源。

            但是，请确保传入的 `ZabbixAPI` 实例是由
            Python zabbix_api 包创建的有效实例。

        :param kwargs:
        """
        self._server = server
        self._user = user
        self._passwd = passwd
        self._timeout = timeout
        self._input_zapi = kwargs.get("zapi")
        self._zapi = None

    def __initialize_zapi(self) -> None:
        """
            初始化 zbx API 客户端。

            如果提供已存在的 `ZabbixAPI` 实例，
            将直接使用该实例；
            否则根据给定参数创建新的 `ZabbixAPI` 实例并登录。

            登录成功后，
            会将 `ZabbixAPI` 实例存储
            在 `self._zapi` 以供后续使用。

        :raises ZabbixAPIException:
        如果登录失败，则抛出异常。
        :return:
        """
        if isinstance(self._input_zapi, ZabbixAPI):
            self._zapi = self._input_zapi
        else:
            try:
                self._zapi = ZabbixAPI(
                    server=self._server,
                    timeout=self._timeout
                )
                self._zapi.validate_certs = False
                self._zapi.login(
                    user=self._user,
                    password=self._passwd
                )
            except ZabbixAPIException as err:
                logging.error(msg=str(err))

    @property
    def __zapi(self) -> ZabbixAPI:
        """
            获取或初始化 `ZabbixAPI` 对象。

            如果之前未初始化过 `ZabbixAPI` 实例，
            则调用 `_initialize_zapi` 方法进行初始化，
            并返回初始化后的 `ZabbixAPI` 对象。

            如果已经有现成的 `ZabbixAPI` 实例，
            则直接返回该实例。

        :return: 返回一个 `ZabbixAPI` 对象，
        用于进行后续的 zbx API 调用。
        """
        if not self._zapi:
            self.__initialize_zapi()
        return self._zapi

    def __get_host_tpls(self, host: str) \
            -> List[Dict]:
        """
            获取指定主机关联的所有模板信息。

        :param host: 指定要查询的主机名。
        :return: 返回一个包含该主机关联所有模板信息的列表。
        如果该主机不存在，则返回空列表。
        """
        host_info = self.__zapi.host.get(
            {
                "output": ["host"],
                "filter": {"host": [host]},
                "selectParentTemplates": ["host"]
            }
        )
        if not host_info:
            return []
        templates = host_info[0].get(
            "parentTemplates",
            []
        )
        return templates

    def __get_tpl(self, tpl_name: str) \
            -> dict or None:
        """
            根据模板名称获取模板详细信息。

        :param tpl_name: 要查询的模板名称。
        :return: 返回一个包含模板详细信息的字典。
        如果指定的模板在 zbx 中不存在，
        则抛出 `TypeError` 异常。
        """
        tpl = self.__zapi.template.get(
            {
                "output": ["host"],
                "filter": {"host": tpl_name}
            }
        )
        if not tpl:
            raise TypeError(
                f"模板 \"{tpl_name}\" 在 Zabbix 中不存在！"
            )
        return tpl[0]

    @staticmethod
    def has_tpl(
            tpl_name: str,
            host_tpls: List[Dict]) -> bool:
        """
            检查指定主机是否已关联特定模板。

        :param host_tpls:
        :param tpl_name: 模板名称。
        :return: 布尔值，如果主机已关联该模板则返回 True，
        否则返回 False。
        """
        return any(
            tpl.get("host") == tpl_name
            for tpl in host_tpls
        )

    def add_tpl(
            self,
            host: str,
            tpl_name: Optional[Union[str, List[str]]]
    ) -> List[Dict] or None:
        """
            向指定主机添加一个模板，并返回更新后的模板列表。

        :param host: 主机名称。
        :param tpl_name: 需要添加的模板名称，
        可以是单个模板名字符串或模板名列表。
        :return: 更新后的主机模板列表，
        包括所有已关联和新添加的模板信息；
        如果没有任何添加，则返回 None。
        """
        host_tpls = self.__get_host_tpls(host=host)
        # 创建一个集合来保存当前主机的所有模板名称
        existing_tpl_names = {
            tpl.get("host")
            for tpl in host_tpls
        }
        # 根据当前主机是否已经存在给定的模板名称
        # 决定是否需要获取新模板信息
        filtered_names = filter(
            lambda name: name not in existing_tpl_names,
            to_list(tpl_name)
        )
        # 使用 `map()` 函数对每个筛选出来的名称
        # 应用 `self.__get_tpl_info` 方法
        # 并使用 `list()` 将结果转换为列表
        new_tpls = list(
            map(self.__get_tpl, filtered_names)
        )
        # 如果有新模板，则将它们添加到现有模板列表中
        if new_tpls:
            final_host_tpls = host_tpls + new_tpls
            return final_host_tpls
        # 如果所有请求的模板都已存在
        # 则直接返回现有列表
        return host_tpls

    def delete_tpl(
            self,
            host: str,
            tpl_name: Optional[Union[str, List[str]]]
    ) -> List[Dict] or None:
        """
            从指定主机中移除一个或多个模板，
            并返回更新后的模板列表。

        :param host: 主机名称。
        :param tpl_name: 需要移除的模板名称或名称列表。
        :return: 更新后的主机模板列表，不再包括被移除的模板信息。
        如果没有更新，则返回 None。
        """
        host_tpls = self.__get_host_tpls(host=host)
        # 避免重复转换 `tpl_name` 到集合
        if not isinstance(tpl_name, set):
            tpl_names = set(to_list(tpl_name))
        # 当需要处理大量数据时使用 `filter()` 函数会更高效
        final_tpls = list(
            filter(
                lambda tpl: tpl.get("host") not in tpl_names,
                host_tpls
            )
        )
        return final_tpls if final_tpls else None

    def replace_tpl(
            self,
            host: str,
            old_tpl_name: str,
            new_tpl_name: str
    ) -> List[Dict] or None:
        """
            替换指定主机上的一个旧模板为新模板，
            并返回更新后的模板列表。

        :param host: 主机名称。
        :param old_tpl_name: 要被替换掉的旧模板名称。
        :param new_tpl_name: 新的替换进来的模板名称。
        :return:
        """
        host_tpls = self.__get_host_tpls(host=host)
        has_tpl = self.has_tpl(
            tpl_name=old_tpl_name,
            host_tpls=host_tpls
        )
        # 如果没有 `old` 模板
        # 则无需进行替换
        if not has_tpl:
            return host_tpls
        old_tpl_info = self.__get_tpl(tpl_name=old_tpl_name)
        new_tpl_info = self.__get_tpl(tpl_name=new_tpl_name)
        # 如果找到 `old` 模板信息也找到 `new` 模板信息
        # 则执行替换
        if old_tpl_info and new_tpl_info:
            remove_old_tpl = self.delete_tpl(
                host=host,
                tpl_name=old_tpl_name
            )
            final_tpls = remove_old_tpl + [new_tpl_info]
            return final_tpls
        # 如果没有找到相应模板信息
        # 则返回原始主机模板列表
        return host_tpls
