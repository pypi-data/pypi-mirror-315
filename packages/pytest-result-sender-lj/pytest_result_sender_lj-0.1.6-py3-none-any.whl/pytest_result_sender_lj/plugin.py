# -*- coding: utf-8 -*-
"""
@Time ： 2024/12/14 12:55
@Auth ： Jin Lyu
@File ：plugin.py
@IDE ：PyCharm
@Describe: ...
"""
import time
from datetime import datetime

import pytest
import requests

data = {"passed": 0, "failed": 0}


def pytest_addoption(parser):
    parser.addini(
        "send_when",
        help="发送测试结果的时机，every表示每次执行发送，on_fail表示当失败时发送",
    )
    parser.addini("send_api", help="发送测试结果发往哪里")
    parser.addini("report_dir", help="测试报告地址，可动态配置")


# 统计成功/失败的用例数量
def pytest_runtest_logreport(report: pytest.TestReport):
    # print(report)
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含所有的用例
    data["total"] = len(session.items)
    # print('用例的总数：', data['total'])


def pytest_configure(config: pytest.Config):
    # 配置加载完毕之后执行，测试用例执行之前执行
    data["start_time"] = datetime.now()
    # print(f"{datetime.now()} pytest 开始执行")
    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")


def pytest_unconfigure(config: pytest.Config):
    # 配置卸载完毕之后执行，所有测试用例执行之后执行
    data["end_time"] = datetime.now()
    # print(f"{datetime.now()} pytest 结束执行")
    data["duration"] = data["end_time"] - data["start_time"]
    data["duration"] = data["duration"].total_seconds()
    data["duration"] = f"{int(data['duration'] / 60)}分{int(data['duration'] % 60)}秒"
    data["passed_ratio"] = data["passed"] / data["total"] * 100
    data["passed_ratio"] = f"{data['passed_ratio']:.2f}%"

    data["report_dir"] = config.getini("report_dir")

    send_result()


def send_result():
    # 如果配置失败才发送，但实际没有失败，则不发送
    if data["send_when"] == "on_fail" and data["failed"] == 0:
        return
    # 如果没有配置发送地址，则不发送
    if not data["send_api"]:
        return

    url = data["send_api"]
    msg_body = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "自动化测试结果",
                    "content": [
                        [{"tag": "text", "text": f"测试时间: {data['end_time'].strftime('%Y-%m-%d %H:%M:%S')}"}],
                        [{"tag": "text", "text": f"用例数量: {data['total']}"}],
                        [{"tag": "text", "text": f"执行时长: {data['duration']}"}],
                        [{"tag": "text", "text": f"测试通过: {data['passed']} "}],
                        [{"tag": "text", "text": f"测试失败: {data['failed']} "}],
                        [
                            {
                                "tag": "text",
                                "text": f"测试通过率：{data['passed_ratio']}",
                            }
                        ],
                        [{"tag": "text", "text": f"测试报告地址：{data['report_dir']}"}],
                    ],
                }
            }
        },
    }
    try:
        requests.post(url, json=msg_body)
    except Exception as e:
        print(e)

    data["send_done"] = 1
