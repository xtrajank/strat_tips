# load env variables
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.quickbooks_client_id = os.getenv("QUICKBOOKS_CLIENT_ID")
        self.quickbooks_client_secret = os.getenv("QUICKBOOKS_CLIENT_SECRET")
        self.quickbooks_redirect_uri = os.getenv("QUICKBOOKS_REDIRECT_URI")

        self.stripe_client_id = os.getenv("STRIPE_CLIENT_ID")
        self.stripe_client_secret = os.getenv("STRIPE_CLIENT_SECRET")
        self.stripe_redirect_uri = os.getenv("STRIPE_REDIRECT_URI")

        self.vertex_ai_project = os.getenv("GOOGLE_PROJECT_ID")

        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.quickbooks_auth_url = "https://appcenter.intuit.com/connect/oauth2"
        self.quickbooks_token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

        self.scope = ["com.intuit.quickbooks.accounting"]

        required_vars = [
            "QUICKBOOKS_CLIENT_ID", "QUICKBOOKS_CLIENT_SECRET", "QUICKBOOKS_REDIRECT_URI",
            "GOOGLE_PROJECT_ID", "OPENAI_API_KEY"
        ]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"ERROR: Missing environment variable {var}")
