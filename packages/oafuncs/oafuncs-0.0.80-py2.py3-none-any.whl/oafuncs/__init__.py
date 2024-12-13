#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 16:09:20
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-12-13 10:56:43
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\__init__.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

# 会导致OAFuncs直接导入所有函数，不符合模块化设计
from oafuncs.oa_s import (
    oa_cmap,
    oa_data,
    oa_draw,
    oa_file,
    oa_help,
    oa_nc,
    oa_python,
)

from .oa_down import *
from .oa_sign import *
from .oa_tool import *
