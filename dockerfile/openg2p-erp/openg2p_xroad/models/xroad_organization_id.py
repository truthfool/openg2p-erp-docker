from odoo import api, fields, models
import requests
from datetime import datetime
import json


class XRoadOrganizationById(models.Model):
    _name = "xroad.organization.id"
    _description = "Organization by ID"

    xroad_config_name = fields.Many2one(
        "xroad.config"
    )
    showheader = fields.Boolean(
        string="show Header"
    )
    organization_id = fields.Text(
        string="Organization ID"
    )
    organization_details = fields.Text(
        string="Organization Details"
    )

    def get_organization_by_id(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/Organization/" + str(self.organization_id)

            headers = {
                'accept': 'text/plain',
                # 'showHeader': ",
            }

            response = requests.request("GET", url, headers=headers)
            # print(response.status_code)
            self.organization_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]
