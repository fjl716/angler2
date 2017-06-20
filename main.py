import re
from time import sleep

import tornado
import yaml

from angler import Angler
import sys
import logging

# logging.basicConfig(level=logging.INFO,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 # filename='myapp.log',
#                 # filemode='w'
#                     )
from test import testAAA

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    file = open('angler.yaml')
    conf = yaml.load(file)
    file.close()

    angler = Angler(conf['angler_id'], conf['zookeeper']['hosts'])
    angler.start()
    while True:
        sleep(1)

    # from kazoo.client import KazooClient
    #
    # zk = KazooClient('127.0.0.1:2181')
    # zk.start()
    #
    # zk.ensure_path('/angler/equipment/00055DE80FA3/packets')
    # zk.ensure_path('/angler/equipment/00055DE80FA3/tasks')
    #
    # # print(zk.get_children('/angler/equipment/00055DE80FA3/packets'))
    # zk.create('/angler/equipment/00055DE80FA3/packets/', bytes('data', 'utf-8'), sequence=True)
    # zk.create('/angler/equipment/00055DE80FA3/packets/', bytes('data', 'utf-8'), sequence=True)
    #
    #
    # @zk.ChildrenWatch('/angler/equipment/00055DE80FA3/packets')
    # def children_callback(children):
    #     print(children)
    #     if len(children) > 0:
    #         print('delete {0}'.format(children[0]))
    #         zk.delete('/angler/equipment/00055DE80FA3/packets/{0}/'.format(children[0]))
    #     # for key in children:
    #     #     node = zk.get('/angler/equipment/{0}'.format(key))
    #     #     print(key, node[0])
    #
    #     # if len(children) > 0:
    #     #     return False
    #
    #
    # print('watch')
    # zk.create('/angler/equipment/00055DE80FA3/packets/', bytes('data', 'utf-8'), sequence=True)
    # print('add 1')
    # zk.create('/angler/equipment/00055DE80FA3/packets/', bytes('data', 'utf-8'), sequence=True)
    # print('add 2')

    # for children in zk.get_children('/angler/equipment'):
    #     zk.delete('/angler/equipment/{0}'.format(children))
    #     print(children)
    #     # return False
    #
    # # watch = ChildrenWatch(zk, '/angler/equipment', children_callback)
    #
    # zk.create('/angler/equipment/01equipment', bytes('1-1', 'utf-8'), sequence=True)
    # zk.create('/angler/equipment/02', bytes('2-1', 'utf-8'), sequence=True)
    # zk.create('/angler/equipment/01', bytes('1-2', 'utf-8'), sequence=True)
    # zk.create('/angler/equipment/02', bytes('2-2', 'utf-8'), sequence=True)


    # callback = {}
    # test = Test1(callback)
    # test.bind('equipment', 'channel')
    # callback['callback']('packet')
    # file = open("angler.yaml")
    # conf = yaml.load(file)
    # file.close()
    # angler = create_angler(conf)
    # angler.start()























    # from functools import partial
    # from time import sleep
    # from bson import ObjectId

    # from angler.angler import Angler
    # from angler.container import Container, Request, Response
    # from angler.events.database.mongo import event_mongo_all
    # from angler.protocols.JsonProtocol import JsonProtocol
    # from angler.services.databases.mongo import MongoDatabase
    # from angler.services.databases.mongo.table import MongoTable
    # from angler.sources.websocket import WebSocket

    # from sqlalchemy import *
    # from sqlalchemy.orm import *
    # engine = create_engine('mysql://root:123456@localhost/Bat', echo=True)
    # metadata = MetaData(engine)
    # users_table = Table('users', metadata,
    #     Column('id', Integer, primary_key=True),
    #     Column('name', String(40)),
    #     Column('email', String(120)))
    # class User(object): pass
    #
    # mapper(User, users_table)
    #
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # u = User()
    # u.name = 'new'
    # session.add(u)
    # session.flush()
    # session.commit()
    # users_table.drop()
    # users_table.create()
    # zk.delete('/zookeeper/goodboy')
    # def children_callback(children):
    #     print('****', children)
    #
    # children = zk.get_children('/zookeeper', children_callback)
    #
    # zk.create('/zookeeper/goodboy', ephemeral=True)
    # while True : sleep(1)
    # from kafka import KafkaProducer
    #
    # producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
    #                          max_block_ms=10000,
    #                          retries=2,
    #                          # compression_type="gzip",
    #                          # value_serializer=str.encode,
    #                          api_version="0.10"
    #                          )

    # for _ in range(100):
    # producer.send('test123', 'data')





    # Print the version of a node and its data
    # data, stat = zk.get("/my/favorite")
    # print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

    #
    # # List the children
    # children = zk.get_children("/my/favorite")
    # print("There are %s children with names %s" % (len(children), children))
    #
    # # Create a node with data
    # zk.create("/my/favorite/node", b"a value")


    # app = Angler('cloud_room')
    # app.services.mongo = MongoDatabase('mongo', 'localhost', 27017, 'cloudroom')
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'attend',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'calendar',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'clazz',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'course',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'paper',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'qrcode',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'result',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'role',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'sidebar',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'user',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "name",
    #         ]
    #     ),
    # )
    # app.services.mongo.add_table(
    #     MongoTable(
    #         'user',
    #         [
    #             ('_id', lambda: ObjectId())
    #         ],
    #         [
    #             "_id",
    #             "loginid",
    #             "openid",
    #             "sex",
    #             "name",
    #             "role",
    #             "avatar",
    #         ]
    #     ),
    # )
    #
    # def user_login(services, request: Request, response: Response):
    #     user = services.mongo['user'].find_one({
    #         'loginid': request.packet['data']['loginid'],
    #         'password': request.packet['data']['password'],
    #     })
    #     response.send(user, True)
    #
    #
    # con1 = Container('pc', WebSocket(JsonProtocol(), 8081))
    # con1.add_event(
    #     'user.login',
    #     ['user._login'],
    #     user_login
    # )
    #
    # event_mongo_all(con1, 'attend')
    # event_mongo_all(con1, 'calendar')
    # event_mongo_all(con1, 'clazz')
    # event_mongo_all(con1, 'course')
    # event_mongo_all(con1, 'paper')
    # event_mongo_all(con1, 'qrcode')
    # event_mongo_all(con1, 'result')
    # event_mongo_all(con1, 'role')
    # event_mongo_all(con1, 'sidebar')
    # event_mongo_all(con1, 'user')
    #
    # app.add_container(con1)
    #
    # con1 = Container('mobile', WebSocket(JsonProtocol(), 8082))
    # app.add_container(con1)
    #
    # # app.arrive(Request(None, JsonPacket({'event': 'user.login'})))
    # app.start()

    # app = make_app()
    # app.listen(8888)
    # tornado.ioloop.IOLoop.current().start()

    # app = create_angler_yml("""
    #     name: cloud_room
    #     cache:
    #         host: localhost
    #         port: 27017
    #         database: cache
    #     session:
    #         host: localhost
    #         port: 27017
    #         database: session
    #     mongo:
    #         host: localhost
    #         port: 27017
    #         database: cloudroom
    #         collections:
    #             - name: calendar
    #               init:
    #                 - _id: newid
    #               simple: [_id, name]
    #     """)
    #
    # mobile = create_container_yml("""
    # name: mobile
    # source:
    #     drive: web_socket
    #     port: 8081
    # protocol:
    #     drive: json_protocol
    # events:
    #
    # """)
    # # app.add_container(mobile)
    #
    # pc = create_container_yml("""
    # name: pc
    # source:
    #     drive: web_socket
    #     port: 8082
    # protocol:
    #     drive: json_protocol
    # events:
    #
    # """)