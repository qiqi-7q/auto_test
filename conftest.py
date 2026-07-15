# -*- coding: utf-8 -*-
import time

import pytest

from common.readyaml import ReadYamlData
from base.removefile import remove_file
from common.dingRobot import send_dd_msg
from conf.setting import dd_msg

import warnings

yfd = ReadYamlData()


@pytest.fixture(scope="session", autouse=True)
def clear_extract():
    # 禁用HTTPS告警，ResourceWarning
    warnings.simplefilter('ignore', ResourceWarning)

    yfd.clear_yaml_data()
    remove_file("./report/temp", ['json', 'txt', 'attach', 'properties'])


def generate_test_summary(terminalreporter):
    """生成测试结果摘要字符串"""
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    try:
        duration = terminalreporter._session_duration.total_seconds()
    except AttributeError:
        start_time = terminalreporter._session_start
        try:
            duration = time.time() - float(start_time)
        except (TypeError, ValueError):
            duration = -1

    summary = f"""
    自动化测试结果，通知如下，请着重关注测试失败的接口，具体执行结果如下：
    测试用例总数：{total}
    测试通过数：{passed}
    测试失败数：{failed}
    错误数量：{error}
    跳过执行数量：{skipped}
    执行总时长：{duration}
    """
    print(summary)
    return summary


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """自动收集pytest框架执行的测试结果并打印摘要信息，推送钉钉通知"""
    summary = generate_test_summary(terminalreporter)

    # 尝试从Jenkins读取Allure报告链接（可选，失败不影响主流程）
    report_line = ''
    try:
        from conf.operationConfig import OperationConfig
        conf = OperationConfig()
        jenkins_enable = conf.get_section_jenkins('enable')
        if jenkins_enable == '1':
            from common.Pjenkins import PJenkins
            jk = PJenkins()
            jk_report = jk.report_success_or_fail()
            report_line = jk_report.get('report_line', '')
            summary += f"\n    Allure报告链接：{report_line}"
    except Exception as e:
        print(f"[Jenkins报告读取跳过] enable=0或服务不可达: {e}")

    if dd_msg:
        send_dd_msg(summary)
