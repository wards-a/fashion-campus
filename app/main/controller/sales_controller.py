from flask_restx import Namespace, Resource, reqparse, fields

from app.main.utils.token import token_required
from app.main.utils.custom_decorator import admin_level
from app.main.service.sales_service import (
    get_total_sales
)


sales_ns = Namespace("sales")
headers = reqparse.RequestParser()
headers.add_argument("Authentication", required=True, location="headers", help="Jwt-Token")

_response_data = sales_ns.model("TotalSalesData", {
    "total": fields.Integer(example="180000")
})

_response = sales_ns.model("TotalSales", {
    "status": fields.Boolean(example="True"),
    "message": fields.String(example="Success"),
    "data": fields.Nested(_response_data)
})

@sales_ns.route("")
class SalesController(Resource):
    @sales_ns.expect(headers)
    @sales_ns.response(200, "Success", _response)
    @token_required
    @admin_level
    def get(user, self):
        return get_total_sales()