Neural Network Project
Description
Ce projet utilise une interface de menu en curses pour gérer des plugins de traitement neuronal et de débogage. Le projet comprend des plugins qui effectuent diverses tâches et un serveur web pour le débogage et le contrôle en temps réel.

Installation
Prérequis
Python 3.11
Flask
Étapes d'installation
Mettre à jour et installer les dépendances:

sh
Copier le code
sudo apt update
sudo apt install python3 python3-venv python3-pip
Cloner le projet ou copier les fichiers dans le répertoire de travail.

Créer un environnement virtuel et installer les paquets nécessaires:

sh
Copier le code
cd /path/to/your/project
python3 -m venv neural_network_project_env
source neural_network_project_env/bin/activate
pip install -r requirements.txt
Lancer le projet:

sh
Copier le code
source neural_network_project_env/bin/activate
python3 main2.py
Structure du projet
arduino
Copier le code
neural_network_project/
├── config.json
├── data/
├── logs/
├── main2.py
├── menu2.py
├── plugins/
│   ├── debug_plugin.py
│   ├── neural_network_plugin.py
│   └── plugin_gateway.py
├── requirements.txt
├── temp_data/
│   └── menu.lst
└── templates/
    ├── control_panel.html
    ├── edit_file.html
    └── view_logs.html
Configuration
config.json
Le fichier config.json contient la configuration du projet et est généré automatiquement s'il n'existe pas. Il comprend des paramètres comme le niveau de verbosité des logs, les répertoires requis et le répertoire des plugins.

Exemple de config.json :
json
Copier le code
{
    "verbosity": "INFO",
    "required_directories": [
        "./logs",
        "./data",
        "./temp_data"
    ],
    "plugins_directory": "./plugins"
}
Fichiers et leur But
main2.py
Le fichier main2.py est le point d'entrée principal du projet. Il initialise les répertoires nécessaires, configure les logs, charge les plugins, génère le fichier menu.lst et lance le serveur web de débogage ainsi que le menu curses.

menu2.py
Ce fichier contient la classe Menu qui gère l'affichage et la navigation dans les menus curses. Il charge les éléments du menu depuis menu.lst et exécute les actions associées aux plugins.

plugins/
Ce répertoire contient les différents plugins du projet.

debug_plugin.py
Ce plugin fournit une interface web pour la visualisation et la modification des fichiers du projet ainsi que pour le contrôle des logs. Il fonctionne sur un serveur Flask et est accessible via http://0.0.0.0:5000/control.

neural_network_plugin.py
Ce plugin gère l'entraînement d'un modèle de réseau neuronal. Il lit la configuration depuis config.json et exécute l'entraînement du modèle en arrière-plan.

plugin_gateway.py
Le PluginGateway est responsable du chargement et de l'exécution des plugins en arrière-plan. Il assure la communication et le transfert de données entre les plugins.

requirements.txt
Ce fichier liste les dépendances Python nécessaires au projet, telles que Flask et Jinja2.

templates/
Ce répertoire contient les templates HTML utilisés par le debug_plugin.py pour le serveur web.

control_panel.html
Template pour le panneau de contrôle principal du plugin de débogage.

edit_file.html
Template pour l'édition de fichiers du projet via l'interface web.

view_logs.html
Template pour la visualisation des logs en temps réel via l'interface web.

Utilisation
Lancement du projet
Activer l'environnement virtuel:

sh
Copier le code
source neural_network_project_env/bin/activate
Démarrer le projet:

sh
Copier le code
python3 main2.py
Navigation dans le menu
Utilisez les touches fléchées pour naviguer dans le menu. Appuyez sur Entrée pour sélectionner une option. Les options de retour et de quitter sont disponibles dans chaque sous-menu.

Interface Web de Débogage
Accédez à l'interface web de débogage via http://0.0.0.0:5000/control pour visualiser et modifier les fichiers du projet, consulter les logs en temps réel, redémarrer ou arrêter le projet.