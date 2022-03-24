from odoo import api, fields, models
import requests, json
from datetime import datetime


class XRoadGeneralDescription(models.Model):
    _name = "xroad.description"
    _description = "General Description"

    xroad_config_name = fields.Many2one(
        "xroad.config",
        string="Security Server Configuration"
    )
    description = fields.Text(
        string="Description"
    )
    date = fields.Datetime(
        string="Date",
        default=datetime.now()
    )
    dateBefore = fields.Datetime(
        string="Date Before",
        default=datetime.now()
    )
    page = fields.Integer(
        string="Page Size",
        default=1
    )
    descriptionId = fields.Text(
        string="Service ID"
    )

    def get_description(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/GeneralDescription"
            headers = {
                'accept': 'text/plain',
                'page': str(self.page),
                'date': str(self.date),
                'dateBefore': str(self.dateBefore)
            }

            response = requests.request("GET", url, headers=headers)

            self.description = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]