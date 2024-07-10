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

    @patch('discord.ext.commands.Bot.run')
    def test_bot_run(self, mock_bot_run):
        # Appeler la méthode run du bot
        bot.run('mock_token')

        # Vérifier que la méthode run a été appelée avec le token
        mock_bot_run.assert_called_once_with('mock_token')

    def test_ping_command(self):
        # Créer un mock pour le contexte (ctx) simulé
        mock_ctx = MagicMock()

        # Appeler la commande ping
        self.assertIsNone(ping(mock_ctx))  # Exemple basique pour tester la fonctionnalité du ping

if __name__ == '__main__':
    unittest.main()

