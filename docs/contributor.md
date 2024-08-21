# ⚙️ Configuration

Pour que le bot fonctionne correctement, un fichier de configuration est nécessaire. Suivez ces instructions pour le configurer :

## 🗂️ Fichier `config.json`

Le fichier `data/config.json` doit être structuré comme suit :

```json
{
  "forum_channel_id": votre_canal_id,                   // ID du canal pour les offres d'alternance
  "forum_channel_id_cdi": votre_canal_id_cdi,           // ID du canal pour les offres CDI, CDD, Freelance, Intérim
  "role_ping": votre_role_id,                          // ID du rôle pour les notifications d'alternance
  "role_ping_cdi": votre_role_id_cdi,                  // ID du rôle pour les notifications CDI, CDD, Freelance, Intérim
  "guild_id": votre_guild_id,                          // ID de votre serveur Discord
  "role_p1_2023": votre_role_id_p1_2023,               // ID du rôle pour les apprenants P1 2023
  "role_p2_2023": votre_role_id_p2_2023,               // ID du rôle pour les apprenants P2 2023
  "role_p1_2024": votre_role_id_p1_2024,               // ID du rôle pour les apprenants P1 2024
  "role_help": votre_role_id_help                       // ID du rôle pour les demandes d'aide
}
```
## 📝 Explications des Champs
- `forum_channel_id` : L'ID du canal où les offres d'alternance seront publiées.
- `forum_channel_id_cdi` : L'ID du canal où les offres CDI, CDD, Freelance, Intérim seront publiées.
- `role_ping` : L'ID du rôle qui sera mentionné pour les notifications d'alternance.
- `role_ping_cdi` : L'ID du rôle qui sera mentionné pour les notifications CDI, CDD, Freelance, Intérim.
- `guild_id` : L'ID de votre serveur Discord, nécessaire pour que le bot puisse interagir avec le bon serveur.
- `role_p1_2023` : L'ID du rôle pour les apprenants de la promo P1 2023.
- `role_p2_2023` : L'ID du rôle pour les apprenants de la promo P2 2023.
- `role_p1_2024` : L'ID du rôle pour les apprenants de la promo P1 2024.
- `role_help` : L'ID du rôle utilisé pour les demandes d'aide.