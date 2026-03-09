"""
Serveur web embarqué pour le flux d'authentification OAuth2-like.

Flux :
  1. L'utilisateur lance /connect dans Discord.
  2. Le bot génère un token UUID lié au discord_id et envoie un lien éphémère.
  3. L'utilisateur clique → ce serveur affiche un formulaire web sécurisé.
  4. L'utilisateur soumet ses identifiants Zone01 (dans le navigateur, jamais dans Discord).
  5. Le serveur authentifie contre Zone01, lie les comptes, puis notifie l'utilisateur par DM.
"""
from __future__ import annotations

import asyncio
import base64
import time
import uuid

import aiohttp
import discord
from aiohttp import web

from utils.logger import logger

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ZONE01_DOMAIN = "zone01normandie.org"
ZONE01_API_URL = "https://api-zone01-rouen.deno.dev/api/v1"

TOKEN_TTL = 600  # secondes (10 minutes)

# Stockage en mémoire des tokens en attente : {token: {discord_id, expires_at}}
_pending_tokens: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Gestion des tokens
# ---------------------------------------------------------------------------

def create_connect_token(discord_id: str) -> str:
    """Génère un token one-time et l'associe au discord_id."""
    _cleanup_expired_tokens()
    token = str(uuid.uuid4())
    _pending_tokens[token] = {
        "discord_id": discord_id,
        "expires_at": time.time() + TOKEN_TTL,
    }
    return token


def _cleanup_expired_tokens() -> None:
    now = time.time()
    expired = [k for k, v in _pending_tokens.items() if v["expires_at"] < now]
    for k in expired:
        del _pending_tokens[k]


def _consume_token(token: str) -> dict | None:
    """Valide et consomme un token (one-time use). Retourne les données ou None."""
    _cleanup_expired_tokens()
    data = _pending_tokens.get(token)
    if not data:
        return None
    if data["expires_at"] < time.time():
        del _pending_tokens[token]
        return None
    del _pending_tokens[token]
    return data


# ---------------------------------------------------------------------------
# HTML Templates
# ---------------------------------------------------------------------------

_BASE_CSS = """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #0d1117;
        color: #e6edf3;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 1rem;
    }
    .card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 8px 32px rgba(0,0,0,.4);
    }
    .logo {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin-bottom: 1.5rem;
    }
    .logo-icon {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #00b4d8, #0077b6);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
    }
    .logo-text { font-size: 1.25rem; font-weight: 700; color: #fff; }
    .logo-sub { font-size: .8rem; color: #8b949e; }
    h2 { font-size: 1.1rem; font-weight: 600; margin-bottom: .4rem; color: #fff; }
    .subtitle { font-size: .85rem; color: #8b949e; margin-bottom: 1.5rem; line-height: 1.5; }
    label { display: block; font-size: .8rem; font-weight: 500; color: #8b949e; margin-bottom: .35rem; }
    input {
        width: 100%;
        padding: .65rem .9rem;
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        color: #e6edf3;
        font-size: .9rem;
        margin-bottom: 1rem;
        outline: none;
        transition: border-color .15s;
    }
    input:focus { border-color: #00b4d8; }
    button {
        width: 100%;
        padding: .7rem;
        background: linear-gradient(135deg, #00b4d8, #0077b6);
        border: none;
        border-radius: 8px;
        color: #fff;
        font-size: .95rem;
        font-weight: 600;
        cursor: pointer;
        transition: opacity .15s;
    }
    button:hover { opacity: .88; }
    .alert {
        background: #2d1b1b;
        border: 1px solid #6e2727;
        border-radius: 8px;
        padding: .75rem 1rem;
        font-size: .85rem;
        color: #f87171;
        margin-bottom: 1.2rem;
    }
    .notice {
        font-size: .75rem;
        color: #6e7681;
        text-align: center;
        margin-top: 1.2rem;
        line-height: 1.5;
    }
    .success-icon { font-size: 3rem; text-align: center; margin-bottom: 1rem; }
    .success-title { font-size: 1.3rem; font-weight: 700; color: #4ade80; text-align: center; margin-bottom: .5rem; }
    .success-sub { font-size: .9rem; color: #8b949e; text-align: center; line-height: 1.6; }
    .timer { font-size: .75rem; color: #6e7681; text-align: center; margin-top: 1.5rem; }
"""


