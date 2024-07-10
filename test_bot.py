import pytest
from unittest.mock import AsyncMock, MagicMock
from bot import send_joblist, update_jobs, ping, bot

# Mock du bot pour éviter l'exécution réelle de bot.run(token)
@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.mark.asyncio
async def test_send_joblist(mock_ctx, mock_channel, mock_bot):
    await send_joblist(mock_ctx, mock_channel)
    # Ajouter des assertions basées sur le comportement de send_joblist

# Autres tests sans dépendance à bot.run(token)
@pytest.mark.asyncio
async def test_update_jobs(mock_ctx, mock_bot):
    await update_jobs(mock_ctx)
    # Ajouter des assertions basées sur le comportement de update_jobs

@pytest.mark.asyncio
async def test_ping(mock_ctx, mock_bot):
    await ping(mock_ctx)
    # Ajouter des assertions basées sur le comportement de ping command
