"""Database"""
# Column, Table, MetaData API
#     https://docs.sqlalchemy.org/en/14/core/metadata.html#column-table-metadata-api
# CursorResult
#     https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult
# PostgreSQL 14 Data Types
#     https://www.postgresql.org/docs/14/datatype.html
import csv
from typing import Any

from loguru import logger
from sqlalchemy import CursorResult, Index, create_engine, text
from sqlalchemy.orm import DeclarativeBase

from . import utils


class Database():
    """Database"""

    engine = create_engine('sqlite://')

    def __init__(self, target: str | None = None, **options):
        """Initiation"""
        if isinstance(target, str) and utils.isTrue(target, str):
            if utils.isTrue(options, dict):
                self.engine = create_engine(target, **options)
            else:
                self.engine = create_engine(target)
        else:
            pass

    def initializer(self):
        """ensure the parent proc's database connections are not touched in the new connection pool"""
        self.engine.dispose(close=False)

    def connect_test(self) -> bool:
        info = "Database connect test"
        try:
            logger.info(f"{info} ......")
            self.engine.connect()
            logger.success(f"{info} [success]")
            return True
        except Exception as e:
            logger.error(f"{info} [failure]")
            logger.exception(e)
            return False

    def metadata_init(self, base: DeclarativeBase, **kwargs) -> bool:
        # https://stackoverflow.com/questions/19175311/how-to-create-only-one-table-with-sqlalchemy
        info = "Database init table"
        try:
            logger.info(f"{info} ......")
            base.metadata.drop_all(self.engine, **kwargs)
            base.metadata.create_all(self.engine, **kwargs)
            logger.success(f"{info} [success]")
            return True
        except Exception as e:
            logger.error(f"{info} [failure]")
            logger.exception(e)
            return False

    def create_index(self, index_name, table_field) -> bool:
        # 创建索引
        #   https://stackoverflow.com/a/41254430
        # 示例:
        #   index_name: a_share_list_code_idx1
        #   table_field: Table_a_share_list.code
        info = "Database create index"
        try:
            logger.info(f"{info} ......")
            idx = Index(index_name, table_field)
            try:
                idx.drop(bind=self.engine)
            except Exception as e:
                logger.exception(e)
            idx.create(bind=self.engine)
            logger.success(f'{info} [success]')
            return True
        except Exception as e:
            logger.error(f'{info} [failure]')
            logger.error(e)
            return False

    # 私有函数, 保存 execute 的结果到 CSV 文件
    def _result_save(self, file, data) -> bool:
        try:
            outcsv = csv.writer(file)
            outcsv.writerow(data.keys())
            outcsv.writerows(data)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def execute(
        self,
        sql: str | None = None,
        sql_file: str | None = None,
        sql_file_kwargs: dict | None = None,
        csv_file: str | None = None,
        csv_file_kwargs: dict | None = None
    ) -> CursorResult[Any] | bool:
        """"运行"""

        # ------------------------------------------------------------

        # 提取 SQL
        # 如果 sql 和 sql_file 同时存在, 优先执行 sql

        sql_object = None

        info: str = f"""Extract SQL: {sql}"""

        try:

            logger.info(f"{info} ......")

            if utils.isTrue(sql, str):

                sql_object = sql

            elif sql_file is not None and utils.isTrue(sql_file, str):

                # 判断文件是否存在
                if isinstance(sql_file, str) and utils.check_file_type(sql_file, "file") is False:

                    logger.error(f"No such file: {sql_file}")
                    return False

                if isinstance(sql_file, str) and utils.isTrue(sql_file, str):

                    # 读取文件内容
                    if sql_file_kwargs is not None and utils.isTrue(sql_file_kwargs, dict):
                        with open(sql_file, "r", encoding="utf-8", **sql_file_kwargs) as _file:
                            sql_object = _file.read()
                    else:
                        with open(sql_file, "r", encoding="utf-8") as _file:
                            sql_object = _file.read()

            else:

                logger.error("SQL or SQL file error")
                logger.error(f"{info} [failure]")
                return False

            logger.success(f'{info} [success]')

        except Exception as e:

            logger.error(f"{info} [failure]")
            logger.exception(e)
            return False

        # ------------------------------------------------------------

        # 执行 SQL

        info = f"""Execute SQL: {sql_object}"""

        try:

            logger.info(f"{info} ......")

            with self.engine.connect() as connect:

                # 执行SQL
                if sql_object is None:
                    return False

                result = connect.execute(text(sql_object))

                connect.commit()

                if csv_file is None:
                    # 如果 csv_file 没有定义, 则直接返回结果
                    logger.success(f'{info} [success]')
                    return result

                # 如果 csv_file 有定义, 则保存结果到 csv_file
                info_of_save = f"Save result to file: {csv_file}"
                logger.info(f"{info_of_save} .......")

                # 保存结果
                if isinstance(csv_file_kwargs, dict) and utils.isTrue(csv_file_kwargs, dict):
                    with open(csv_file, "w", encoding="utf-8", **csv_file_kwargs) as _file:
                        result_of_save = self._result_save(_file, result)
                else:
                    with open(csv_file, "w", encoding="utf-8") as _file:
                        result_of_save = self._result_save(_file, result)

                # 检查保存结果
                if result_of_save is True:
                    logger.success(f'{info_of_save} [success]')
                    logger.success(f'{info} [success]')
                    return True

                logger.error(f"{info_of_save} [failure]")
                logger.error(f"{info} [failure]")
                return False

        except Exception as e:

            logger.error(f'{info} [failure]')
            logger.exception(e)
            return False
