from flask_restx import Resource

from app.main.api_model.sales_am import SalesApiModel
from app.main.utils.token import token_required
from app.main.utils.custom_decorator import admin_level
from app.main.service.sales_service import (
    get_total_sales
)


sales_ns = SalesApiModel.api

@sales_ns.route("")
class SalesController(Resource):
    @token_required
    @admin_level
    def get(user, self):
        return get_total_sales()