from __future__ import print_function

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_create_draft():
    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    import os
    from google.oauth2 import service_account
    from google.cloud import language_v1
    import json
    credentials = service_account.Credentials.from_service_account_file("service_account _key.json")
    client = language_v1.LanguageServiceClient(credentials=credentials)

    client = language_v1.LanguageServiceClient.from_service_account_json("service_account _key.json")
    creds, _ = google.auth.default()

    google.auth.load_credentials_from_file("service_account _key.json", scopes=None, default_scopes=None, quota_project_id=None, request=None)

    delegated_credentials = credentials.with_subject('iiitprep.store@gmail.com')
    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message.set_content('This is automated draft mail')

        message['To'] = 'iiitprep.store@gmail.com'
        message['From'] = 'iiitprep.store@gmail.com'
        message['Subject'] = 'Automated draft'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
                'raw': encoded_message
        }
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None

    return draft




if __name__ == '__main__':
    gmail_create_draft()