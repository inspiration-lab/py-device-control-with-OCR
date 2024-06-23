from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OptionData(Base):
    __tablename__ = 'option_data'

    id = Column(BigInteger, primary_key=True)
    code = Column(String)
    name = Column(String)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)

    def __init__(self, id, code, name, create_time, update_time):
        self.id = id
        self.code = code
        self.name = name
        self.create_time = create_time
        self.update_time = update_time

    def __repr__(self):
        return (f"OptionData(id={self.id}, code={self.code}, name={self.name}, "
                f"create_time={self.create_time}, update_time={self.update_time})")
