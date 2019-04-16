import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):  #Inherit from Resource class
		
	parser= reqparse.RequestParser()
	parser.add_argument('imdb_score',
		type=float,
		required=False,
		help="This field cannot be left blank"
	)
	parser.add_argument('_99popularity',
		type=float,
		required=False,
		help="This field cannot be left blank"
	)
	parser.add_argument('director',
		type=str,
		required=True,
		help="This field cannot be left blank"
	)
	parser.add_argument('genre',
		type=str,
		required=True,
		help="This field cannot be left blank"
	)


	def get(self,name):
		item = self.find_by_name(name)
		if item:
			return item
		return {'message':'Item not found'}, 404	

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()

		if row:
			return {"item" : {'id':row[0],'name': row[1],'imdb_score':row[2],'_99popularity':row[3], 'director': row[4],'genre':row[5]}}

	@jwt_required()
	def post(self,name):
		#Error first approach
		if self.find_by_name(name):
			return {'message':"Movie with title '{}' already exists.".format(name)}, 400

		data = Item.parser.parse_args()
		item = {'name': name,'imdb_score':data['imdb_score'],'_99popularity':data['_99popularity'], 'director': data['director'],'genre':data['genre']}
		#print(item)
		#exit()
		try:
			self.insert(item)
		except:
			return {"message":"An error occurred inserting the Movie"}, 500

		return item, 201

	@classmethod
	def insert(cls,item):

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (NULL,?, ?, ? , ?,?)"
		cursor.execute(query, (item['name'], item['imdb_score'],item['_99popularity'], item['director'],item['genre']))

		connection.commit()
		connection.close()
	
	@jwt_required()
	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()

		return {'message': 'Item deleted'}

	@jwt_required()
	def put(self,name): #POST idempotent
		#data= request.get_json()
		data=Item.parser.parse_args()

		item = self.find_by_name(name)
		updated_item={'name':name, 'genre':data['genre']}
		updated_item1 = {'name': name,'imdb_score':data['imdb_score'],'_99popularity':data['_99popularity'], 'director': data['director'],'genre':data['genre']}
		

		if item is None:
			try:
				self.insert(updated_item1)
			except:
				return {"message":"An error occurred inserting the Movie"}, 500

			return updated_item1
		else:
			try:
				self.update(updated_item)
				#print("Only genre column updated")
			except:
				return {"message":"An error occurred updating the Movie"}, 500

			return updated_item

	@classmethod
	def update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET genre=? WHERE name=?"
		cursor.execute(query, (item['genre'],item['name']))

		connection.commit()
		connection.close()
	


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items"
		result = cursor.execute(query)
		items = []
		for row in result:
			items.append({'id':row[0],'name': row[1],'imdb_score':row[2],'_99popularity':row[3], 'director': row[4],'genre':row[5]})

		connection.close()

		return {'items':items}
