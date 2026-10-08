# TP : API de réservation de salles

> **À compléter par votre groupe avant le dernier push.**

## Groupe

| Membre | Compte GitHub | Rôle / tâches principales |
|--------|---------------|---------------------------|
|MESSOU grace|Grace-amanda237 | Conception et développement de l'API |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Comptes de test (mot de passe : `motdepasse123`) : `alice`, `bob`, `charlie`.
Super-utilisateur : `admin` / `admin123`.

## Endpoints

> À compléter : listez les routes de votre API, les méthodes autorisées et qui a le droit de les appeler.

| Route | Méthodes | Permissions |
|-------|----------|-------------|
| /api/salles/ |GET|Tout le monde |
| /api/salles/ | POST| Utilisateur staff |
| /api/salles/{id}/| GET  | Tout le monde |
| /api/salles/{id}/ | PUT, PATCH, DELETE | Utilisateur staff |
| /api/salles/{id}/occupation/ | GET | Tout le monde|

| /api/reservation/ |GET|Tout le monde |
| /api/reservation/ | POST| Utilisateur staff |
| /api/reservation/{id}/| GET  | Tout le monde |
| /api/reservation/{id}/ | PUT, PATCH, DELETE | Utilisateur staff |


## Choix de conception et difficultés rencontrées

> Quelques lignes : comment avez-vous défini le chevauchement ? Qu'est-ce qui vous a posé problème ?

Pour gérer les réservations, j’ai fait la vérification des chevauchements directement dans le serializer. Cela me permet de vérifier automatiquement que les dates sont correctes aussi bien lorsqu’on crée une réservation que lorsqu’on la modifie.
J’ai aussi fait en sorte que deux réservations puissent se suivre directement sans être considérées comme un chevauchement. Par exemple, si une réservation se termine à 10h00, une autre peut commencer à 10h00.

La gestion des modifications avec PATCH m’a également posé quelques difficultés. Comme toutes les informations ne sont pas forcément envoyées lors d’une modification, il fallait utiliser les anciennes valeurs de la réservation pour pouvoir refaire correctement les vérifications.
aussi, j’ai dû mettre en place les permissions pour que chaque utilisateur puisse uniquement modifier ou supprimer ses propres réservations. Pour les salles, seules les personnes ayant les droits nécessaires peuvent les créer, les modifier ou les supprimer.
