import os
from odoo import fields, models
from datetime import date, datetime
import csv
import requests
import uuid
import boto3 
import pandas as pd

class CronBatchTransaction(models.Model):
    _name="openg2p.cron.batch.transaction"

    def cron_create_batch_transaction(self):
        
        batches_list=self.env["openg2p.disbursement.batch.transaction"].search([("state","=","draft")])

        if not batches_list:
            return

        for batch in batches_list:
            self.create_bulk_transfer_cron(batch)

    def create_bulk_transfer_cron(self,batch):

        beneficiary_transactions = self.env["openg2p.disbursement.main"].search(
            [("batch_id", "=", batch.id)]
        )

        # CSV filename as RequestID+Datetime
        csvname = (
                self.request_id
                + "-"
                + str(datetime.now().strftime(r"%d-%m-%Y-%H:%M"))
                + ".csv"
        )

        with open(csvname, "a") as csvfile:
            csvwriter = csv.writer(csvfile)
            entry = [
                "id",
                "request_id",
                "payment_mode",
                "amount",
                "currency",
                "note",
            ]
            csvwriter.writerow(entry)

            for rec in beneficiary_transactions:
                entry = [
                    rec.id,
                    rec.beneficiary_request_id,
                    "gsma",  # rec.payment_mode or "gsma",
                    rec.amount,
                    "LE",  # rec.currency_id.name,
                    rec.note,
                ]

                # id,request_id,payment_mode,amount,currency,note
                csvwriter.writerow(entry)

        url_token = "http://ops-bk.ibank.financial/oauth/token?grant_type=client_credentials"

        headers_token = {
            'Platform-TenantId': 'ibank-usa',
            'Authorization': 'Basic Y2hhbm5lbC1pYmFuay11c2E6cDEyMzQ='
        }

        try:
            response_token = requests.request("POST", url_token, headers=headers_token)

            response_token_data = response_token.json()
            batch.token_response = response_token_data["access_token"]

        except BaseException as e:
            print(e)

        # Uploading to AWS bucket
        uploaded = self.upload_to_aws(csvname, "paymenthub-ee-dev")

        headers = {"Platform-TenantId": "ibank-usa"}

        files = {
            "data": (csvname, open(csvname, "rb"), "text/csv"),
            "requestId": (None, str(batch.request_id)),
            "purpose": (None, "Bulk transfers"),
            # "checksum": (None, str(self.generate_hash(csvname))),
        }
        url = "http://channel.ibank.financial/channel/bulk/transfer"

        try:
            response = requests.post(url, files=files)
            response_data = response.json()

            batch.transaction_status = "queued"
            batch.transaction_batch_id = "c02a14f0-5e7e-44a1-88eb-5584a21e6f28"

        except BaseException as e:
            print(e)

        # Emitting disbursement event
        # self.env["openg2p.workflow"].handle_tasks("batch_send", self)
        