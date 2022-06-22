from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from data_base import db
import json

CREDENTIALS_FILE = 'creds.json'
credentials = Credentials.from_service_account_file(CREDENTIALS_FILE)
service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1HHBxWVvx0Qy7zWMIek2A8neDAZAFH-HkWPiqRi9RAyg'

def write_feedback(user_id, feedback):
  service.spreadsheets().values().append(
      spreadsheetId=spreadsheet_id,
      range='feedback!A2:B2',
      # body = {
      valueInputOption = "USER_ENTERED",
      insertDataOption = "INSERT_ROWS",
      body = {"values":[[f"{user_id}", f"{feedback}"]]}
    ).execute()

def read_farmers():
  values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='farmers!A2:D',
    majorDimension='ROWS'
  ).execute()
  parsed_values = values['values']
  return parsed_values