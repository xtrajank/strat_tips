import requests

class Qb:
    def __init__(self, access_token, realm_id):
        self.access_token = access_token
        self.realm_id = realm_id

    def fetch_quickbooks_data(self, endpoint):
        """ Generic function to fetch data from QuickBooks API """
        BASE_URL = f'https://quickbooks.api.intuit.com/v3/company/{self.realm_id}'

        headers = {
            "Authorization": f'Bearer {self.access_token}',
            "Accept": "application/json"
        }

        response = requests.get(f'{BASE_URL}/{endpoint}', headers=headers)

        if response.status_code != 200:
            return {"error": response.json(), "status_code": response.status_code}
        
        print(f"Fetching: {BASE_URL}/{endpoint}")
        print(f"Headers: {headers}")
        print(f"Response Code: {response.status_code}")
        print(f"Response: {response.text}")


        return response.json()

    def get_invoices(self):
        return self.fetch_quickbooks_data("query?query=SELECT * FROM Invoice")

    def get_cash_flow(self):
        return self.fetch_quickbooks_data("reports/CashFlow")

    def get_profit_loss(self):
        return self.fetch_quickbooks_data("reports/ProfitAndLoss")
