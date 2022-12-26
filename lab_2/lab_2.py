import psycopg2
from faker import Faker
import random
import numpy as np

conn = psycopg2.connect(
    dbname="sport_shops",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

fake = Faker(locale="ru_RU")

# Vendor
names = set()
while len(names) < 5:
    names.add(fake.company())

for id in range(4, 4 + len(names)):
    name = names.pop()
    contract_start_date = fake.past_date(start_date="-3y")
    contract_end_date = fake.future_date(end_date="+3y")

    cur.execute("INSERT INTO vendor "
                "(id, name, contract_start_date, contract_end_date) "
                "VALUES (%s, %s, %s, %s);",
                (id, name, contract_start_date, contract_end_date))

conn.commit()

# Product
for id in range(8, 101):
    product_name = fake.pystr(min_chars=8, max_chars=30)
    purchase_price = round(random.uniform(0.01, 99999.00), 2)
    retail_price = round(random.uniform(purchase_price + 0.01, 99999.99), 2)
    vendor_id = random.randint(1, 8)

    cur.execute("INSERT INTO product "
                "(id, product_name, purchase_price, retail_price, vendor_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, product_name, purchase_price, retail_price, vendor_id))

conn.commit()

# Personal data
for id in range(5, 101):
    gender = fake.random.choice(["М", "Ж"])
    if gender == "М":
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
    date_of_birth = fake.date_of_birth()
    phone_number = fake.phone_number()

    cur.execute("INSERT INTO personal_data "
                "(id, first_name, last_name, gender, date_of_birth, phone_number) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (id, first_name, last_name, gender, date_of_birth, phone_number))

conn.commit()

# Customer
cur.execute("SELECT personal_data_id FROM customer;")
conn.commit()

pd_ids = set()
for pd_id in cur.fetchall():
    pd_ids.add(pd_id[0])

for id in range(4, 21):
    discount_card = bool(random.getrandbits(1))

    personal_data_id = random.randint(1, 100)
    while personal_data_id in pd_ids:
        personal_data_id = random.randint(1, 100)
    pd_ids.add(personal_data_id)

    cur.execute("INSERT INTO customer "
                "(id, discount_card, personal_data_id) "
                "VALUES (%s, %s, %s);",
                (id, discount_card, personal_data_id))

conn.commit()

# Cart
for id in range(5, 101):
    order_date = fake.past_date(start_date="-3y")
    rating = random.randint(1, 5)
    feedback = fake.text(max_nb_chars=250).replace("\n", " ")
    customer_id = random.randint(1, 20)

    cur.execute("INSERT INTO cart "
                "(id, order_date, rating, feedback, customer_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, order_date, rating, feedback, customer_id))

conn.commit()

# Products in carts
products_in_carts = np.zeros(10000, dtype=int).reshape(100, 100)

cur.execute("SELECT * FROM products_in_carts;")
conn.commit()

for product_cart in cur.fetchall():
    products_in_carts[product_cart[0] - 1][product_cart[1] - 1] = product_cart[2]

for id in range(9, 101):
    product_id = random.randint(1, 100)
    cart_id = random.randint(1, 100)
    quantity = random.randint(1, 100)

    while products_in_carts[product_id - 1][cart_id - 1] != 0:
        product_id = random.randint(1, 100)
        cart_id = random.randint(1, 100)

    products_in_carts[product_id - 1][cart_id - 1] = quantity

    cur.execute("INSERT INTO products_in_carts "
                "(product_id, cart_id, quantity) "
                "VALUES (%s, %s, %s);",
                (product_id, cart_id, quantity))

conn.commit()

# Store
for id in range(3, 16):
    city = fake.random.choice(["Санкт-Петербург", "Москва", "Сочи", "Казань", "Барнаул"])
    address = fake.street_address()
    rental_price = round(random.uniform(10000.00, 999999.99), 2)
    rental_start_date = fake.past_date(start_date="-3y")
    rental_end_date = fake.future_date(end_date="+3y")

    cur.execute("INSERT INTO store "
                "(id, city, address, rental_price, rental_start_date, rental_end_date) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (id, city, address, rental_price, rental_start_date, rental_end_date))

conn.commit()

# Products in stores
products_in_stores = np.zeros(1500, dtype=int).reshape(100, 15)

cur.execute("SELECT * FROM products_in_stores;")
conn.commit()

for product_store in cur.fetchall():
    products_in_stores[product_store[0] - 1][product_store[1] - 1] = product_store[2]

for id in range(8, 101):
    product_id = random.randint(1, 100)
    store_id = random.randint(1, 15)
    quantity = random.randint(1, 100)

    while products_in_stores[product_id - 1][store_id - 1] != 0:
        product_id = random.randint(1, 100)
        store_id = random.randint(1, 15)

    products_in_stores[product_id - 1][store_id - 1] = quantity

    cur.execute("INSERT INTO products_in_stores "
                "(product_id, store_id, quantity) "
                "VALUES (%s, %s, %s);",
                (product_id, store_id, quantity))

conn.commit()

# Seller
cur.execute("SELECT personal_data_id FROM seller;")
conn.commit()

pd_ids = set()
for pd_id in cur.fetchall():
    pd_ids.add(pd_id[0])

for id in range(3, 31):
    salary = round(random.uniform(10000.00, 99999.99), 2)
    working_email_address = fake.pystr(min_chars=8, max_chars=30) + fake.random.choice(["@mail.ru", "@gmail.com"])

    personal_data_id = random.randint(1, 100)
    while personal_data_id in pd_ids:
        personal_data_id = random.randint(1, 100)
    pd_ids.add(personal_data_id)

    store_id = random.randint(1, 15)

    cur.execute("INSERT INTO seller "
                "(id, salary, working_email_address, personal_data_id, store_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, salary, working_email_address, personal_data_id, store_id))

conn.commit()

# Warehouse
for id in range(3, 16):
    city = fake.random.choice(["Санкт-Петербург", "Москва", "Сочи", "Казань", "Барнаул"])
    address = fake.street_address()
    warehouse_area = divmod(random.randint(300, 10000), 100)[0] * 100
    rental_price = round(random.uniform(10000.00, 999999.99), 2)
    rental_start_date = fake.past_date(start_date="-3y")
    rental_end_date = fake.future_date(end_date="+3y")

    cur.execute("INSERT INTO warehouse "
                "(id, city, address, warehouse_area, rental_price, rental_start_date, rental_end_date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                (id, city, address, warehouse_area, rental_price, rental_start_date, rental_end_date))

conn.commit()

# Products in warehouses
products_in_warehouses = np.zeros(1500, dtype=int).reshape(100, 15)

cur.execute("SELECT * FROM products_in_warehouses;")
conn.commit()

for product_warehouse in cur.fetchall():
    products_in_warehouses[product_warehouse[0] - 1][product_warehouse[1] - 1] = product_warehouse[2]

for id in range(9, 101):
    product_id = random.randint(1, 100)
    warehouse_id = random.randint(1, 15)
    quantity = random.randint(1, 100)

    while products_in_warehouses[product_id - 1][warehouse_id - 1] != 0:
        product_id = random.randint(1, 100)
        warehouse_id = random.randint(1, 15)

    products_in_warehouses[product_id - 1][warehouse_id - 1] = quantity

    cur.execute("INSERT INTO products_in_warehouses "
                "(product_id, warehouse_id, quantity) "
                "VALUES (%s, %s, %s);",
                (product_id, warehouse_id, quantity))

conn.commit()

# Worker
cur.execute("SELECT personal_data_id FROM worker;")
conn.commit()

pd_ids = set()
for pd_id in cur.fetchall():
    pd_ids.add(pd_id[0])

for id in range(3, 31):
    salary = round(random.uniform(10000.00, 99999.99), 2)
    working_email_address = fake.pystr(min_chars=8, max_chars=30) + fake.random.choice(["@mail.ru", "@gmail.com"])

    personal_data_id = random.randint(1, 100)
    while personal_data_id in pd_ids:
        personal_data_id = random.randint(1, 100)
    pd_ids.add(personal_data_id)

    warehouse_id = random.randint(1, 15)

    cur.execute("INSERT INTO worker "
                "(id, salary, working_email_address, personal_data_id, warehouse_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, salary, working_email_address, personal_data_id, warehouse_id))

conn.commit()

cur.close()
conn.close()

# перед запуском generator.py необходимо создать БД sport_shops в pgAdmin 4
import psycopg2
from faker import Faker
import random
import numpy as np

conn = psycopg2.connect(
    dbname="sport_shops",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Создание таблиц

cur.execute("CREATE TABLE vendor ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "name VARCHAR(100) NOT NULL,"
            "contract_start_date DATE NOT NULL,"
            "contract_end_date DATE NOT NULL,"
            "CONSTRAINT dates_check CHECK (contract_start_date < contract_end_date)"
            ");"
            ""
            "CREATE TABLE product ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "product_name VARCHAR(200) NOT NULL,"
            "purchase_price NUMERIC(7, 2) NOT NULL,"
            "retail_price NUMERIC(7, 2) NOT NULL,"
            "vendor_id INTEGER REFERENCES vendor(id)"
            ");"
            ""
            "CREATE TABLE personal_data ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "first_name VARCHAR(20) NOT NULL,"
            "last_name VARCHAR(20) NOT NULL,"
            "gender VARCHAR(1) NOT NULL,"
            "date_of_birth DATE NOT NULL,"
            "phone_number VARCHAR(20) NOT NULL,"
            "CONSTRAINT gender_check CHECK (gender = 'М' OR gender = 'Ж')"
            ");"
            ""
            "CREATE TABLE customer ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "discount_card BOOLEAN NOT NULL,"
            "personal_data_id INTEGER REFERENCES personal_data(id)"
            ");"
            ""
            "CREATE TABLE cart ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "order_date DATE NOT NULL,"
            "rating INTEGER NOT NULL,"
            "feedback VARCHAR(500) NOT NULL,"
            "customer_id INTEGER REFERENCES customer(id),"
            "CONSTRAINT rating_check CHECK (rating >= 1 AND rating <= 5)"
            ");"
            ""
            "CREATE TABLE products_in_carts ("
            "product_id INTEGER REFERENCES product(id),"
            "cart_id INTEGER REFERENCES cart(id),"
            "quantity INTEGER NOT NULL"
            ");"
            ""
            "CREATE TABLE store ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "city VARCHAR(100) NOT NULL,"
            "address VARCHAR(200) NOT NULL,"
            "rental_price NUMERIC(8, 2) NOT NULL,"
            "rental_start_date DATE NOT NULL,"
            "rental_end_date DATE NOT NULL,"
            "CONSTRAINT dates_check CHECK (rental_start_date < rental_end_date)"
            ");"
            ""
            "CREATE TABLE products_in_stores ("
            "product_id INTEGER REFERENCES product(id),"
            "store_id INTEGER REFERENCES store(id),"
            "quantity INTEGER NOT NULL"
            ");"
            ""
            "CREATE TABLE seller ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "salary NUMERIC(7, 2) NOT NULL,"
            "working_email_address VARCHAR(100) NOT NULL,"
            "personal_data_id INTEGER REFERENCES personal_data(id),"
            "store_id INTEGER REFERENCES store(id)"
            ");"
            ""
            "CREATE TABLE warehouse ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "city VARCHAR(100) NOT NULL,"
            "address VARCHAR(200) NOT NULL,"
            "warehouse_area INTEGER NOT NULL,"
            "rental_price NUMERIC(8, 2) NOT NULL,"
            "rental_start_date DATE NOT NULL,"
            "rental_end_date DATE NOT NULL,"
            "CONSTRAINT dates_check CHECK (rental_start_date < rental_end_date)"
            ");"
            ""
            "CREATE TABLE products_in_warehouses ("
            "product_id INTEGER REFERENCES product(id),"
            "warehouse_id INTEGER REFERENCES warehouse(id),"
            "quantity INTEGER NOT NULL"
            ");"
            ""
            "CREATE TABLE worker ("
            "id INTEGER NOT NULL PRIMARY KEY,"
            "salary NUMERIC(7, 2) NOT NULL,"
            "working_email_address VARCHAR(100) NOT NULL,"
            "personal_data_id INTEGER REFERENCES personal_data(id),"
            "warehouse_id INTEGER REFERENCES warehouse(id)"
            ");")

conn.commit()

# Заполнение таблиц

fake = Faker(locale="ru_RU")

number_of_vendors = 10
number_of_products = 100

number_of_personal_datas = 300
number_of_customers = 200

number_of_carts = 300
number_of_products_in_carts = 1000

number_of_stores = 20
number_of_products_in_stores = 1000
number_of_sellers = 80

number_of_warehouses = 30
number_of_products_in_warehouses = 1500
number_of_workers = 90

# Vendor
names = set()
while len(names) < number_of_vendors:
    names.add(fake.company())

for id in range(1, number_of_vendors + 1):
    name = names.pop()
    contract_start_date = fake.past_date(start_date="-3y")
    contract_end_date = fake.future_date(end_date="+3y")

    cur.execute("INSERT INTO vendor "
                "(id, name, contract_start_date, contract_end_date) "
                "VALUES (%s, %s, %s, %s);",
                (id, name, contract_start_date, contract_end_date))

conn.commit()

# Product
for id in range(1, number_of_products + 1):
    product_name = fake.pystr(min_chars=8, max_chars=30)
    purchase_price = round(random.uniform(0.01, 99999.00), 2)
    retail_price = round(random.uniform(purchase_price + 0.01, 99999.99), 2)
    vendor_id = random.randint(1, number_of_vendors)

    cur.execute("INSERT INTO product "
                "(id, product_name, purchase_price, retail_price, vendor_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, product_name, purchase_price, retail_price, vendor_id))

conn.commit()

# Personal data
for id in range(1, number_of_personal_datas + 1):
    gender = fake.random.choice(["М", "Ж"])
    if gender == "М":
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
    date_of_birth = fake.date_of_birth()
    phone_number = fake.phone_number()

    cur.execute("INSERT INTO personal_data "
                "(id, first_name, last_name, gender, date_of_birth, phone_number) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (id, first_name, last_name, gender, date_of_birth, phone_number))

conn.commit()

# Customer
pd_ids = set()

for id in range(1, number_of_customers + 1):
    discount_card = bool(random.getrandbits(1))

    personal_data_id = random.randint(1, number_of_personal_datas)
    while personal_data_id in pd_ids:
        personal_data_id = random.randint(1, number_of_personal_datas)
    pd_ids.add(personal_data_id)

    cur.execute("INSERT INTO customer "
                "(id, discount_card, personal_data_id) "
                "VALUES (%s, %s, %s);",
                (id, discount_card, personal_data_id))

conn.commit()

# Cart
for id in range(1, number_of_carts + 1):
    order_date = fake.past_date(start_date="-3y")
    rating = random.randint(1, 5)
    feedback = fake.text(max_nb_chars=250).replace("\n", " ")
    customer_id = random.randint(1, number_of_customers)

    cur.execute("INSERT INTO cart "
                "(id, order_date, rating, feedback, customer_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, order_date, rating, feedback, customer_id))

conn.commit()

# Products in carts
products_in_carts = np.zeros(number_of_products * number_of_carts, dtype=int)\
    .reshape(number_of_products, number_of_carts)

for id in range(1, number_of_products_in_carts + 1):
    product_id = random.randint(1, number_of_products)
    cart_id = random.randint(1, number_of_carts)
    quantity = random.randint(1, 100)

    while products_in_carts[product_id - 1][cart_id - 1] != 0:
        product_id = random.randint(1, number_of_products)
        cart_id = random.randint(1, number_of_carts)

    products_in_carts[product_id - 1][cart_id - 1] = quantity

    cur.execute("INSERT INTO products_in_carts "
                "(product_id, cart_id, quantity) "
                "VALUES (%s, %s, %s);",
                (product_id, cart_id, quantity))

conn.commit()

# Store
for id in range(1, number_of_stores + 1):
    city = fake.random.choice(["Санкт-Петербург", "Москва", "Сочи", "Казань", "Барнаул"])
    address = fake.street_address()
    rental_price = round(random.uniform(10000.00, 999999.99), 2)
    rental_start_date = fake.past_date(start_date="-3y")
    rental_end_date = fake.future_date(end_date="+3y")

    cur.execute("INSERT INTO store "
                "(id, city, address, rental_price, rental_start_date, rental_end_date) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (id, city, address, rental_price, rental_start_date, rental_end_date))

conn.commit()

# Products in stores
products_in_stores = np.zeros(number_of_products * number_of_stores, dtype=int)\
    .reshape(number_of_products, number_of_stores)

for id in range(1, number_of_products_in_stores + 1):
    product_id = random.randint(1, number_of_products)
    store_id = random.randint(1, number_of_stores)
    quantity = random.randint(1, 100)

    while products_in_stores[product_id - 1][store_id - 1] != 0:
        product_id = random.randint(1, number_of_products)
        store_id = random.randint(1, number_of_stores)

    products_in_stores[product_id - 1][store_id - 1] = quantity

    cur.execute("INSERT INTO products_in_stores "
                "(product_id, store_id, quantity) "
                "VALUES (%s, %s, %s);",
                (product_id, store_id, quantity))

conn.commit()

# Seller
pd_ids = set()

for id in range(1, number_of_sellers + 1):
    salary = round(random.uniform(10000.00, 99999.99), 2)
    working_email_address = fake.pystr(min_chars=8, max_chars=30) + fake.random.choice(["@mail.ru", "@gmail.com"])

    personal_data_id = random.randint(1, number_of_personal_datas)
    while personal_data_id in pd_ids:
        personal_data_id = random.randint(1, number_of_personal_datas)
    pd_ids.add(personal_data_id)

    store_id = random.randint(1, number_of_stores)

    cur.execute("INSERT INTO seller "
                "(id, salary, working_email_address, personal_data_id, store_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, salary, working_email_address, personal_data_id, store_id))

conn.commit()

# Warehouse
for id in range(1, number_of_warehouses + 1):
    city = fake.random.choice(["Санкт-Петербург", "Москва", "Сочи", "Казань", "Барнаул"])
    address = fake.street_address()
    warehouse_area = divmod(random.randint(300, 10000), 100)[0] * 100
    rental_price = round(random.uniform(10000.00, 999999.99), 2)
    rental_start_date = fake.past_date(start_date="-3y")
    rental_end_date = fake.future_date(end_date="+3y")

    cur.execute("INSERT INTO warehouse "
                "(id, city, address, warehouse_area, rental_price, rental_start_date, rental_end_date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                (id, city, address, warehouse_area, rental_price, rental_start_date, rental_end_date))

conn.commit()

# Products in warehouses
products_in_warehouses = np.zeros(number_of_products * number_of_warehouses, dtype=int)\
    .reshape(number_of_products, number_of_warehouses)

for id in range(1, number_of_products_in_warehouses + 1):
    product_id = random.randint(1, number_of_products)
    warehouse_id = random.randint(1, number_of_warehouses)
    quantity = random.randint(1, 100)

    while products_in_warehouses[product_id - 1][warehouse_id - 1] != 0:
        product_id = random.randint(1, number_of_products)
        warehouse_id = random.randint(1, number_of_warehouses)

    products_in_warehouses[product_id - 1][warehouse_id - 1] = quantity

    cur.execute("INSERT INTO products_in_warehouses "
                "(product_id, warehouse_id, quantity) "
                "VALUES (%s, %s, %s);",
                (product_id, warehouse_id, quantity))

conn.commit()

# Worker
pd_ids = set()

for id in range(1, number_of_workers + 1):
    salary = round(random.uniform(10000.00, 99999.99), 2)
    working_email_address = fake.pystr(min_chars=8, max_chars=30) + fake.random.choice(["@mail.ru", "@gmail.com"])

    personal_data_id = random.randint(1, number_of_personal_datas)
    while personal_data_id in pd_ids:
        personal_data_id = random.randint(1, number_of_personal_datas)
    pd_ids.add(personal_data_id)

    warehouse_id = random.randint(1, number_of_warehouses)

    cur.execute("INSERT INTO worker "
                "(id, salary, working_email_address, personal_data_id, warehouse_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                (id, salary, working_email_address, personal_data_id, warehouse_id))

conn.commit()

cur.close()
conn.close()
