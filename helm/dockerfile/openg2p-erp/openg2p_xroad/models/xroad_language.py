from odoo import api, fields, models
import requests,json


class XRoadLanguages(models.Model):
    _name = "xroad.language"
    _description = "Languages available"

    xroad_config_name = fields.Many2one(
        "xroad.config",
        string="Security Server Configuration"
    )
    language_details = fields.Text(
        string="Language Details"
    )

    def get_language_codes(self):
        server_detail = self.env["xroad.config"].search([("id", "=", self.xroad_config_name.id)])
        try:
            url = str(server_detail.url) + "/CodeList/GetLanguageCodes"
            headers = {
                'accept': 'text/plain'
            }

            response = requests.request("GET", url, headers=headers)

            self.language_details = json.loads(response.text)
        except BaseException as e:
            print(e)

    def name_get(self):
        return [(res.id, res.xroad_config_name.server_name) for res in self]