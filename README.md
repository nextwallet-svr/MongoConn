# MongoConn

need call `init_conn(DB_CONFIG)` before use  
`DB_CONFIG` is a python dict such as:  
```python
MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'DB_NAME',
    'username': None,
    'password': None,
}
``` 