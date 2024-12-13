import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from datetime import datetime

import mns_common.constant.db_name_constant as db_name_constant
import mns_scheduler.finance.em_financial_profit_sync_service_api as em_financial_profit_sync_service_api
from mns_common.db.MongodbUtil import MongodbUtil
from loguru import logger
import \
    mns_scheduler.finance.em_financial_asset_liability_sync_service_api as em_financial_asset_liability_sync_service_api
import mns_scheduler.risk.financial_report_risk_check_api as financial_report_risk_check_api
import mns_common.utils.data_frame_util as data_frame_util
import mns_scheduler.finance.finance_common_api as finance_common_api
import mns_scheduler.risk.compliance.undisclosed_annual_report_api as undisclosed_annual_report_api

mongodb_util = MongodbUtil('27017')


# 上市公司年报披露时间:每年1月1日一- 4月30日。
# 2、上市公司中年报披露时间:每年7月1日--8月30日。
# 3、上市公司季报披露时间:
#    1季报:每年4月1日-- -4月30日。
#    2季报(中报) :每年7月1日--8月30日。
#    3季报:每年10月1日--10月31日4季报(年报) :每年1月1日--4月30日

def sync_financial_report():
    now_date = datetime.now()
    now_year = now_date.year
    now_month = now_date.month
    sync_time = now_date.strftime('%Y-%m-%d %H:%M:%S')
    # 年报
    if 1 <= now_month <= 5:
        period = 4
        period_time = str(now_year - 1) + "-12-31 00:00:00"
        sync_profit_report(period_time, sync_time, period)
        sync_asset_liability_report(period_time, sync_time, period)

    # 一季报
    elif now_month == 5:
        period = 1
        period_time = str(now_year) + "-03-31 00:00:00"
        sync_profit_report(period_time, sync_time, period)
        sync_asset_liability_report(period_time, sync_time, period)

    # 二季报
    elif 7 <= now_month <= 8:
        period = 2
        period_time = str(now_year) + "-06-30 00:00:00"
        sync_profit_report(period_time, sync_time, period)
        sync_asset_liability_report(period_time, sync_time, period)
    # 三季报
    elif now_month == 10:
        period = 3
        period_time = str(now_year) + "-09-30 00:00:00"
        sync_profit_report(period_time, sync_time, period)
        sync_asset_liability_report(period_time, sync_time, period)
    # 未出报告check
    undisclosed_annual_report_api.un_disclosed_report_check(sync_time, now_year, period, period_time)
    # 新股或者未出报告的
    sync_miss_report(sync_time)


# 同步资产表
def sync_asset_liability_report(period_time, sync_time, period):
    un_report_asset_df = finance_common_api.find_un_report_symbol(period_time,
                                                                  db_name_constant.EM_STOCK_ASSET_LIABILITY)
    for un_report_asset_one in un_report_asset_df.itertuples():
        try:
            symbol = un_report_asset_one.symbol
            new_asset_df = em_financial_asset_liability_sync_service_api.get_em_asset_liability_api(symbol)
            # 负债比
            new_asset_df['liability_ratio'] = round(
                new_asset_df['TOTAL_LIABILITIES'] * 100 / new_asset_df['TOTAL_ASSETS'],
                2)
            new_asset_df['sync_time'] = sync_time
            if data_frame_util.is_empty(new_asset_df):
                continue
            new_asset_df['symbol'] = symbol
            mongodb_util.insert_mongo(new_asset_df, db_name_constant.EM_STOCK_ASSET_LIABILITY)

            # 年报审核
            financial_report_risk_check_api.financial_report_check(new_asset_df, period_time, period,
                                                                   db_name_constant.EM_STOCK_ASSET_LIABILITY)

        except Exception as e:
            logger.error("同步资产表异常:{},{},{}", symbol, period_time, e)


# 同步利润表
def sync_profit_report(period_time, sync_time, period):
    un_report_profit_df = finance_common_api.find_un_report_symbol(period_time, db_name_constant.EM_STOCK_PROFIT)
    for un_report_profit_one in un_report_profit_df.itertuples():
        try:
            symbol = un_report_profit_one.symbol
            new_profit_df = em_financial_profit_sync_service_api.get_em_profit_api(symbol)
            if data_frame_util.is_empty(new_profit_df):
                continue
            new_profit_df['sync_time'] = sync_time

            new_profit_df['symbol'] = symbol
            mongodb_util.insert_mongo(new_profit_df, db_name_constant.EM_STOCK_PROFIT)

            # 年报审核
            financial_report_risk_check_api.financial_report_check(new_profit_df, period_time,
                                                                   period, db_name_constant.EM_STOCK_PROFIT)
        except Exception as e:
            logger.error("同步利润表异常:{},{},{}", symbol, period_time, e)


def sync_miss_report(sync_time):
    query = {"total_operate_income": 0}
    un_report_company_info = mongodb_util.find_query_data(db_name_constant.COMPANY_INFO, query)
    for un_report_one in un_report_company_info.itertuples():
        try:
            symbol = un_report_one.symbol
            new_profit_df = em_financial_profit_sync_service_api.get_em_profit_api(symbol)
            if data_frame_util.is_empty(new_profit_df):
                continue
            new_profit_df['sync_time'] = sync_time

            new_profit_df['symbol'] = symbol
            mongodb_util.insert_mongo(new_profit_df, db_name_constant.EM_STOCK_PROFIT)

            new_asset_df = em_financial_asset_liability_sync_service_api.get_em_asset_liability_api(symbol)
            # 负债比
            new_asset_df['liability_ratio'] = round(
                new_asset_df['TOTAL_LIABILITIES'] * 100 / new_asset_df['TOTAL_ASSETS'],
                2)
            new_asset_df['sync_time'] = sync_time
            if data_frame_util.is_empty(new_asset_df):
                continue
            new_asset_df['symbol'] = symbol
            mongodb_util.insert_mongo(new_asset_df, db_name_constant.EM_STOCK_ASSET_LIABILITY)

        except Exception as e:
            logger.error("同步财报补偿任务异常:{},{},{}", symbol, e)


if __name__ == '__main__':
    now_date = datetime.now()
    now_year = now_date.year
    now_month = now_date.month
    sync_time_test = now_date.strftime('%Y-%m-%d %H:%M:%S')
    sync_miss_report(sync_time_test)
