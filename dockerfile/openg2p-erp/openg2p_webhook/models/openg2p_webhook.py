from odoo import models, fields
import json
from .task_email import send_mail
from .webhook import webhook_event


class CreateWebhook(models.Model):
    _name = "openg2p.webhook"
    _description = "Create Webhook for Events"

    webhook_url = fields.Text(
        blank=False
    )

    events = fields.Many2many(
        "openg2p.task.subtype",
        relation="openg2p_webhook_subtypes",
        required=True,
        string="Events"
    )

    type_data = fields.Selection(
        [
            ("JSON", "JSON"),
            ("XML", "XML"),
        ]
        ,
        string="Type",
        required=True
    )

    # Send events to webhook URL and emails
    def create_notification(self, process, event_code, obj_ids):

        task_subtype_id = self.env["openg2p.process"].get_id_from_ext_id(event_code)

        task_subtype = self.env["openg2p.task.subtype"].search([("id", "=", task_subtype_id)])

        context = json.loads(process.context)

        latest_task_id = json.loads(context["tasks"])[-1]

        latest_task = self.env["openg2p.task"].search([("id", "=", latest_task_id)])

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        if len(task_subtype) > 0:
            task_subtype = task_subtype[0]

            if not isinstance(obj_ids, bool):
                for obj_id in obj_ids:
                    # Sending Emails
                    send_mail(latest_task.assignee_id.name, latest_task.assignee_id.email,
                              f"{base_url}/web#id={obj_id}&model={task_subtype.entity_type_id}")

                    # Sending event to webhook url
                    webhooks = self.env["openg2p.webhook"].search([("events", "in", (task_subtype_id,))])
                    print(webhooks,len(webhooks))
                    for webhook in webhooks:
                        webhook_data = {
                            "eventName": task_subtype.name,
                            "value": {
                                "id": obj_id,
                                "details": latest_task.context or ""
                            }
                        }
                        print(webhook_data)
                        webhook_event(webhook_data, webhook.webhook_url, webhook.type_data)
