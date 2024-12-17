#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2024/12/16 4:01 PM
@Desc    :  main line.
"""
from sharpshot.error import MissingParameterError
from sharpshot.run import sharp_shot
from sharpshot.tools import cli_env_new


def main():
    cli_param = cli_env_new()
    pr = cli_param.get("pr")
    username = cli_param.get("username")

    if pr is None:
        raise MissingParameterError("pr")
    if username is None:
        raise MissingParameterError("username")

    sharp_shot(pr, username, cli_param.get("access_token", None))
