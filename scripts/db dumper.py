from os import system as cmd
from time import time
from  datetime import datetime

user = 'root'
db = 'sales'

print(f'\nuser: {user}')

# windows
# command = f'''mysqldump --add-drop-database -B --comments --column-statistics --create-options --dump-date --flush-privileges --network-timeout -R --order-by-primary --triggers -u {user} -p "{db}" > "{path}"'''
    
timestamp = str(datetime.now())
path = f'./../dumps/{db} dump file {timestamp}.sql'
command = f'''mysqldump --add-drop-database -B --comments --create-options --dump-date --flush-privileges -R --order-by-primary --triggers -u {user} -p "{db}" > "{path}"'''

start = time()
cmd(command)
end = time()

print("dumping finsihed in: %.2fs"%(end-start))
print(f'dump file saved at: {path}')

# to 'undump'
# mysql -p -u root -h 127.0.0.1 "db" < "dump".sql
