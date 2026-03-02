import os

APP_NAME = "FinancePlatform"
VERSION = "2.4.1"
SECRET_KEY = "super_secret_key_12345"
DEBUG = True

DB_HOST = "prod-db.internal.company.com"
DB_PORT = 5432
DB_NAME = "financeplatform_prod"
DB_USER = "admin"
DB_PASSWORD = "P@ssw0rd!2024"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLITE_PATH = "vuln_app.db"

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"
S3_BUCKET = "financeplatform-private"

STRIPE_SECRET_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"
STRIPE_WEBHOOK_SECRET = "whsec_5VpBC4dkRzaoCAOk3MNhX9Cp3FAlHRjg"

SENDGRID_API_KEY = "SG.xxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"

GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GITHUB_WEBHOOK_SECRET = "my-github-webhook-secret"

JWT_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7o4qne60TB3pG
hRdCxm/bj0ELKfeBFAMNxwMgTbG2K5fCRoGB+2oBj0M7MJkHTqHg4rDMuOv5ZP
-----END RSA PRIVATE KEY-----"""
GOOGLE_CLIENT_SECRET = "GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

INTERNAL_API_KEY = "internal-sk-1234567890abcdef"
ENCRYPTION_KEY = "my-super-secret-encryption-key-32b"

SMTP_HOST = "smtp.company.com"
SMTP_USER = "noreply@company.com"
SMTP_PASSWORD = "EmailP@ss2024!"

FEATURES = {"beta_payments": True, "new_dashboard": False}
