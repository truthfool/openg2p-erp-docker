from odoo import api, fields, models
import requests,json


class XRoadMunicipalityCodes(models.Model):
    _name = "xroad.municipality"
    _description = "Municipality Codes"

    xroad_config_name = fields.Many2one(
        "xroad.config",
        string="Security Server Configuration"
    )
    municipality_details = fields.Text(
        string="Municipality Details"
    )

    def get_municipality_codes(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/CodeList/GetMunicipalityCodes"
            headers = {
                'accept': 'text/plain'
            }

            response = requests.request("GET", url, headers=headers)

            self.municipality_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]