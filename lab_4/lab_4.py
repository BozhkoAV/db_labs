import psycopg2
from functools import lru_cache
import sys
from time import time, sleep
import random
from faker import Faker

conn = psycopg2.connect(
    dbname="sport_shops",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


# кэширующий прокси
@lru_cache(maxsize=128)
# количество кэшируемых запросов
def cache_query(query):
    if query.split(" ")[0] in ["INSERT", "UPDATE", "DELETE"]:
        cur.execute(query)
        cache_query.cache_clear()
    else:
        cur.execute(query)


# функция для выполнения запросов и измерения результатов
def execute_queries(is_cached, queries, n):
    max_time = 0
    min_time = sys.maxsize
    sum_time = 0

    for ind in range(n):
        start_time = time()
        query = queries[ind]

        if is_cached:
            cache_query(query)
        else:
            cur.execute(query)

        conn.commit()

        sleep(0.001)

        end_time = time()

        result_time = end_time - start_time
        if max_time < result_time:
            max_time = result_time
        if min_time > result_time:
            min_time = result_time
        sum_time += result_time

    print('\tКоличество выполненных запросов \n\t' + str(n))
    print('\tСреднее время выполнения запроса \n\t' + str(round((sum_time / n), 5)))
    print('\tСуммарное время выполнения запроса \n\t' + str(round(sum_time, 5)))
    print('\tМинимальное время выполнения запроса \n\t' + str(round(min_time, 5)))
    print('\tМаксимальное время выполнения запроса \n\t' + str(round(max_time, 5)))


number_of_queries = 1000

# Personal data
personal_data_select_queries = dict()
for i in range(number_of_queries):
    ids = set()
    while len(ids) < 100:
        ids.add(random.randint(1, 101))
    personal_data_select_queries[i] = \
        'SELECT * FROM personal_data WHERE id IN (' + str(ids).strip('{}') + ');'

print('SELECT для personal_data')
print('\nisCashed = True')
execute_queries(True, personal_data_select_queries, number_of_queries)
print()
print(cache_query.cache_info())
print('\nisCashed = False')
execute_queries(False, personal_data_select_queries, number_of_queries)
cache_query.cache_clear()
print()

number_of_queries = 3000

# Cart
cart_select_queries = dict()
for i in range(number_of_queries):
    ids = set()
    while len(ids) < 100:
        ids.add(random.randint(1, 101))
    cart_select_queries[i] = \
        'SELECT * FROM cart WHERE id IN (' + str(ids).strip('{}') + ');'

print('SELECT для cart')
print('\nisCashed = True')
execute_queries(True, cart_select_queries, number_of_queries)
print()
print(cache_query.cache_info())
print('\nisCashed = False')
execute_queries(False, cart_select_queries, number_of_queries)
cache_query.cache_clear()
print()

number_of_queries = 1000

# Store
store_select_queries = dict()
for i in range(number_of_queries):
    ids = set()
    while len(ids) < 29:
        ids.add(random.randint(1, 31))
    store_select_queries[i] = \
        'SELECT * FROM store WHERE id IN (' + str(ids).strip('{}') + ');'

print('SELECT для store')
print('\nisCashed = True')
execute_queries(True, store_select_queries, number_of_queries)
print()
print(cache_query.cache_info())
print('\nisCashed = False')
execute_queries(False, store_select_queries, number_of_queries)
cache_query.cache_clear()
print()

ratios = [(8, 1), (4, 1), (2, 1), (1, 1), (1, 2), (1, 4), (1, 8)]
for ratio in ratios:
    # Personal_data INSERT + SELECT
    number_of_insert_queries = 1024
    fake = Faker(locale="ru_RU")
    insert_select_queries = dict()
    for i in range(number_of_insert_queries):
        gender = fake.random.choice(["М", "Ж"])
        if gender == "М":
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
        date_of_birth = fake.date_of_birth()
        phone_number = fake.phone_number()

        insert_select_queries[i] = 'INSERT INTO personal_data ' \
                                   '(id, first_name, last_name, gender, date_of_birth, phone_number) ' \
                                   'VALUES (' + str(1000 + i) + ', \'' + first_name + '\', \'' + \
                                   last_name + '\', \'' + gender + '\', \'' + str(date_of_birth) + \
                                   '\', \'' + phone_number + '\');'

    number_of_select_queries = int(ratio[0] * number_of_insert_queries / ratio[1])
    for i in range(number_of_insert_queries, number_of_insert_queries + number_of_select_queries):
        insert_select_queries[i] = 'SELECT * FROM personal_data;'

    random_insert_select_queries = dict()

    i = 0
    while len(insert_select_queries) > 0:
        j = fake.random.choice(list(insert_select_queries.keys()))
        random_insert_select_queries[i] = insert_select_queries[j]
        del insert_select_queries[j]
        i += 1

    # Personal_data UPDATE + SELECT
    number_of_update_queries = 1024
    update_select_queries = dict()
    for i in range(number_of_update_queries):
        gender = fake.random.choice(["М", "Ж"])

        ids = set()
        while len(ids) < random.randint(1, 21):
            ids.add(random.randint(1000, 1000 + number_of_insert_queries - 1))
        update_select_queries[i] = 'UPDATE personal_data SET gender = \'' + gender + \
                                   '\' WHERE id IN (' + str(ids).strip('{}') + ');'

    number_of_select_queries = int(ratio[0] * number_of_update_queries / ratio[1])
    for i in range(number_of_update_queries, number_of_update_queries + number_of_select_queries):
        update_select_queries[i] = 'SELECT * FROM personal_data;'

    random_update_select_queries = dict()

    i = 0
    while len(update_select_queries) > 0:
        j = fake.random.choice(list(update_select_queries.keys()))
        random_update_select_queries[i] = update_select_queries[j]
        del update_select_queries[j]
        i += 1

    # Personal_data DELETE + SELECT
    number_of_delete_queries = number_of_insert_queries
    delete_select_queries = dict()
    ids = set()
    for i in range(1000, 1000 + number_of_insert_queries):
        ids.add(i)

    for i in range(number_of_delete_queries):
        delete_id = random.choice(list(ids))
        delete_select_queries[i] = 'DELETE FROM personal_data WHERE id = ' + str(delete_id) + ';'
        ids.remove(delete_id)

    number_of_select_queries = int(ratio[0] * number_of_delete_queries / ratio[1])
    for i in range(number_of_delete_queries, number_of_delete_queries + number_of_select_queries):
        delete_select_queries[i] = 'SELECT * FROM personal_data;'

    random_delete_select_queries = dict()

    i = 0
    while len(delete_select_queries) > 0:
        j = fake.random.choice(list(delete_select_queries.keys()))
        random_delete_select_queries[i] = delete_select_queries[j]
        del delete_select_queries[j]
        i += 1

    print('INSERT + SELECT для personal_data')
    print('ratio = ' + str(ratio[0]) + ' SELECT к ' + str(ratio[1]) + ' INSERT')
    print('\nisCashed = True')
    execute_queries(True, random_insert_select_queries, len(random_insert_select_queries))
    print()
    print(cache_query.cache_info())
    cache_query.cache_clear()
    print()

    print('UPDATE + SELECT для personal_data')
    print('ratio = ' + str(ratio[0]) + ' SELECT к ' + str(ratio[1]) + ' UPDATE')
    print('\nisCashed = True')
    execute_queries(True, random_update_select_queries, len(random_update_select_queries))
    print()
    print(cache_query.cache_info())
    cache_query.cache_clear()
    print()

    print('DELETE + SELECT для personal_data')
    print('ratio = ' + str(ratio[0]) + ' SELECT к ' + str(ratio[1]) + ' DELETE')
    print('\nisCashed = True')
    execute_queries(True, random_delete_select_queries, len(random_delete_select_queries))
    print()
    print(cache_query.cache_info())
    cache_query.cache_clear()
    print()

    print('INSERT + SELECT для personal_data')
    print('ratio = ' + str(ratio[0]) + ' SELECT к ' + str(ratio[1]) + ' INSERT')
    print('\nisCashed = False')
    execute_queries(False, random_insert_select_queries, len(random_insert_select_queries))
    print()

    print('UPDATE + SELECT для personal_data')
    print('ratio = ' + str(ratio[0]) + ' SELECT к ' + str(ratio[1]) + ' UPDATE')
    print('\nisCashed = False')
    execute_queries(False, random_update_select_queries, len(random_update_select_queries))
    print()

    print('DELETE + SELECT для personal_data')
    print('ratio = ' + str(ratio[0]) + ' SELECT к ' + str(ratio[1]) + ' DELETE')
    print('\nisCashed = False')
    execute_queries(False, random_delete_select_queries, len(random_delete_select_queries))
    print()

cur.close()
conn.close()
