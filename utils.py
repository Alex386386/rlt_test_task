import os

mongo_host = os.getenv('MONGO_HOST', 'mongo')
mongo_port = int(os.getenv('MONGO_PORT', 27017))

invalid_value = ('Невалидный запрос. Пример запроса:'
                 ' {"dt_from": "2022-09-01T00:00:00",'
                 ' "dt_upto": "2022-12-31T23:59:00",'
                 ' "group_type": "month"}')
