import psycopg2
import settings

create_table_commands = ["""CREATE TABLE customers (
                            cust_id SERIAL PRIMARY KEY,
                            first_nm VARCHAR(100) NOT NULL,
                            last_nm VARCHAR(100) NOT NULL)
                         """,
                         """CREATE TABLE orders (
                            order_id SERIAL PRIMARY KEY,
                            cust_id SERIAL NOT NULL,
                            order_dttm TIMESTAMP DEFAULT Now(),
                            status VARCHAR(20) NOT NULL,
                            FOREIGN KEY (cust_id)
                            REFERENCES customers(cust_id)
                            ON UPDATE CASCADE ON DELETE CASCADE)
                         """,
                         """CREATE TABLE goods (
                            good_id SERIAL PRIMARY KEY,
                            vendor VARCHAR(100) NOT NULL,
                            name VARCHAR(100) NOT NULL,
                            description VARCHAR(300))
                         """,
                         """CREATE TABLE order_items (
                            order_item_id SERIAL PRIMARY KEY,
                            order_id SERIAL NOT NULL,
                            good_id SERIAL NOT NULL,
                            quantity INTEGER NOT NULL,
                            FOREIGN KEY (order_id)
                              REFERENCES orders (order_id)
                              ON UPDATE CASCADE ON DELETE CASCADE,
                            FOREIGN KEY (good_id)
                              REFERENCES goods (good_id)
                              ON UPDATE CASCADE ON DELETE CASCADE)
                         """]

insert_customers_commands = ["""INSERT INTO customers(first_nm, last_nm)
                                VALUES ('John', 'Connor')
                             """,
                             """INSERT INTO customers(first_nm, last_nm)
                                VALUES ('Jack', 'Rassel')
                             """]

insert_orders_commands = ["""INSERT INTO orders(cust_id, status)
                             VALUES (1, 'Ready')
                          """,
                          """INSERT INTO orders(cust_id, status)
                             VALUES (2, 'Wait')
                          """]

insert_goods_commands = ["""INSERT INTO goods(vendor, name, description)
                             VALUES ('samsung', 'galaxy s2', 'smartphone')
                         """,
                         """INSERT INTO goods(vendor, name, description)
                            VALUES ('apple', 'iphone 3', 'smartphone')
                         """]

insert_order_items_commands = ["""INSERT INTO order_items(order_id, good_id, quantity)
                                  VALUES (1, 2, 3)
                               """,
                               """INSERT INTO order_items(order_id, good_id, quantity)
                                  VALUES (2, 1, 2)
                               """,
                               ]

get_db_info_command = """SELECT customers.first_nm, customers.last_nm, goods.name, goods.vendor, orders.status, quantity
                         FROM public.order_items INNER JOIN public.orders ON order_items.order_id = orders.order_id
                         INNER JOIN public.customers ON orders.cust_id = customers.cust_id
                         INNER JOIN public.goods ON order_items.good_id = goods.good_id;
                      """


def add_good_in_order(order_id, good_id, quantity):
    command = """INSERT INTO order_items(order_id, good_id, quantity)
                 VALUES (%s, %s, %s)
              """
    try:
        cur = conn.cursor()
        cur.execute(command, (order_id, good_id, quantity))
        cur.close()
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def delete_good_from_order(order_id, good_id):
    command = """DELETE FROM order_items
                 WHERE order_id = %s AND good_id = %s
              """
    try:
        cur = conn.cursor()
        cur.execute(command, (order_id, good_id))
        cur.close()
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def change_good_quantity_in_order(order_id, good_id, quantity):
    command = """UPDATE order_items SET quantity = %s
                 WHERE order_id = %s AND good_id = %s
              """
    try:
        cur = conn.cursor()
        cur.execute(command, (quantity, order_id, good_id))
        cur.close()
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_db_info():
    try:
        with open("data.csv", "w") as f:
            cur = conn.cursor()
            cur.execute(get_db_info_command)
            f.write("first_nm,last_nm,good_name,vendor,status,quantity\n")
            for row in cur:
                f.write(','.join(map(str, row)) + '\n')
            cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


conn = psycopg2.connect(host=settings.host, database=settings.database, user=settings.user,
                        password=settings.password, port=settings.port)
try:
    cur = conn.cursor()
    for command in create_table_commands:
        cur.execute(command)
    for command in insert_customers_commands:
        cur.execute(command)
    for command in insert_orders_commands:
        cur.execute(command)
    for command in insert_goods_commands:
        cur.execute(command)
    for command in insert_order_items_commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    add_good_in_order(1, 1, 1)
    delete_good_from_order(1, 2)
    change_good_quantity_in_order(2, 1, 5)
    get_db_info()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
