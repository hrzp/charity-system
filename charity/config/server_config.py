def OBJ(): return lambda: None


redis = OBJ()
redis.password = "1234"

server = OBJ()
server.secret_key = "Set a Storng Key, Current key is not secure"
server.static_url_path = '/static'
server.static_folder = 'ui'
server.address = 'http://127.0.0.1:5000'

db = OBJ()
db.password = "xxx1234xxx"
