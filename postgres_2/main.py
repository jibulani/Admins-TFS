import model


def add_good_in_order(order, good, quantity):
    order_item = model.OrderItem()
    order_item.order_id = order
    order_item.good_id = good
    order_item.quantity = quantity
    order_item.save()


def delete_good_from_order(order, good):
    model.OrderItem.delete()\
        .where(model.OrderItem.order_id == order and model.OrderItem.good_id == good)\
        .execute()


def change_good_quantity_in_order(order, good, quantity):
    order_item = model.OrderItem.select()\
        .where(model.OrderItem.order_id == order and model.OrderItem.good_id == good)\
        .get()
    order_item.quantity = quantity
    order_item.save()


def get_db_info():
    with open('data.csv', 'w') as f:
        f.write('first_nm,last_nm,good_name,vendor,status,quantity\n')
        for order_item in model.OrderItem.select():
            customer = order_item.order_id.cust_id
            good = order_item.good_id
            f.write(customer.first_nm + ',' + customer.last_nm + ','
                    + good.name + ',' + good.vendor + ','
                    + order_item.order_id.status + ',' + str(order_item.quantity) + '\n')


model.create_tables()

customer_1 = model.Customer()
customer_1.first_nm = 'John'
customer_1.last_nm = 'Connor'
customer_1.save()

customer_2 = model.Customer()
customer_2.first_nm = 'Jack'
customer_2.last_nm = 'Rassel'
customer_2.save()

order_1 = model.Order()
order_1.cust_id = customer_1
order_1.status = 'Ready'
order_1.save()

order_2 = model.Order()
order_2.cust_id = customer_2
order_2.status = 'Wait'
order_2.save()

good_1 = model.Good()
good_1.vendor = 'samsung'
good_1.name = 'galaxy s2'
good_1.description = 'smartphone'
good_1.save()

good_2 = model.Good()
good_2.vendor = 'apple'
good_2.name = 'iphone 3'
good_2.description = 'smartphone'
good_2.save()

order_item_1 = model.OrderItem()
order_item_1.order_id = order_1
order_item_1.good_id = good_2
order_item_1.quantity = 3
order_item_1.save()

order_item_2 = model.OrderItem()
order_item_2.order_id = order_2
order_item_2.good_id = good_1
order_item_2.quantity = 2
order_item_2.save()

add_good_in_order(order_1, good_1, 1)
delete_good_from_order(order_1, good_2)
change_good_quantity_in_order(order_2, good_1, 5)
get_db_info()
