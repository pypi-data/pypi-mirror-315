import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from mns_common.db.MongodbUtil import MongodbUtil
from loguru import logger
import mns_scheduler.k_line.clean.k_line_info_clean_task as k_line_info_clean_task

mongodb_util = MongodbUtil('27017')


def clean_history_data():
    query = {"$and": [{"trade_date": {"$gte": '2023-11-06'}}, {"trade_date": {"$lte": '2024-05-29'}}]}
    trade_date_list_df = mongodb_util.find_query_data('trade_date_list', query)
    trade_date_list_df = trade_date_list_df.sort_values(by=['trade_date'], ascending=False)
    for trade_data_one in trade_date_list_df.itertuples():
        try:
            k_line_info_clean_task.sync_k_line_info_task(trade_data_one.trade_date)
            logger.info("清洗数据到:{}", trade_data_one.trade_date)
        except BaseException as e:
            logger.error("发生异常:{},{}", trade_data_one.trade_date, e)


if __name__ == '__main__':
    # 001389  001359
    k_line_info_clean_task.sync_k_line_info('2024-07-12', ['300784'])
    # clean_history_data()
