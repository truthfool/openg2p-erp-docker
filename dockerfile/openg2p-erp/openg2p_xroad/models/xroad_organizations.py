from odoo import api, fields, models
import requests
from datetime import datetime
import json


class XRoadOrganizations(models.Model):
    _name = "xroad.organizations"
    _description = "Organizations available"

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
        string="status",
        default="Published"
    )
    organization_details = fields.Text(
        string="Organization Details"
    )

    def get_organizations(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/Organization"
            headers = {
                'accept': 'text/plain',
                'page': str(self.page_size),
                'date': str(self.date_now),
                'dateBefore': str(self.date_before),
                'status': str(self.status)
            }

            response = requests.request("GET", url, headers=headers)

            self.organization_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]