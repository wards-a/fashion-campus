from flask_restx import Resource

from app.main.api_model.sales_am import SalesApiModel


sales_ns = SalesApiModel.api

@sales_ns.route("")
class SalesController(Resource):
    def get(self):
        pass