from odoo import api, fields, models

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os


class DetailedPaymentStatus(models.Model):
    _name = "openg2p.detailed.payment.status"
    _description = "Displaying detailed payment status for each batch"

    batch_id = fields.Many2one(
        "openg2p.disbursement.batch.transaction",
        string="Batch ID"
    )
    beneficiary_id = fields.Text(
        string="Beneficiary ID"
    )
    errorInformation = fields.Text(
        string="Error Information"
    )
    workflowInstanceKey = fields.Text(
        string="Workflow Instance Key"
    )
    transactionId = fields.Text(
        string="Transaction ID"
    )
    startedAt = fields.Text(
        string="Started At"
    )
    completedAt = fields.Text(
        string="Completed At"
    )
    status = fields.Text(
        string="Status"
    )
    statusDetail = fields.Text(
        string="Status Detail"
    )
    payeeDfspId = fields.Text(
        string="Payee dfsp ID"
    )
    payeePartyId = fields.Text(
        string="Payee Party ID"
    )
    payeePartyIdType = fields.Text(
        string="Payee Party Id Type"
    )
    payeeFee = fields.Text(
        string="Payee Fee"
    )
    payeeFeeCurrency = fields.Text(
        string="Payee Fee Currency"
    )
    payeeQuoteCode = fields.Text(
        string="Payee Quote Code"
    )
    payerDfspId = fields.Text(
        string="Payer Dfsp ID"
    )
    payerPartyId = fields.Text(
        string="Payer Party Id"
    )
    payerPartyIdType = fields.Text(
        string="Payer Party Id Type"
    )
    payerFee = fields.Text(
        string="Payer Fee"
    )
    payerFeeCurrency = fields.Text(
        string="Payer Fee Currency"
    )
    payerQuoteCode = fields.Text(
        string="Payer Quote Code"
    )
    amount = fields.Text(
        string="Amount"
    )
    currency = fields.Text(
        string="Currency"
    )
    direction = fields.Text(
        string="Direction"
    )
    batchId = fields.Text(
        string="Batch ID"
    )
