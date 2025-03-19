import requests
from flask import Flask, request
from requests_oauthlib import OAuth2Session
from config import Config
from quickbooks import Qb
import pandas as pd

def quickbooks_authorization():
    QB_AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
    QB_TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    SCOPE = ["com.intuit.quickbooks.accounting"]

    # get authorization url
    oauth = OAuth2Session(Config.quickbooks_client_id, redirect_uri=Config.quickbooks_redirect_uri, scope=SCOPE)
    authorization_url, state = oauth.authorization_url(QB_AUTH_URL)

    print("Go to the following URL and authorize:", authorization_url)

    # with authorization, quickbooks will direct to redirect uri with a code
    auth_code = request.args.get("code")
    realm_id = request.args.get("realmId")

    # exchange code for tokens
    token_data = oauth.fetch_token(QB_TOKEN_URL, client_secret=Config.quickbooks_client_secret, code=auth_code)
    print("Quickbooks connected successfully!")

    qb = Qb(token_data["access_token"], auth_code, realm_id)

    return qb

def fetch_quickbooks_data(authorized_quickbooks, endpoint):
    BASE_URL = f'https://quickbooks.api.intuit.com/v3/company/{authorized_quickbooks.realm_id}'

    headers = {
        "Authorization": f'Bearer {authorized_quickbooks.access_token}',
        "Accept": "application/json"
    }

    response = requests.get(f'{BASE_URL}/{endpoint}', headers=headers)
    return response.json()

def get_invoices(client_quickbooks):
    invoices = fetch_quickbooks_data(client_quickbooks, "query?query=SELECT * FROM Invoice")

    return invoices

def get_cash_flow(client_quickbooks):
    cash_flow = fetch_quickbooks_data(client_quickbooks, "reports/CashFlow")

    return cash_flow

def get_profit_loss(client_quickbooks):
    profit_loss = fetch_quickbooks_data("reports/ProfitAndLoss")

    return profit_loss

def process_data(invoices, cash_flow, profit_loss):
    invoice_df = pd.DataFrame(invoices["Invoice"])
    invoice_df = invoice_df[["Id", "TotalAmt", "Balance", "TxnDate"]]

    cash_flow_df = pd.DataFrame(cash_flow["Rows"]["Row"])

    profit_loss_df = pd.DataFrame(profit_loss["Rows"]["Row"])