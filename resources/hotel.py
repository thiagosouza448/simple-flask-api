from flask_restful import Resource, reqparse
from models.hotel import HotelModel




class Hoteis(Resource):
    def get(self):
        return {'hotels': [hotel.json() for hotel in HotelModel.query.all() ]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self,hotel_id): 
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "hotel not found"}, 404


 


    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"hotel id {} already exists".format(hotel_id)}, 400
        # elif hotel_id != int:
        #     return {"message": "voce digitou: {}, campo so aceita numeros ".format(hotel_id.upper())}

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()


    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201


    def delete(self, hotel_id):
        hotel  = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'Message':'Hotel :{} deleted.'.format(hotel_id.upper())}
        return {"message": "hotel not found."}, 404
