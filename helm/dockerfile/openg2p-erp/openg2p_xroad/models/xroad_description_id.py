from odoo import api, fields, models
import requests, json
from jinja2 import Environment
from datetime import datetime


class XRoadGeneralDescriptionById(models.Model):
    _name = "xroad.description.id"
    _description = "General Description about a Service"

    xroad_config_name = fields.Many2one(
        "xroad.config",
        string="Security Server Configuration"
    )
    description = fields.Text(
        string="Description"
    )
    descriptionId = fields.Text(
        string="Service ID"
    )
    show_header = fields.Boolean(
        string="showHeader",
        default=False
    )

    def get_description_by_id(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/GeneralDescription"
            headers = {
                'accept': 'text/plain',
                'id': str(self.descriptionId)
            }

            response = requests.request("GET", url, headers=headers)

            self.description = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]