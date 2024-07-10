import unittest
from unittest.mock import patch, MagicMock
from bot import send_joblist, update_jobs, ping, bot  # Assurez-vous d'importer correctement les éléments nécessaires

class TestBotFunctions(unittest.TestCase):

    @patch('bot.send_joblist')
    def test_update_jobs_command(self, mock_send_joblist):
        # Créer un mock pour le contexte (ctx) simulé
        mock_ctx = MagicMock()

        # Appeler la commande update_jobs
        update_jobs(mock_ctx)

        # Vérifier que send_joblist a été appelé avec le contexte simulé
        mock_send_joblist.assert_called_once_with(mock_ctx)

    def test_ping_command(self):
        # Créer un mock pour le contexte (ctx) simulé
        mock_ctx = MagicMock()

        # Appeler la commande ping
        self.assertIsNone(ping(mock_ctx))  # Exemple basique pour tester la fonctionnalité du ping

if __name__ == '__main__':
    unittest.main()
