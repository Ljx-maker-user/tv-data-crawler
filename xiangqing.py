import pymysql
import pymysql.cursors



__all__ = [
    'select',
    'update'
]

def get_mysql_db():
    """
    获取MySQL数据库连接
    """
    try:
        # 建立数据库连接
        db = pymysql.connect(host='localhost', user='root', password='2636023', database='dsj')
        return db
    except Exception as e:
        print(f"数据库连接出错: {e}")

def select(sql, params=None):
    """查询数据"""
    try:
        db = get_mysql_db()
        cursor = db.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"查询数据出错: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def update(sql, params=None):
    """
    插入、修改、删除数据
    :param sql:
    :param params:
    :return:
    """
    try:
        db = get_mysql_db()
        cursor = db.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"查询数据出错: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:

            db.close()