import json
import os
from datetime import datetime
from collections import deque

# Fichier pour stocker les logs
LOGS_FILE = "data/bot_logs.json"
MAX_LOGS_IN_MEMORY = 500  # Nombre maximum de logs en mémoire

class BotLogger:
    """Logger centralisé pour le bot Discord"""

    def __init__(self):
        self.logs = deque(maxlen=MAX_LOGS_IN_MEMORY)
        self.load_logs()

    def load_logs(self):
        """Charge les logs depuis le fichier"""
        if os.path.exists(LOGS_FILE):
            try:
                with open(LOGS_FILE, 'r') as f:
                    data = json.load(f)
                    # Charger seulement les derniers logs
                    self.logs = deque(data[-MAX_LOGS_IN_MEMORY:], maxlen=MAX_LOGS_IN_MEMORY)
            except:
                self.logs = deque(maxlen=MAX_LOGS_IN_MEMORY)

    def save_logs(self):
        """Sauvegarde les logs dans le fichier"""
        try:
            os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)
            with open(LOGS_FILE, 'w') as f:
                json.dump(list(self.logs), f, indent=2)
        except Exception as e:
            # En cas d'erreur, ne pas crasher le bot
            pass

    def _log(self, level, message, category="general"):
        """Méthode interne pour logger un message"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "category": category,
            "message": str(message)
        }

        self.logs.append(log_entry)
        self.save_logs()

    def info(self, message, category="general"):
        """Log un message d'information"""
        self._log("INFO", message, category)

    def success(self, message, category="general"):
        """Log un message de succès"""
        self._log("SUCCESS", message, category)

    def warning(self, message, category="general"):
        """Log un avertissement"""
        self._log("WARNING", message, category)

    def error(self, message, category="general"):
        """Log une erreur"""
        self._log("ERROR", message, category)

    def debug(self, message, category="general"):
        """Log un message de debug"""
        self._log("DEBUG", message, category)

    def get_logs(self, limit=100, level=None, category=None):
        """Récupère les logs avec filtres optionnels"""
        logs_list = list(self.logs)

        # Filtrer par niveau si spécifié
        if level:
            logs_list = [log for log in logs_list if log['level'] == level]

        # Filtrer par catégorie si spécifié
        if category:
            logs_list = [log for log in logs_list if log['category'] == category]

        # Retourner les derniers logs (les plus récents en premier)
        return logs_list[-limit:][::-1]

    def clear_logs(self):
        """Efface tous les logs"""
        self.logs.clear()
        self.save_logs()

    def get_stats(self):
        """Retourne des statistiques sur les logs"""
        logs_list = list(self.logs)

        stats = {
            "total": len(logs_list),
            "info": len([log for log in logs_list if log['level'] == 'INFO']),
            "success": len([log for log in logs_list if log['level'] == 'SUCCESS']),
            "warning": len([log for log in logs_list if log['level'] == 'WARNING']),
            "error": len([log for log in logs_list if log['level'] == 'ERROR']),
            "debug": len([log for log in logs_list if log['level'] == 'DEBUG']),
        }

        return stats

# Instance globale du logger
logger = BotLogger()
