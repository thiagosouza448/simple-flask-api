from flask import Flask, jsonify
from flask_restful import Resource, Api
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserLogin, UserRegister, UserLogout
from resources.site import Sites, Site
from flask_jwt_extended import JWTManager, get_jwt_header
from blacklist import BLACKLIST

# TODO: settings flask database sqlalchemy 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

# TODO: config JWT
api = Api(app)
jwt = JWTManager(app)



@app.before_first_request
def cria_banco():
    banco.create_all()

# TODO: JWR verify black list with token 
@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

# TODO: JWR check if the user is logged in
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({"message": "You have been logged out."}),401



# TODO: routes endopoints that are being used
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuario/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')




 


if __name__ == "__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
