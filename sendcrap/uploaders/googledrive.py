#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
DOCDOCDOC
'''
import sys, os
import httplib2

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage 
from oauth2client.client import AccessTokenRefreshError 
from oauth2client.tools import run

from sendcrap import utils

# Copy your credentials from the APIs Console
SENDCRAP_ID     = '282067003773.apps.googleusercontent.com'
SENDCRAP_SECRET = 'ImqWr2qLfdmAHQnkam4YfEty'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# http://fr.nicosphere.net/utilisation-de-lapi-goo-gl-avec-oauth-et-python-2403/
def upload_file(file_path):
    ''' '''
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(SENDCRAP_ID, SENDCRAP_SECRET,
                               OAUTH_SCOPE, REDIRECT_URI)

    storage = Storage('googl.tok')
    credentials = storage.get() 
    # Si le fichier n'existe pas, ou n'est pas valide, on demande une 
    # authorisation, le fonctionnement est directement dans l'API de 
    # google. 
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)

    # La requete http est préparé. 
    http = httplib2.Http() 
    http = credentials.authorize(http) 
    drive_service = build('drive', 'v2', http=http)

    try:
        # Insert a file
        media_body = MediaFileUpload(file_path, 
                                     mimetype="'application/x-tar'",
                                     resumable=True)
        body = {
          'title': os.path.basename(file_path),
          'description': 'A test document',
          'mimeType': "'application/x-tar'",
          'shared': True
        }
        request = drive_service.files().insert(
            body=body, media_body=media_body)
        response = None
        while True:
            status, response = request.next_chunk() # define chunk size ?
            if status:
                utils.cli_progressbar("Uploaded: ", 
                                      int(status.progress() * 100))
            if response is not None: break
        utils.cli_progressbar("Uploaded: ", 100) # Ugly
        utils.output("\tUpload Complete!")
        
        permissions = {
              'role': 'reader',
              'type': 'anyone',
              'value': "",
              'withLink': True
        }
        drive_service.permissions().insert(
            fileId=response['id'], body=permissions).execute()
        return drive_service.files().get(
            fileId=response['id']).execute()['alternateLink']
            
    except AccessTokenRefreshError:
        utils.forced_output("The credentials have been revoked or "
                            "expired, please re-run the application to "
                            "re-authorize")
        sys.exit(0)
        
               
if __name__ == '__main__':
    # Testing
    f = os.path.abspath('./data/test-data/randomcrap.txt')
    url = upload_file(f)
    print url
