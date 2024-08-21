# 📈 Module de Gestion des CDI, CDD, Freelance, Intérim, etc.

Découvrez le module de gestion des offres d'emploi pour le **Bot Discord Zone01** ! Ce module est responsable de la gestion des offres en CDI, CDD, Freelance, Intérim, et autres types de contrats. Il utilise une API générale intégrant plusieurs applications de recrutement telles que LinkedIn, Indeed, HelloWork, etc. pour récupérer les dernières offres et les publier dans un canal spécifique. 🌐

## 🌟 Fonctionnalités

### Commande `!update_cdi`
- **Description :** Force la mise à jour des offres d'emploi en CDI, CDD, Freelance, Intérim, et autres. 📈
- **Utilisation :** Lorsqu'un utilisateur exécute cette commande, un message de chargement est envoyé pour indiquer que la mise à jour est en cours. Le bot récupère les offres d'emploi depuis LinkedIn, Indeed, et autres APIs, puis les publie dans un canal de forum dédié. 📢

### 🔄 Processus de Mise à Jour
1. **Récupération des Offres :** Le bot utilise les fonctions `fetch_api_fulltime` pour obtenir les offres d'emploi. 📊
2. **Création de Threads :** Pour chaque offre valide (titre, entreprise, lien), le bot crée un nouveau thread dans le canal de forum spécifié. Si un thread avec le même titre existe déjà, il passe à l'offre suivante pour éviter les doublons. 📎
3. **Gestion des Erreurs :** Si l'une des APIs échoue, le bot informe l'utilisateur via un message d'erreur approprié. 🚨

### 🔍 Autres Détails
- **Canaux et Rôles :** Le module utilise des identifiants de canal et de rôle définis dans un fichier de configuration, facilitant la gestion des alertes pour les utilisateurs concernés. 🛠️
- **Latence et Débogage :** Des vérifications de latence sont intégrées, et le bot gère les erreurs liées aux appels API et à la création de threads. 🕵️‍♂️

### 🚀 Installation
Pour activer ce module, utilisez la commande `!update_cdi` et suivez les instructions fournies par le bot. 📜

Ce module contribue à rendre l'accès aux offres d'emploi plus accessible pour les apprenants, en centralisant les informations pertinentes dans un seul endroit sur Discord. 🌟
