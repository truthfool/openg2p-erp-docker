from odoo import api, fields, models
import requests
from datetime import datetime
import json


class XRoadServiceById(models.Model):
    _name = "xroad.service.id"
    _description = "Services available by ID"

    xroad_config_name = fields.Many2one(
        "xroad.config"
    )
    show_header = fields.Boolean(
        string="Show Header",
        default=False
    )
    service_details = fields.Text(
        string="Service Details"
    )

    def get_service_by_id(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/Service"
            headers = {
                'accept': 'text/plain',
                # 'showHeader': self.show_header
            }

            response = requests.request("GET", url, headers=headers)

            self.service_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]