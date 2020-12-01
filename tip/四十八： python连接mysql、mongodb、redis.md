# python连接mysql/mongodb/redis
### 1. 连接mysql数据库(pymysql和sqlalchemy) -- 

	通过pymysql连接mysql数据库:

	    import pymysql
	    host = '127.0.0.1'
	    port = 3306
	    user = 'root'
	    password = '123456'
	    database = 'mogujie'  # mysql中数据库的名字
	    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)  # 建立连接
	    cursor = db.cursor()  # 获取游标对象
	    sql = "select * from table_goods where id=1;"  # 需要执行的sql
	    sql1 = "insert into table_goods (name,price) values (%s,%s)"  # 需要执行的sql
	    cursor.execute(sql,("shoes",100))  # 执行sql
	    db.commit()  # 提交事务
	    db.close()  # 关闭连接

    通过sqlalchemy建立model连接数据库：

	    from sqlalchemy.orm import sessionmaker
	    from sqlalchemy import create_engine
		from sqlalchemy.ext.declarative import declarative_base

		Base = declarative_base()
		class Goods(Base):
		    __tablename__ = 'goods'   #映射的数据库表名
		    id = Column(Integer, primary_key=True, autoincrement=True)    # 主键自增
		    title = Column(String(128))
		    img = Column(String(1024))
		    price = Column(String(32))


        engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/mogujie?charset=utf8") # 建立连接
        Session = sessionmaker(bind=engine)  #Session()可以创建一个绑定到数据库的对象。但是到此为止，它还没有打开任何的连接
        session = Session  #当它第一次被调用的时候，会尝试从数据库引擎连接池中检索一个链接，该连接会一直被持有直到所有的任务都被提交或者Session对象被关闭
        goods = Goods()
        goods.title = '衣服'
		goods.img = '111.png'
		goods.price = '100'
        session.add(goods)
        session.commit()
### 2.连接mongodb数据库（pymongo/mongoengine）
		from pymongo import MongoClient
		client = MongoClient()  # client = MongoClient('mongodb://127.0.0.1:20719') 建立连接
		db = client.mogujie  # db = client['mogujie'] 获取数据库对象
		coll = db.goods  # coll = db['goods']  获取集合对象
		coll.insert_one({"name":'裤子'})  # 插入数据
		coll.insert_many([{'name':'裤子'},{'name':'衣服'}]) # 插入数据
		coll.find() # 查询所有数据
### 3.连接redis数据库
		import redis
		pool = redis.ConnectionPool(host='127.0.0.1',password='123456') # 实现一个连接池
		r = redis.Redis(connection_pool=pool)
		r.set('foo','bar')
		foo = r.get('foo')
		
		set(name, value, ex=None, px=None, nx=False, xx=False)
		　　在Redis中设置值，默认，不存在则创建，存在则修改
		　　参数：
		     　　ex，过期时间（秒）
		     　　px，过期时间（毫秒）
		     　　nx，如果设置为True，则只有name不存在时，当前set操作才执行
		     　　xx，如果设置为True，则只有name存在时，岗前set操作才执行