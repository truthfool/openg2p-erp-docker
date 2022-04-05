from odoo import api, fields, models


class XRoadConfig(models.Model):
    _name = "xroad.config"
    _description = "Configuration for connecting to security server"

    server_name = fields.Text(
        string="Security Server Name",
        required=True
    )
    xroad_username = fields.Char(
        string="UserName",
        required=True
    )
    xroad_password = fields.Char(
        string="Password",
        required=True
    )
    url = fields.Text(
        string="URL",
        required=True
    )

    def name_get(self):
        return [(res.id, res.server_name) for res in self]