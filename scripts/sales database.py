import re
from os import system as cmd
from myconnection import connect_to_mysql

config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": input('enter password: ')
}

cnx = connect_to_mysql(config, attempts=3)

if cnx and cnx.is_connected():  

  with open('sales schema.sql') as script:
    schemas = script.read().split(';')

  for i in schemas:
    if re.match(r'^[\s\n\t ]*$',i):
      schemas.remove(i)

  schemas = list(map(lambda x: x+';', schemas))

  cmd('python "sales data.py"')
  
  with open('sales data.sql') as script:
    data = script.read().split(';')

  for i in data:
    if re.match(r'^[\s\n\t ]*$',i):
      data.remove(i)

  data = list(map(lambda x: x+';', data))

  with open('sales functions.sql') as script:
    functions = script.read().split('\n')

  while '' in functions:
    functions.remove('')

  with open('sales sp.sql') as script:
    sp = script.read().split('\n')

  while '' in sp:
    sp.remove('')

  with open('sales views.sql') as script:
    views = script.read().split('\n')

  while '' in views:
    views.remove('')

  with cnx.cursor() as cursor:
    print('########## Schemas ##########\n\n')
    for query in schemas:
      print(query)
      cursor.execute(query)

    print('########## Stored Procedures ##########\n\n')
    for query in sp:
      print(query)
      cursor.execute(query)

    print('########## Views ##########\n\n')
    for query in views:
      print(query)
      cursor.execute(query)

    print('########## Functions ##########\n\n')
    for query in functions:
      print(query)
      cursor.execute(query)

    print('########## Data ##########\n\n')
    for query in data:
      print(query)
      cursor.execute(query)

  cnx.commit()
  cnx.close()

else:
  print("Could not connect")


# dump the database
print('\n\n\ndumping the database...')
cmd('python "db dumper.py"')