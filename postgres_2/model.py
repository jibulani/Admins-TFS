from peewee import *
import settings
import datetime

db = PostgresqlDatabase(settings.database, user=settings.user, password=settings.password,
                        host=settings.host, port=settings.port)


class Customer(Model):
    cust_id = AutoField(primary_key=True)
    first_nm = CharField(max_length=100)
    last_nm = CharField(max_length=100)

    class Meta:
        database = db
        db_table = 'customers'


class Order(Model):
    order_id = AutoField(primary_key=True)
    cust_id = ForeignKeyField(model=Customer)
    order_dttm = DateTimeField(default=datetime.datetime.now)
    status = CharField(max_length=20)

    class Meta:
        database = db
        db_table = 'orders'


class Good(Model):
    good_id = AutoField(primary_key=True)
    vendor = CharField(max_length=100)
    name = CharField(max_length=100)
    description = CharField(max_length=300)

    class Meta:
        database = db
        db_table = 'goods'


class OrderItem(Model):
    order_item_id = AutoField(primary_key=True)
    order_id = ForeignKeyField(model=Order)
    good_id = ForeignKeyField(model=Good)
    quantity = IntegerField()

    class Meta:
        database = db
        db_table = 'order_items'


def create_tables():
    with db:
        db.create_tables([Customer, Order, Good, OrderItem])