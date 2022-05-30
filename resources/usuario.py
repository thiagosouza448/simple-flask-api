from flask_jwt_extended.utils import create_refresh_token
from flask_restful import Resource,reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field LOGIN cannot be left blank')
atributos.add_argument('senha', type=str, required=True, help='The field SENHA cannot be left blank')

class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"message":"User not found"}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {"message":"User deleted"}, 200
        return {"message":"user not found"}, 404


#/cadastro
class UserRegister(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help='The field LOGIN cannot be left blank')
        atributos.add_argument('senha', type=str, required=True, help='The field SENHA cannot be left blank')

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message":"The login {} alredy exists".format(dados['login'].upper())}

        user = UserModel(**dados)
        user.save_user()
        return {"message":"user created successfully"}, 201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {"acess_token": token_de_acesso, "refresh_token": refresh_token},200
        return {"message": "The username or passoword is incorrect"},401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "logged out successfully"}, 200
