# Documentation pour le module job_fetcher

## Description

La fonction `fetch_api_intern` est une fonction asynchrone qui récupère des offres de stage pour des postes de Développeur Full Stack Alternant à Rouen, France, via l'API JSearch. Elle filtre les résultats pour ne conserver que les offres de stage publiées aujourd'hui.

## Détails de l'implémentation

- **URL de l'API** : `https://jsearch.p.rapidapi.com/search`
- **Méthode HTTP utilisée** : `GET`
- **Paramètres de la requête** :
  - `query` : "Full Stack Developer Alternant Rouen France"
  - `page` : "1"
  - `num_pages` : "1"
  - `date_posted` : "today"
  - `employment_types` : "INTERN"
  - `radius` : "120"

- **En-têtes de la requête** :
  - `x-rapidapi-key` : Clé d'API récupérée depuis la variable d'environnement `RAPIDAPI_KEY`
  - `x-rapidapi-host` : "jsearch.p.rapidapi.com"

## Fonctionnalité

1. **Envoi de la requête** :
   - La fonction envoie une requête HTTP GET à l'URL de l'API avec les en-têtes et paramètres définis.

2. **Traitement de la réponse** :
   - La fonction vérifie que la réponse est valide et lève une exception en cas d'erreur de requête (`RequestException`).
   - Si la requête est réussie, elle extrait les données JSON de la réponse.
   - Elle retourne la liste des résultats sous la clé `'data'` si les données sont sous forme de liste ; sinon, elle retourne une liste vide.

3. **Gestion des erreurs** :
   - En cas d'échec de la requête, la fonction imprime un message d'erreur et retourne une liste vide.

## Exemples d'utilisation

```python
data = await fetch_api_intern()
print(data)
```

## Gestion des erreurs

- **Exceptions possibles** :
  - `requests.exceptions.RequestException` : Exception générale pour les erreurs de requête HTTP, comme les problèmes de connexion ou les réponses invalides.

## Remarques

- **Variables d'environnement** :
  - Assurez-vous que la variable d'environnement `RAPIDAPI_KEY` est correctement définie et contient une clé API valide pour accéder à l'API JSearch.

- **Environnement asynchrone** :
  - La fonction est conçue pour être utilisée dans un environnement compatible avec `asyncio`, bien que la fonction utilise `requests`, qui est une bibliothèque synchrone. Pour une utilisation entièrement asynchrone, envisagez d'utiliser `aiohttp` à la place de `requests`.

- **Configuration** :
  - Assurez-vous que les paramètres de la requête (comme `query`, `radius`, etc.) sont adaptés aux besoins spécifiques de votre recherche.

