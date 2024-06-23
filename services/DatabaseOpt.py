from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from entity.OptionData import OptionData


class DatabaseOpt:
    def __init__(self):
        # 定义固定的数据库连接信息
        self.databases = {
            'primary_db': "postgresql://postgres:postgres@localhost:5432/postgres",
        }
        self.engines = {alias: create_engine(conn_str) for alias, conn_str in self.databases.items()}
        self.sessionmakers = {alias: sessionmaker(bind=engine) for alias, engine in self.engines.items()}
        self.sessions = {}

    def get_session(self, alias):
        """
        获取指定数据库的session
        :param alias: 数据库别名
        :return: session对象
        """
        if alias not in self.sessions:
            self.sessions[alias] = self.sessionmakers[alias]()
        return self.sessions[alias]

    def execute_sql(self, alias, sql, params=None):
        """
        执行SQL语句，并处理事务
        :param alias: 数据库别名
        :param sql: 要执行的SQL语句
        :param params: SQL语句的参数
        """
        session = self.get_session(alias)
        try:
            result = session.execute(sql, params or {})
            session.commit()
            if 'INSERT' in sql.text.upper():
                print("Insert statement detected, not fetching scalars.")
                return None
            else:
                return result.all()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise
        finally:
            # 关闭session
            session.close()


if __name__ == "__main__":
    db = DatabaseOpt()

    # 执行一个查询示例，指定使用primary_db
    try:
        # result=db.execute_sql('primary_db', text("insert into option_data (code, name,create_time) values ('33234234', 'none name is',now() at time zone 'PRC');"))
        result = db.execute_sql('primary_db', text("select * from option_data;"))
        if result is not None:
            for row in result:
                option_data = OptionData(*row)
                print(option_data)
    except Exception as e:
        print(f"An error occurred during SQL execution: {e}")

    # 执行一个查询示例，指定使用primary_db
    try:
        db.execute_sql('primary_db', text(
            "insert into processed_codes (code, create_time) values ('0100056', now() at time zone 'PRC');"))
        result = db.execute_sql('primary_db', text("select * from processed_codes;"))
        if result is not None:
            for row in result:
                print(row)
    except Exception as e:
        print(f"An error occurred during SQL execution: {e}")