def _render_form(token: str, error: str = "") -> str:
    error_html = f'<div class="alert">{error}</div>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Connexion Zone01 — Lier mon compte Discord</title>
  <style>{_BASE_CSS}</style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <div class="logo-icon">🎓</div>
      <div>
        <div class="logo-text">Zone01</div>
        <div class="logo-sub">Liaison de compte Discord</div>
      </div>
    </div>
    <h2>Connectez-vous à Zone01</h2>
    <p class="subtitle">
      Entrez vos identifiants Zone01 pour lier votre compte Discord.
      Vos identifiants transitent directement vers Zone01 et ne sont jamais stockés.
    </p>
    {error_html}
    <form method="POST" action="/connect">
      <input type="hidden" name="token" value="{token}">
      <label for="login">Login Zone01</label>
      <input type="text" id="login" name="login" placeholder="prenom.nom" autocomplete="username" required>
      <label for="password">Mot de passe</label>
      <input type="password" id="password" name="password" placeholder="••••••••" autocomplete="current-password" required>
      <button type="submit">🔗 Lier mon compte</button>
    </form>
    <p class="notice">
      Ce lien est à usage unique et expire dans 10 minutes.<br>
      Si le lien a expiré, relancez <strong>/connect</strong> dans Discord.
    </p>
  </div>
</body>
</html>"""


_SUCCESS_PAGE = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Compte lié — Zone01</title>
  <style>{_BASE_CSS}</style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <div class="logo-icon">🎓</div>
      <div>
        <div class="logo-text">Zone01</div>
        <div class="logo-sub">Liaison de compte Discord</div>
      </div>
    </div>
    <div class="success-icon">✅</div>
    <div class="success-title">Compte lié avec succès !</div>
    <p class="success-sub">
      Votre compte Discord est maintenant lié à votre compte Zone01.<br>
      Un message de confirmation vous a été envoyé par le bot sur Discord.
    </p>
    <p class="timer">Vous pouvez fermer cette page.</p>
  </div>
</body>
</html>"""

_EXPIRED_PAGE = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lien expiré — Zone01</title>
  <style>{_BASE_CSS}</style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <div class="logo-icon">🎓</div>
      <div>
        <div class="logo-text">Zone01</div>
        <div class="logo-sub">Liaison de compte Discord</div>
      </div>
    </div>
    <div class="success-icon">⏱️</div>
    <div class="success-title" style="color:#f87171">Lien invalide ou expiré</div>
    <p class="success-sub">
      Ce lien est à usage unique et a expiré ou a déjà été utilisé.<br>
      Relancez <strong>/connect</strong> dans Discord pour obtenir un nouveau lien.
    </p>
  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Handlers HTTP
# ---------------------------------------------------------------------------

async def _handle_get(request: web.Request) -> web.Response:
    """Affiche le formulaire de connexion si le token est valide."""
    token = request.rel_url.query.get("token", "")
    _cleanup_expired_tokens()

    if not token or token not in _pending_tokens:
        return web.Response(text=_EXPIRED_PAGE, content_type="text/html", status=400)

    return web.Response(text=_render_form(token), content_type="text/html")


