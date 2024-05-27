from sqlalchemy import Column, String, create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Laptop(Base):
    __tablename__ = 'laptops'

    name = Column(String, primary_key=True)
    price = Column(String)
    display_size = Column(String)
class SQLAlchemyPipeline(object):
    def __init__(self):
        db_uri = 'postgresql://postgres:password@url:5432'  # replace with your actual URI
        self.db_engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.db_engine)
        Base.metadata.drop_all(self.db_engine)  # Drop all tables
        Base.metadata.create_all(self.db_engine)  # Create all tables
        

    def close_spider(self, spider):
        self.db_engine.dispose()

    def process_item(self, item, spider):
        session = self.Session()
        metadata = MetaData()
        laptops = Table('laptops', metadata, autoload_with=self.db_engine)
        insert = laptops.insert().values(name=item['name'], price=item['price'], display_size=item['display_size'])
        session.execute(insert)
        session.commit()
        session.close()
        return item