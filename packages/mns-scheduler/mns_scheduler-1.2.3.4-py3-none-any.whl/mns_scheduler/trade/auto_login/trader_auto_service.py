import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.component.deal.deal_service_api as deal_service_api
from mns_common.component.deal.terminal_enum import TerminalEnum
import time


# qmt 自动登录
def qmt_auto_login():
    deal_service_api.auto_login(TerminalEnum.QMT.terminal_code)


# 同花顺自动登陆
def ths_auto_login():
    deal_service_api.auto_login(TerminalEnum.EASY_TRADER.terminal_code)


def auto_login():
    qmt_auto_login()
    time.sleep(5)
    ths_auto_login()


if __name__ == '__main__':
    auto_login()
