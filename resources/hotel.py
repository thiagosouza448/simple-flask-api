from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import sqlite3


def normalize_path_params(cidade=None, 
                        estrelas_min = 0,
                        estrelas_max = 5,
                        diaria_min=0,
                        diaria_max= 10000,
                        limit= 80,
                        offset= 0, **dados ):
    if cidade:
        return {
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "cidade": cidade,
        "limit": limit,
        "offset": offset,
        
        }
    return  {
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset,
        
        }

# consulta por path

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float )
path_params.add_argument('estrelas_max', type=float )
path_params.add_argument('diaria_min', type=float )
path_params.add_argument('diaria_max', type=float )
path_params.add_argument('limit', type=float )
path_params.add_argument('offset', type=float )


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados= path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros =  normalize_path_params(**dados_validos)
        if not parametros.get('cidade'):
            consulta = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta =  "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            and cidade = ? LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        
        hoteis = []
        for linha in resultado:
            hoteis.append({
            "hotel_id": linha[0],
            "nome": linha[1],
            "estrelas":linha[2],
            "diaria": linha[3],
            "cidade": linha[4]
            })


        return {'hotels':  hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="the field estrelas cannot be left blank"  )
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self,hotel_id): 
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "hotel not found"}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"hotel id {} already exists.".format(hotel_id)}, 400
        # elif hotel_id != int:
        #     return {"message": "voce digitou: {}, campo so aceita numeros ".format(hotel_id.upper())}

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save to hotel"}, 500
        return hotel.json()

    @jwt_required()
    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save to hotel"}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel  = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message":"An error ocurred trying to delete"}, 500
            return {'Message':'Hotel :{} deleted.'.format(hotel_id.upper())}
        return {"message": "hotel not found."}, 404
