# create random data for rate table
#
# mysql> describe rate;
# +-------+---------------+------+-----+---------+-------+
# | Field | Type          | Null | Key | Default | Extra |
# +-------+---------------+------+-----+---------+-------+
# | name  | char(100)     | NO   | PRI | NULL    |       |
# | price | decimal(10,2) | NO   |     | NULL    |       |
# +-------+---------------+------+-----+---------+-------+
# 2 rows in set (0.00 sec)
#

from random import randint, choice
from json import load
from uuid import uuid4
from faker import Faker

names = {'cucumber', 'apple', 'carrot', 'brinjal', 'lemon', 'milk', 'curd', 'ghee', 'butter', 'banana', 'soyabean', 'strawberry', 'blueberry', 'blackberry', 'rice', 'pistachio', 'cashew nuts', 'dry grapes', 'dates', 'pumpkin seeds', 'sunflower seeds', 'almonds'}
names = list(names)
rate_queries = list()

for name in names:
	query = f'insert into sales.rate (name, price) values ("{name}", {round(randint(10,100)/randint(2,8),2)}) ;'
	rate_queries.append(query)

# create random data for customers table

# mysql> desc customers;
# +-------+-----------+------+-----+---------+-------+
# | Field | Type      | Null | Key | Default | Extra |
# +-------+-----------+------+-----+---------+-------+
# | id    | char(36)  | NO   | PRI | NULL    |       |
# | name  | char(100) | NO   |     | NULL    |       |
# | phone | char(10)  | YES  |     | NULL    |       |
# | email | char(100) | YES  |     | NULL    |       |
# +-------+-----------+------+-----+---------+-------+
# 4 rows in set (0.00 sec)
#

with open('./../config/parameters.json') as file:
	parameters = load(file)

fake = Faker()
customers = [str(uuid4()) for i in range(parameters['customers'])]
customer_queries = list()

for customer in customers:
	query = f'''insert into sales.customers (id, name, phone, email) values ("{customer}", "{fake.name()}", "{str(fake.phone_number()).replace('x', '')}", "{str(fake.email()).replace('example', 'gmail')}") ;'''
	customer_queries.append(query)

# create random data for transactions table

# mysql> describe transactions;
# +---------------+---------------+------+-----+---------+-------+
# | Field         | Type          | Null | Key | Default | Extra |
# +---------------+---------------+------+-----+---------+-------+
# | saledate      | date          | YES  |     | NULL    |       |
# | transactionid | char(36)      | NO   | PRI | NULL    |       |
# | customer_id   | char(36)      | YES  | MUL | NULL    |       |
# | item          | char(100)     | YES  |     | NULL    |       |
# | rate          | decimal(10,2) | YES  |     | NULL    |       |
# | quantity      | decimal(10,2) | YES  |     | NULL    |       |
# | total         | decimal(10,2) | YES  |     | NULL    |       |
# +---------------+---------------+------+-----+---------+-------+
# 7 rows in set (0.00 sec)
#


transactions_queries = list()

for i in range(parameters['transactions']):
	transactionid = str(uuid4())
	saledate = fake.date_between(start_date=parameters['data start'], end_date=parameters['data end'])
	customer_id = choice(customers)
	item = choice(names)
	quantity = round(randint(1,15)/randint(2,8),2)
	query = f'insert into sales.transactions (saledate, transactionid, customer_id, item, quantity) values ("{saledate}", "{transactionid}", "{customer_id}", "{item}", {quantity}) ;'
	transactions_queries.append(query)


# combine all data to a script

start = 'use sales ;'
combined = rate_queries + ['\n'] + customer_queries + ['\n'] + transactions_queries

update = 'update sales.transactions t join sales.rate r on t.item=r.name set t.rate=r.price where t.item=r.name ;\n'
update += 'update sales.transactions set total = rate*quantity;\n'

with open('sales data.sql', 'w') as script:
	script.write(start+'\n\n')
	
	for query in combined:
		script.write(query+'\n')

	script.write('\n\n')
	script.write(update+'\n')

