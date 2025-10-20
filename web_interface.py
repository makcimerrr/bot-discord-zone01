from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import logger

app = Flask(__name__)

# Charger les variables d'environnement
env_path = Path('.env')
load_dotenv(dotenv_path=env_path, override=True)

# Configuration
CONFIG_FILE = "data/config.json"
HELP_REQUESTS_FILE = "data/help_requests.json"

def load_json_file(file_path):
    """Charge un fichier JSON"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def get_bot_commands():
    """Retourne la liste de toutes les commandes du bot"""
    commands = {
        "Administration": [
            {
                "name": "setqueryIntern",
                "description": "Définit la query de recherche pour les alternances/stages",
                "usage": "!setqueryIntern <query>",
                "aliases": [],
                "admin_only": True
            },
            {
                "name": "setqueryFulltime",
                "description": "Définit la query de recherche pour les emplois à temps plein (CDI)",
                "usage": "!setqueryFulltime <query>",
                "aliases": [],
                "admin_only": True
            },
            {
                "name": "update_internships",
                "description": "Force la mise à jour des offres d'emploi pour les alternances",
                "usage": "!update_internships",
                "aliases": ["update_jobs"],
                "admin_only": True
            },
            {
                "name": "update_fulltime",
                "description": "Force la mise à jour des offres d'emploi pour les CDI",
                "usage": "!update_fulltime",
                "aliases": ["update_cdi"],
                "admin_only": True
            },
            {
                "name": "timeline",
                "description": "Affiche la timeline des promotions",
                "usage": "!timeline",
                "aliases": ["tl"],
                "admin_only": True
            }
        ],
        "Configuration": [
            {
                "name": "showqueryIntern",
                "description": "Affiche la query actuelle pour les alternances/stages",
                "usage": "!showqueryIntern",
                "aliases": [],
                "admin_only": True
            },
            {
                "name": "showqueryFulltime",
                "description": "Affiche la query actuelle pour les emplois à temps plein",
                "usage": "!showqueryFulltime",
                "aliases": [],
                "admin_only": True
            }
        ],
        "Utilitaire": [
            {
                "name": "ping",
                "description": "Renvoie la latence du bot en millisecondes",
                "usage": "!ping",
                "aliases": ["pingme", "pingpong", "pingtest", "latence", "latency"],
                "admin_only": False
            },
            {
                "name": "help",
                "description": "Affiche la liste des commandes disponibles",
                "usage": "!help [commande]",
                "aliases": ["helpme"],
                "admin_only": False
            }
        ],
        "Événements": [
            {
                "name": "/create_event",
                "description": "Crée un événement avec inscription pour les participants",
                "usage": "/create_event",
                "aliases": [],
                "admin_only": True
            }
        ],
        "Système d'Aide": [
            {
                "name": "/send_help_embed",
                "description": "Envoie un embed d'aide avec bouton dans le canal spécifié",
                "usage": "/send_help_embed <channel>",
                "aliases": [],
                "admin_only": True
            },
            {
                "name": "/setup_reaction_help",
                "description": "Configure le message de demande d'aide par réaction",
                "usage": "/setup_reaction_help <channel>",
                "aliases": [],
                "admin_only": True
            }
        ]
    }
    return commands

@app.route('/')
def index():
    """Page d'accueil"""
    config = load_json_file(CONFIG_FILE)
    help_requests = load_json_file(HELP_REQUESTS_FILE)

    # Statistiques
    stats = {
        "total_help_requests": len(help_requests),
        "active_requests": len([r for r in help_requests.values() if 'current_helper' in r]),
        "query_intern": os.getenv('QUERY_INTERNSHIP', 'Non définie'),
        "query_fulltime": os.getenv('QUERY_FULLTIME', 'Non définie'),
    }

    return render_template('index.html', stats=stats, config=config)

@app.route('/commands')
def commands():
    """Page des commandes"""
    bot_commands = get_bot_commands()
    return render_template('commands.html', commands=bot_commands)

@app.route('/help-system')
def help_system():
    """Page du système d'aide"""
    help_requests = load_json_file(HELP_REQUESTS_FILE)

    # Formater les données pour l'affichage
    formatted_requests = []
    for req_id, req_data in help_requests.items():
        formatted_requests.append({
            'id': req_id,
            'user_id': req_data.get('user_id', 'N/A'),
            'guild_id': req_data.get('guild_id', 'N/A'),
            'current_helper': req_data.get('current_helper', 'Aucun'),
            'contacted_helpers_count': len(req_data.get('contacted_helpers', [])),
            'contacted_helpers': req_data.get('contacted_helpers', [])
        })

    return render_template('help_system.html', requests=formatted_requests)

@app.route('/config')
def configuration():
    """Page de configuration"""
    config = load_json_file(CONFIG_FILE)

    # Variables d'environnement
    env_vars = {
        'QUERY_INTERNSHIP': os.getenv('QUERY_INTERNSHIP', 'Non définie'),
        'QUERY_FULLTIME': os.getenv('QUERY_FULLTIME', 'Non définie'),
        'DISCORD_TOKEN': '****** (masqué pour sécurité)' if os.getenv('DISCORD_TOKEN') else 'Non défini'
    }

    return render_template('config.html', config=config, env_vars=env_vars)

@app.route('/api/stats')
def api_stats():
    """API pour récupérer les statistiques en temps réel"""
    help_requests = load_json_file(HELP_REQUESTS_FILE)

    stats = {
        "total_help_requests": len(help_requests),
        "active_requests": len([r for r in help_requests.values() if 'current_helper' in r]),
        "timestamp": datetime.now().isoformat()
    }

    return jsonify(stats)

@app.route('/api/help-requests')
def api_help_requests():
    """API pour récupérer les demandes d'aide en temps réel"""
    help_requests = load_json_file(HELP_REQUESTS_FILE)
    return jsonify(help_requests)

@app.template_filter('format_timestamp')
def format_timestamp(timestamp):
    """Filtre pour formater les timestamps"""
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return 'N/A'

@app.template_filter('format_log_timestamp')
def format_log_timestamp(timestamp_str):
    """Filtre pour formater les timestamps des logs"""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return timestamp_str

@app.route('/logs')
def logs():
    """Page des logs"""
    # Récupérer les paramètres de filtre
    level = request.args.get('level', None)
    category = request.args.get('category', None)
    limit = int(request.args.get('limit', 100))

    # Récupérer les logs avec filtres
    logs_list = logger.get_logs(limit=limit, level=level, category=category)

    # Récupérer les statistiques
    stats = logger.get_stats()

    return render_template('logs.html', logs=logs_list, stats=stats)

@app.route('/api/logs')
def api_logs():
    """API pour récupérer les logs"""
    level = request.args.get('level', None)
    category = request.args.get('category', None)
    limit = int(request.args.get('limit', 100))

    logs_list = logger.get_logs(limit=limit, level=level, category=category)
    return jsonify(logs_list)

@app.route('/api/logs/stats')
def api_logs_stats():
    """API pour récupérer les statistiques des logs"""
    stats = logger.get_stats()
    return jsonify(stats)

@app.route('/api/logs/clear', methods=['POST'])
def api_logs_clear():
    """API pour effacer tous les logs"""
    try:
        logger.clear_logs()
        return jsonify({"success": True, "message": "Logs effacés"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    # Créer les dossiers nécessaires s'ils n'existent pas
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # Log du démarrage de l'interface web
    logger.success("Interface web démarrée sur http://localhost:5001", category="web")

    # Désactiver les logs Flask dans le terminal
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
