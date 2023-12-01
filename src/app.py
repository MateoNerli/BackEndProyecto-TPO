from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:0306@localhost/proyectotpo'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino las tablas
class Users(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    user=db.Column(db.String(100))
    email=db.Column(db.String(400))
    password=db.Column(db.String(100))
    role=db.Column(db.Integer)
    def __init__(self,nombre,apellido,user,email,password,role):   #crea el  constructor de la clase
        self.nombre=nombre
        self.apellido=apellido
        self.user=user
        self.email=email
        self.password=password
        self.role=role


class Producto(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    descripcion=db.Column(db.String(400))
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,precio,descripcion,imagen):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.precio=precio
        self.descripcion=descripcion
        self.imagen=imagen


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','descripcion','imagen')
producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','user','email','password','role')
user_schema=UserSchema()            # El objeto producto_schema es para traer un product
users_schema=UserSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto



# crea los endpoint o rutas (json)
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro

@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()                     # confirma el delete
    return producto_schema.jsonify(producto) # me devuelve un json con el registro eliminado


@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    descripcion=request.json['descripcion']
    imagen=request.json['imagen']
    new_producto=Producto(nombre,precio,descripcion,imagen)
    db.session.add(new_producto)
    db.session.commit() # confirma el alta
    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
 
    producto.nombre=request.json['nombre']
    producto.precio=request.json['precio']
    producto.stock=request.json['stock']
    producto.imagen=request.json['imagen']


    db.session.commit()    # confirma el cambio
    return producto_schema.jsonify(producto)    # y retorna un json con el producto
 
 
@app.route('/users',methods=['GET'])
def get_Users():
    all_users=Users.query.all()         # el metodo query.all() lo hereda de db.Model
    result=users_schema.dump(all_users)  # el metodo dump() lo hereda de ma.schema y
                                                    # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

@app.route('/users/<id>',methods=['GET'])
def get_user(id):
    user=Users.query.get(id)
    return user_schema.jsonify(user)

@app.route('/users', methods=['POST']) # crea ruta o endpoint
def create_user():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    user=request.json['user']
    email=request.json['email']
    password=request.json['password']
    role=request.json['role']
    new_user=Users(nombre,apellido,user,email,password,role)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/users/<id>' ,methods=['PUT'])
def update_user(id):
    user=Users.query.get(id)
 
    user.nombre=request.json['nombre']
    user.apellido=request.json['apellido']
    user.user=request.json['user']
    user.email=request.json['email']
    user.password=request.json['password']
    user.role=request.json['role']

    db.session.commit()    # confirma el cambio
    return user_schema.jsonify(user)    # y retorna un json con el producto

@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    user=Users.query.get(id)
    db.session.delete(user)
    db.session.commit()                     # confirma el delete
    return user_schema.jsonify(user)


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)