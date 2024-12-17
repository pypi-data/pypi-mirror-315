#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2024/12/16 4:39 PM
@Desc    :  error line.
"""


class MissingParameterError(Exception):
    def __init__(self, parameter):
        self.parameter = parameter
        self.message = f"缺少必要的参数: {parameter}"
        super().__init__(self.message)