async def _handle_post(request: web.Request, bot: discord.Client) -> web.Response:
    """Traite la soumission du formulaire."""
    data = await request.post()
    token = data.get("token", "")
    login = data.get("login", "").strip()
    password = data.get("password", "")

    if not login or not password:
        _cleanup_expired_tokens()
        if token not in _pending_tokens:
            return web.Response(text=_EXPIRED_PAGE, content_type="text/html", status=400)
        return web.Response(
            text=_render_form(token, "Veuillez remplir tous les champs."),
            content_type="text/html",
        )

    token_data = _consume_token(token)
    if not token_data:
        return web.Response(text=_EXPIRED_PAGE, content_type="text/html", status=400)

    discord_id = token_data["discord_id"]

    # --- Étape 1 : Authentification Zone01 ---
    credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://{ZONE01_DOMAIN}/api/auth/signin",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {credentials}",
                },
                timeout=aiohttp.ClientTimeout(total=10),
            ) as auth_resp:
                if not auth_resp.ok:
                    logger.warning(
                        f"Échec d'auth Zone01 — login: {login} (HTTP {auth_resp.status})",
                        category="connect",
                    )
                    # Remettre un token frais pour que l'utilisateur puisse réessayer
                    new_token = str(uuid.uuid4())
                    _pending_tokens[new_token] = {
                        "discord_id": discord_id,
                        "expires_at": time.time() + TOKEN_TTL,
                    }
                    return web.Response(
                        text=_render_form(new_token, "Login ou mot de passe incorrect."),
                        content_type="text/html",
                    )

            # --- Étape 2 : Liaison Discord ↔ Zone01 ---
            async with session.put(
                f"{ZONE01_API_URL}/discord-users",
                json={"login": login, "discord_id": discord_id},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as api_resp:
                if not api_resp.ok:
                    logger.error(
                        f"Erreur API liaison — login: {login} (HTTP {api_resp.status})",
                        category="connect",
                    )
                    return web.Response(
                        text="<p>Erreur lors de l'enregistrement. Réessayez plus tard.</p>",
                        content_type="text/html",
                        status=500,
                    )

    except asyncio.TimeoutError:
        logger.error("Timeout lors de l'authentification Zone01", category="connect")
        return web.Response(
            text="<p>Le serveur Zone01 ne répond pas. Réessayez plus tard.</p>",
            content_type="text/html",
            status=503,
        )
    except aiohttp.ClientError as e:
        logger.error(f"Erreur réseau : {e}", category="connect")
        return web.Response(
            text="<p>Erreur réseau. Réessayez plus tard.</p>",
            content_type="text/html",
            status=503,
        )

    # --- Succès : notifier l'utilisateur par DM ---
    logger.success(
        f"Liaison réussie : Zone01={login} ↔ Discord ID={discord_id}",
        category="connect",
    )
    asyncio.create_task(_notify_discord(bot, int(discord_id), login))

    return web.Response(text=_SUCCESS_PAGE, content_type="text/html")


async def _notify_discord(bot: discord.Client, discord_id: int, login: str) -> None:
    """Envoie un DM de confirmation à l'utilisateur Discord."""
    try:
        user = await bot.fetch_user(discord_id)
        embed = discord.Embed(
            title="✅ Compte lié avec succès !",
            description=f"Votre compte Discord est maintenant lié à votre compte Zone01 **{login}**.",
            color=discord.Color.green(),
        )
        embed.set_footer(text="Relancez /connect à tout moment pour mettre à jour la liaison.")
        await user.send(embed=embed)
    except discord.Forbidden:
        logger.warning(f"Impossible d'envoyer un DM à l'utilisateur {discord_id}", category="connect")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du DM de confirmation : {e}", category="connect")


# ---------------------------------------------------------------------------
# Démarrage du serveur
# ---------------------------------------------------------------------------

async def start_web_server(bot: discord.Client, host: str = "0.0.0.0", port: int = 8080) -> None:
    """Lance le serveur web aiohttp en parallèle du bot."""

    async def post_handler(request: web.Request) -> web.Response:
        return await _handle_post(request, bot)

    app = web.Application()
    app.router.add_get("/connect", _handle_get)
    app.router.add_post("/connect", post_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    logger.success(f"Serveur web démarré sur http://{host}:{port}", category="connect")
