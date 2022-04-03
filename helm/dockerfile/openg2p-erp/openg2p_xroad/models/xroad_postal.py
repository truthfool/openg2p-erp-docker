from odoo import api, fields, models
import requests,json


class XRoadPostalCodes(models.Model):
    _name = "xroad.postal"
    _description = "Postal Codes"

    xroad_config_name = fields.Many2one(
        "xroad.config",
        string="Security Server Configuration"
    )
    postal_details = fields.Text(
        string="Postal Details"
    )

    def get_postal_codes(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/CodeList/GetPostalCodes"
            headers = {
                'accept': 'text/plain'
            }

            response = requests.request("GET", url, headers=headers)

            self.postal_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]