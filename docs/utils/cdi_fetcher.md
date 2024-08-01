# Documentation pour le module cdi_fetcher

## Description

La fonction `fetch_api_fulltime` est une fonction asynchrone qui récupère des offres d'emploi pour des postes de Développeur Full Stack à Rouen, France, via l'API JSearch. Elle filtre les résultats pour ne conserver que les offres de travail à temps plein publiées aujourd'hui.

## Détails de l'implémentation

- **URL de l'API** : `https://jsearch.p.rapidapi.com/search`
- **Méthode HTTP utilisée** : `GET`
- **Paramètres de la requête** :
  - `query` : "Full Stack Developer Rouen France"
  - `page` : "1"
  - `num_pages` : "1"
  - `date_posted` : "today"
  - `employment_types` : "FULLTIME"
  - `radius` : "120"

- **En-têtes de la requête** :
  - `x-rapidapi-key` : Clé d'API récupérée depuis la variable d'environnement `RAPIDAPI_KEY`
  - `x-rapidapi-host` : "jsearch.p.rapidapi.com"

## Fonctionnalité

1. La fonction envoie une requête HTTP GET à l'URL de l'API avec les en-têtes et paramètres définis.
2. Elle vérifie que la réponse est valide et lève une exception en cas d'erreur de requête (`RequestException`).
3. Si la requête est réussie, elle extrait les données JSON et retourne la liste des résultats sous la clé `'data'`. Si les données ne sont pas sous forme de liste, elle retourne une liste vide.
4. En cas d'erreur lors de la récupération des données, la fonction imprime un message d'erreur et retourne une liste vide.

## Exemples d'utilisation

```python
data = await fetch_api_fulltime()
print(data)
```

## Gestion des erreurs

- En cas d'échec de la requête (par exemple, problème de connexion ou réponse invalide), un message d'erreur est affiché dans la console, et la fonction retourne une liste vide.

## Remarques

- Assurez-vous que la variable d'environnement `RAPIDAPI_KEY` est correctement définie et contient une clé API valide pour accéder à l'API JSearch.
- La fonction est conçue pour être utilisée dans un environnement asynchrone compatible avec `asyncio`, bien que la fonction elle-même utilise `requests`, qui est une bibliothèque synchrone. Pour une utilisation entièrement asynchrone, envisagez d'utiliser `aiohttp` à la place de `requests`.

