from odoo import api, fields, models
import requests
from datetime import datetime
import json


class XRoadService(models.Model):
    _name = "xroad.service"
    _description = "Services available"

    xroad_config_name = fields.Many2one(
        "xroad.config"
    )
    date_now = fields.Datetime(
        string="Date",
        default=datetime.now()
    )
    date_before = fields.Datetime(
        string="dateBefore",
        default=datetime.now()
    )
    page_size = fields.Integer(
        string="Page Size",
        default=1,
    )
    status = fields.Char(
        string="Status",
        default="Published"
    )
    service_details = fields.Text(
        string="Service Details"
    )

    def get_services(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/Service"
            headers = {
                'accept': 'text/plain',
                'page': str(self.page_size),
                'date': str(self.date_now),
                'dateBefore': str(self.date_before),
                'status': str(self.status)
            }

            response = requests.request("GET", url, headers=headers)

            self.service_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]