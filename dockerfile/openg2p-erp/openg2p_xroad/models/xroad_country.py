from odoo import api, fields, models,http
from odoo.http import request
import requests, json


class XRoadCountryCodes(models.Model):
    _name = "xroad.country"
    _description = "Country Codes"

    xroad_config_name = fields.Many2one(
        "xroad.config",
        string="Security Server Configuration"
    )
    country_details = fields.Text(
        string="Country Details"
    )

    @api.model
    def get_country_codes(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])

        try:
            url = str(server_detail.url) + "/CodeList/GetCountryCodes"
            headers = {
                'accept': 'text/plain'
            }

            response = requests.request("GET", url, headers=headers)

            self.country_details = json.loads(response.text)

            return {
                'values': self.country_details
            }
        except BaseException as e:
            print(e)

        # return {'items': self.country_details}
    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]