# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class ZPopup(http.Controller):

    @http.route('/my_rpc', type="json", auth='public', methods=["POST"], csrf="false")
    def my_rpc(self, model_name, method_name, args):
        Model = request.env[model_name]
        method = getattr(Model, method_name)
        result = method(*args)
        # return json.dumps(result)
        return result

    
    # @http.route('/student/name', auth='public', type="json", methods=['POST'])
    # def index(self, **kw):
    #     result = self.env['z_popup.student'].get_sid(kw['arg1'], kw['arg2'])
    #     return json.dumps(result)

