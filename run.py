# -*- coding:utf8 -*-
import sys, json

import requests
from flask import Flask, make_response, redirect, render_template, request, session
from forms import ProjectForm
from storage import retrieve_projects, DB_SHEET_REF


app = Flask(__name__)

WEB_INPUTS = {
    'nom_projet': 'input_1',
    'nom_asso': 'input_3',
    'type_projet': 'input_57',
    'lieu_projet': 'input_7',
    'date_heure': 'input_59',
    'desc_projet': 'input_10',
    'crit_initiative_potentiel': 'input_12',
    'crit_retombees': 'input_13',
    'crit_rayonnement': 'input_14',
    'crit_nombre': 'input_15',
    'crit_finance': 'input_16',
    'fichier_opt_1': 'input_19',
    'fichier_opt_2': 'input_20',
    'fichier_opt_3': 'input_21',
    'fichier_opt_4': 'input_22',
    'fichier_opt_5': 'input_61',
    'budget_fichier': 'input_24',
    'montant_demande': 'input_25',
    'nom_resp': 'input_29',
    'prenom_resp': 'input_30',
    'courriel_resp': 'input_31',
    'adresse_post_resp': 'input_32.1',
    'ville_resp': 'input_32.3',
    'province_resp': 'input_32.4',
    'code_postal_resp': 'input_32.5',
    'phone_resp': 'input_33',
    'matricule_resp': 'input_34',
    'liste_organisateurs': 'input_35',
    'cheque_nom': 'input_38',
    'cheque_adresse_post': 'input_60.1',
    'cheque_ville': 'input_60.3',
    'cheque_province': 'input_60.4',
    'cheque_code_postal': 'input_60.5',
    'check_conditions': 'input_46.1',
    'check_conforme': 'input_47.1',
}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', ' POST'])
def index():
    form = ProjectForm()
    projects = retrieve_projects()
    response = make_response(render_template('index.html', form=form, projects=enumerate(projects)))
    response.headers['Access-Control-Allow-Origin'] = '*'

    if request.method == 'POST':
        project = projects[int(request.form.get('id'))]
        data = {}
        for ref, fieldname in WEB_INPUTS.items():
            if ref.startswith('fichier'):
                continue
            if ref == 'nom_asso' or ref.startswith('che'):
                data[fieldname] = DB_SHEET_REF[ref]
                continue
            if ref == 'date_heure':
                data[fieldname] = ' '.join([project[c] for c in DB_SHEET_REF[ref]])
                continue
            try:
                data[fieldname] = project[DB_SHEET_REF[ref]]
            except IndexError:
                continue
        # s = requests.Session()
        # url = 'https://www.bve.ulaval.ca/formulaires/formulaire-de-demande-de-soutien-financier/#gf_27'
        url = 'http://localhost:5000/mock'
        r = requests.post(url, data)
        res = json.loads(r.text)
        response = make_response(render_template('index.html', form=form, projects=enumerate(projects),
                                                 alert=res[0]['msg'], success=res[0]['success'],
                                                 fields=res[0]['fields']))
        # r = s.post(url, data=data)
        # print(r.text, file=sys.stderr)
    return response


@app.route('/mock', methods=['GET', 'POST'])
def mock():
    required = []
    for ref, fieldname in WEB_INPUTS.items():
        if '_opt' not in ref:
            if request.form.get(fieldname) is not None:
                continue
            required.append(ref)
    if not required:
        alert = u'Le formulaire a été soumis avec succès.'
        success = True
    else:
        alert = 'Des informations obligatoires sont absentes.'
        success = False
    print(alert, file=sys.stderr)
    return make_response(json.dumps([{'msg': alert, 'success': success, 'fields': required}]))


app.secret_key = 'dI\x07\x90\x88a\x91KskQ\x82+\xb5\xad\x943z$\xb3\xe8Y\xebr'

if __name__ == "__main__":
    app.run(debug=True, port=5005)
