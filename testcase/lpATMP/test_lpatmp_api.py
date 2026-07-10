import allure
import pytest
import yaml

from base.apiutil import RequestBase
from base.generateId import m_id, c_id


def load_cases(file):
    """
    加载多接口 yaml 用例文件（一个文件含多个 baseInfo 块），
    拆分为 [(base_info, 单条testCase), ...] 参数对，供 pytest.mark.parametrize 使用。
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    cases = []
    for item in data:
        base_info = item['baseInfo']
        for tc in item['testCase']:
            cases.append([base_info, tc])
    return cases


@allure.feature(next(m_id) + '智驾测试管理平台-车辆管理模块')
class TestVehicle:

    @allure.story(next(c_id) + "车辆管理接口")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', load_cases("./testcase/lpATMP/vehicle.yaml"))
    def test_vehicle(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


@allure.feature(next(m_id) + '智驾测试管理平台-测试记录模块')
class TestRecord:

    @allure.story(next(c_id) + "测试记录接口")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', load_cases("./testcase/lpATMP/test_record.yaml"))
    def test_record(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


@allure.feature(next(m_id) + '智驾测试管理平台-借用管理模块')
class TestBorrow:

    @allure.story(next(c_id) + "借用管理接口")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', load_cases("./testcase/lpATMP/borrow.yaml"))
    def test_borrow(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)
