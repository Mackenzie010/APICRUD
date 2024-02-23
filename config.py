
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'felipemack'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Gavioesdafiel04'
app.config['MYSQL_DATABASE_DB'] = 'acapi10'
app.config['MYSQL_DATABASE_HOST'] = 'db4free.net'
mysql.init_app(app)