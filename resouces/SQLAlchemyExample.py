from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class OptionDataEx(Base):
    __tablename__ = 'option_data'

    id = Column(BigInteger, primary_key=True)
    code = Column(String)
    name = Column(String)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    update_time = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return (f"OptionData(id={self.id}, code={self.code}, name={self.name}, "
                f"create_time={self.create_time}, update_time={self.update_time})")


def get_option_data_by_code(code):
    session = SessionLocal()
    try:
        # 使用ORM方式执行查询
        option_data = session.query(OptionDataEx).filter(OptionDataEx.code == code).first()
        return option_data
    finally:
        session.close()

def get_all_option_data():
    session = SessionLocal()
    # 查询所有OptionData记录
    return session.query(OptionDataEx).all()

def insert_option_data(code, name):
    session = SessionLocal()
    new_option = OptionDataEx(code=code, name=name, create_time=func.now())
    session.add(new_option)
    session.commit()

def update_option_data(code, updated_name):
    session = SessionLocal()
    option = session.query(OptionDataEx).filter(OptionDataEx.code == code).first()
    if option:
        option.name = updated_name
        session.commit()
    else:
        print(f"No data found with code: {code}")

def delete_option_data(code):
    session = SessionLocal()
    option = session.query(OptionDataEx).filter(OptionDataEx.code == code).first()
    if option:
        session.delete(option)
        session.commit()
    else:
        print(f"No data found with code: {code}")

if __name__ == "__main__":

    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # 这将根据定义的实体类创建表，如果表不存在的话

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 示例查询
    example_code = 'SOME_CODE'
    option_data = get_option_data_by_code("13576")
    if option_data:
        print(option_data)
    else:
        print("No data found for the given code.")

    all_option_data = get_all_option_data()
    for option in all_option_data:
        print(option)
