# -*- coding:utf8 -*-
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import arrow

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = '.credentials'
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def retrieve_projects():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1qB7xhICnUR6pJRH9Oy7ResxX-mltfWFyLfsv5Z0GXhs'
    rangeName = 'projets!A2:Y100'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    return values


def generate_id(project):
    h = arrow.get(project[0], 'DD/MM/YYYY HH:mm:ss').timestamp
    n = project[1]
    return '{}{}'.format(h,n)


DB_SHEET_REF = {
    'nom_projet': 1,
    'nom_asso': "Association Culturelle Africaine de l'Université Laval",
    'type_projet': 2,
    'lieu_projet': 3,
    'date_heure': [4, 5],
    'desc_projet': 6,
    'crit_initiative_potentiel': 7,
    'crit_retombees': 8,
    'crit_rayonnement': 9,
    'crit_nombre': 10,
    'crit_finance': 11,
    'fichier_opt_1': 'input_19',
    'fichier_opt_2': 'input_20',
    'fichier_opt_3': 'input_21',
    'fichier_opt_4': 'input_22',
    'fichier_opt_5': 'input_61',
    'budget_fichier': 14,
    'montant_demande': 12,
    'nom_resp': 17,
    'prenom_resp': 18,
    'courriel_resp': 24,
    'adresse_post_resp': 20,
    'ville_resp': 21,
    'province_resp': 22,
    'code_postal_resp': 23,
    'phone_resp': 19,
    'matricule_resp': 16,
    'liste_organisateurs': 13,
    'cheque_nom': "Association Culturelle Africaine de l'Université Laval",
    'cheque_adresse_post': "2344-2325, rue de l'Université, Pavillon Alphonse-Desjardins, C.P. 31",
    'cheque_ville': 'Québec',
    'cheque_province': 'Québec',
    'cheque_code_postal': 'G1V 0A6',
    'check_conditions': 'Oui',
    'check_conforme': 'Oui',
}

if __name__ == '__main__':
    get_credentials()