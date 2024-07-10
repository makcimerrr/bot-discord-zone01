import unittest
from unittest.mock import patch, MagicMock
import os
from bot import send_joblist, update_jobs, ping  # Assurez-vous d'importer correctement les éléments nécessaires

class TestBotFunctions(unittest.TestCase):

    @patch('bot.send_joblist')
    def test_update_jobs_command(self, mock_send_joblist):
        # Récupérer le token depuis les variables d'environnement
        token = os.getenv('TOKEN')

        # Vérifier que le token est bien défini
        self.assertIsNotNone(token, "Le token n'est pas défini dans les variables d'environnement")

        # Créer un mock pour le contexte (ctx) simulé
        mock_ctx = MagicMock()

        # Appeler la commande update_jobs avec le token
        update_jobs(mock_ctx, token)

        # Vérifier que send_joblist a été appelé avec le contexte simulé
        mock_send_joblist.assert_called_once_with(mock_ctx)

    def test_ping_command(self):
        # Récupérer le token depuis les variables d'environnement
        token = os.getenv('TOKEN')

        # Vérifier que le token est bien défini
        self.assertIsNotNone(token, "Le token n'est pas défini dans les variables d'environnement")

        # Créer un mock pour le contexte (ctx) simulé
        mock_ctx = MagicMock()

        # Appeler la commande ping avec le token
        self.assertIsNone(ping(mock_ctx, token))  # Exemple basique pour tester la fonctionnalité du ping

if __name__ == '__main__':
    unittest.main()
