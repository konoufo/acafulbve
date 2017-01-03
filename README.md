# acafulbve
Envoyer automatiquement les projets d'Acaful au BVE pour demande de financement.

# Instructions pour développement local
## Installation
`pip install -r requirements.txt`
## Utilisation et test
Exécuter `run.py' et 'mockserver.py' dans deux terminaux différents.
`mockserver.py' sert de serveur test (simule le serveur du BVE); il détecte les informations obligatoires non renseignées.
```
   python run.py
```
et
```
   python mockserver.py
```

# Todos
- Transmettre des fichiers au BVE en chargeant les URL Google Drive.
