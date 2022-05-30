from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {"message": "site not found"}, 404

    @jwt_required()
    def post(self, url):
        if SiteModel.find_site(url):
            return {"Message": "The site {} already exists.".format(url)}, 400
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {"Message": "An internal error ocurred trying to create a new site"}, 500
        return site.json()

    @jwt_required()
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {"message": "Site deleted"}
        return {"message": "site not found"}, 404
