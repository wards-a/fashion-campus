from flask_restx import Resource

from app.main.api_model.sales_am import SalesApiModel
from app.main.utils.token import token_required
from app.main.service.sales_service import (
    get_total_sales
)


sales_ns = SalesApiModel.api

@sales_ns.route("")
class SalesController(Resource):
    @token_required
    def get(user, self):
        # check not admin
        if user.is_admin.value == "0":
            return {"code": 403, "message": "Does not have access", "data": [{"total": 0}]}, 403
        return get_total_sales()