from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import click


engine = create_engine('mysql://root:root123@127.0.0.1:3306/test')
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    import all modules here that might define models so that they will be registered properly on the metadata.
    Otherwise you will have to import them first before init_db()
    """
    from flaskr import models
    # 根据模板创建所有表格
    Base.metadata.create_all(bind=engine)


def shutdown_session(exception=None):
    """ 关闭session """
    db_session.remove()


@click.command('init-database')
def init_db_command():
    """ 定义 flask init-database 为初始化mysql数据库 """
    init_db()
    click.echo('Intialized mysql database!')


def init_app(app):
    # 添加当app结束时关闭session
    app.teardown_appcontext(shutdown_session)
    # 为app添加command
    app.cli.add_command(init_db_command)
