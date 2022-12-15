import pymysql
#import pymysql.cursors

class ConnectionMysql:
	"""
	docstring for Connection_Mysql
	
	"""
	def __init__(self, database_host, user, password):
		"""
		Constructor de la clase donde contiene 2 atributos
		* db: atributo que crea la conexion a la base de datos
		* cursor: atributo donde ejecuta todas las querys

		Para el constructor se necesita pasar 3 parametros
		* database_host: es el host o donde esta alojado la base de datos
		* user: es el usuario que tiene acceso a la base de datos
		* password: es la contraseña que tiene la base de datos

		"""

		try:
			self._db = pymysql.connect(
										host=database_host, 
										user=user, 
										password=password)

			self._cursor = self._db.cursor()

		except pymysql.err.InternalError as e:
			code, msg = e.args
			
			return msg

	# Recibe el nombre de la base de datos a crear 
	def create_db(self, name):
		"""
		*Metodo que crea una base de datos*

		- `@param name: es el nombre de la base de datos que se quiere crear`

		`Ejemplo: con.create_db('test_2')`
		"""
		try:
			self._cursor.execute('CREATE database IF NOT EXISTS {0}'.format(name))
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	# Recibe el nombre de la base de datos a eliminar
	def drop_db(self, name):
		"""
		*Metodo que elimina una base de datos*

		- `@param name: es el nombre de la base de datos que se desea eliminar`
	
		`Ejemplo: con.drop_db('test_2')`
		"""
		try:
			self._cursor.execute('DROP database {0}'.format(name))
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	# Recibe el nombre de la base de datos a usar
	def use_data_base(self, name):
		"""
		*Metodo para seleccionar la base de datos a usera*
		- `@param name: nombre de la base de datos a usar`

		`Ejemplo: con.use_data_base('Test')`
		"""
		try:
			self._cursor.execute('USE {0}'.format(name))
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	def drop_user(self, name_user):
		"""
		*Metodo para eliminar un usuario en especifico en el localhost*

		- `@param name_user: nombre del usuario a eliminar`

		`Ejemplo: con.drop_user('test')`
		"""
		try:
			self._cursor.execute('DROP USER ' + name_user + '@localhost')
			self._db.commit()
			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False


	def create_table(self, name_table, data):
		"""
		*Metodo para crear una tabla dentro de la base de datos*

		- `@param name_table: nombre de la tabla nueva en la base de datos`
		- `@param data: lista de tuplas que pasa las caracteristicas de la tabla`

		Ejemplo:
		`values_table = [('id', 'int'), ('denom', 'CHAR(20)'), ('provin', 'CHAR(10)'), ('PRIMARY KEY (id)',)]`
		`con.create_table('Oficinas', values_table)`

		Ejemplo 2:
		`values_table = [('id', 'int'), ('denom', 'CHAR(20)'), ('provin', 'CHAR(10)'), ('PRIMARY KEY (id)',)]`
		`con.create_table('Oficinas', values_table)`

		`values_table = [('post_id', 'INT'), ('message', 'TEXT'), ('publish_date', 'DATETIME'), ('PRIMARY KEY (post_id)',)]`
		`con.create_table('post', values_table)`
		"""
		try:
			query = 'CREATE TABLE IF NOT EXISTS ' + name_table + ' ('

			for element in data:
				if len(element) > 1:
					for column_data in element:
						query += column_data + ' '

					query += ', '

				else:
					query += element[0]

			query += ')'

			self._cursor.execute(query)
			self._db.commit()

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	# Recibe el nombre de la tabla a eliminar
	def drop_table(self, name_table):
		"""
		*Metodo para eliminar una tabla de la base de datos*

		- `@param name_table: nombre de la tabla que se quiere eliminar`

		`Ejemplo: con.drop_table('personas')`
		"""
		try:
			self._cursor.execute('DROP TABLE IF EXISTS {0}'.format(name_table))
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	def insert_data(self, name_table, values):
		"""
		*Metodo para insertar datos a una tabla de la base de datos*

		- `@param name_table: nombre de la tabla donde ingresaremos los datos
		- `@param values: lista de tuplas con los datos a ingresar a la tabla

		Ejemplo:
		`values = [(1 ,'Norte', 'Bilbao'), (2, 'Extremadura', 'Badajoz')]`
		`con.insert_data('Oficinas', values)`
		"""
		try:
			self._cursor.execute('describe ' + name_table)
			describe = self._cursor.fetchall()

			try:
				for value in values:
					query = 'INSERT INTO ' + name_table + ' VALUES ('
					for val in value:
						if type(val) == int:
							query += str(val) + ', '

						elif type(val) == str:
							query += "'" + val + "', " 

					query_insert = query[:-2] + ')'

					self._cursor.execute(query_insert)

				self._db.commit()

			except:
				assert False, 'Ocurrio un error al insertar los datos'


		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False


	# Recibe el nombre de la tabla donde estara el nombre de la columna a eliminar
	def drop_column(self, name_table, name_column):
		"""
		*Metodo que elimina una columna de una tabla de la base de datos*

		- `@param name_table: nombre de la tabla a seleccionar`
		- `@param name_column: nombre de la columna a eliminar`

		`Ejemplo: con.drop_column('alumnos', 'autor')`
		"""
		try:
			self._cursor.execute('ALTER TABLE ' + name_table + ' drop column ' + name_column)
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	# Recibe el nombre de la tabla y una lista de tuplas
	def add_column(self, name_table, values):
		"""
		*Metodo que agrega una nueva columna a una tabla especifica a la base de datos*

		- `@param name_table: nombre de la tabla que queremos seleccionar`
		- `@param values: es una lista de tuplas con todos los valores que queremos agregar a la tabla`

		Ejemplo:
		`values_column = [('autor', 'varchar(20)', 'not null', 'default', "'Desconocido'")]`
		`con.add_column('alumnos', values_column)`

		"""
		try:

			for value in values:
				query = 'ALTER TABLE '+ name_table + ' add '
				for val in value:
					query += val + ' '

				self._cursor.execute(query)

			self._db.commit()
			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False


	# Recibe nombre de la tabla, nombre de la columna antigua, y nombre de la nueva columna
	def change_column(self, name_table, old_column, new_column):
		"""
		*Metodo que cambia el nombre de una columna de una tabla especifica*

		- `@param name_table: nombre de la tabla que queremos cambiar la columna`
		- `@param old_column: nombre de la tabla que es la actual que esta en la base de datos`
		- `@param new_column: nombre nuevo que queremos asignarles a la columna`

		`Ejemplo: con.change_column('alumnos', 'nombre', 'Nombre')`

		"""
		type_variable = ''
		try:
			self._cursor.execute('describe ' + name_table)
			describe = self._cursor.fetchall()

			for element in describe:
				if element[0] == old_column:
					type_variable = element[1]
					break

			if type_variable != '':
				query = 'ALTER TABLE ' + name_table + ' CHANGE ' + old_column + ' ' + new_column + ' ' + type_variable
				self._cursor.execute(query)
				self._db.commit()

				return True

			else:
				return False

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False

	# Recibe nombre tabla, nombre columna y nuevo tipo de dato
	def modify_column(self, name_table, name_column, new_type_data):
		"""
		*Metodo que modifica el tipo de variable de una columna de una tabla*

		- `@param name_table: nombre de la tabla que queremos seleccionar`
		- `@param name_column: nombre de la columna que queremos modificar el tipo de datos`
		- `@param new_type_data: el nuevo tipo de dato que queremos asignarle`

		`Ejemplo: con.modify_column('alumnos', 'Nombre', 'varchar(60)')`
		"""
		try:
			query = 'ALTER TABLE ' + name_table + ' MODIFY ' + name_column + ' ' + new_type_data
			self._cursor.execute(query)
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False


	# Recibe el nombre de la tabla, lista de tuplas (columna , valor), y una lista de tuplas (condicion, columna, valor)
	def update_data(self, name_table, values_update, conditions):
		"""

		Ejemplo: 
		`values_update = [('edad', '27'), ('nombre', '"luis"')]`
		`values_condition = [('WHERE', 'nombre', '"Luis"'), ('AND', 'edad', '27')]`
		`con.update_data('alumnos', values_update, values_condition)`
		"""
		try:
			query = 'UPDATE ' + name_table + ' SET '

			if len(values_update) == 1:
				for value in values_update:
					query += value[0] + ' = ' + value[1]

			else:
				for value in values_update:
					query += value[0] + ' = ' + value[1] + ', '

			query_update = query[:-2]

			for condition in conditions:
				query_update += ' ' + condition[0] + ' ' + condition[1] + '=' + condition[2]

			self._cursor.execute(query_update)
			self._db.commit()

			return True

		except pymysql.err.InternalError as e:
			code, msg = e.args

			return False


	def execute_query(self, query):
		"""
		*Metodo para ejecutar una query cualquiera*

		- `@param query: ejecutar una query cualquiera de mysql`

		Ejemplo:
		`con.execute_query('SELECT * FROM alumnos')`

		"""

		#try:
		self._cursor.execute(query)

		return self._cursor.fetchall()

		#except pymysql.err.InternalError as e:
		#	code, msg = e.args

		#	return msg


	def execute_query2(self, query):
		"""
		

		"""

		#try:
		self._cursor.execute(query)
		self._db.commit()

		#except:
		#	assert False, "Error query"


	def close_connection(self):
		self._db.close()
