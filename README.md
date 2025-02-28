```````````` # README.md - Projet Chatbot ISO 27001 # ````````````

Nous sommes **Manal Kassaoui** et **Douaa El Korti**, et voici notre projet : un **chatbot sur la norme ISO 27001:2022**. On a travaillé ensemble pour créer un outil qui aide les gens à mieux comprendre cette norme de sécurité de l’information. Ce fichier est notre "README", un guide simple pour expliquer ce qu’on a fait et comment utiliser notre projet.

## C’est quoi ce projet ?

Notre projet est un **chatbot intelligent** qui répond à des questions sur la norme **ISO 27001:2022**, une norme internationale pour sécuriser les systèmes d’information. Il peut :
- Répondre à des questions simples (ex. : "Qu’est-ce que ISO 27001 ?").
- Vérifier si une organisation respecte des règles précises, comme la politique de sécurité (A.5.1), avec des questions interactives.
- Donner des conseils pratiques pour être conforme.

On a utilisé **Python** comme langage principal, **Flask** pour l’interface web, **MongoDB** pour stocker les conversations, et des bibliothèques comme **SpaCy** et **TF-IDF** pour rendre le chatbot malin dans ses réponses.

## Pourquoi on a fait ça ?

On voulait :
- Créer un outil utile pour les entreprises ou les étudiants qui découvrent ISO 27001.
- Montrer nos compétences en programmation, en gestion de bases de données, et en travail d’équipe.
- Apprendre nous-mêmes les détails de cette norme importante.

## Comment ça marche ?

Le chatbot s’appuie sur une **base de connaissances** (un fichier JSON appelé `iso27001.json`) avec toutes les infos sur ISO 27001 : clauses, contrôles, bonnes pratiques, etc. Voici comment il fonctionne :
- On pose une question (ex. : "Comment maintenir la certification ISO 27001 ?").
- Il analyse la question avec SpaCy et TF-IDF, puis trouve la meilleure réponse dans ses données.
- Si on demande "Mon SI est-il conforme ?", il pose des questions comme "Avez-vous une politique de sécurité ?" et donne des actions correctives si besoin.
- Toutes les conversations sont enregistrées dans une base **MongoDB** pour suivre ce qu’on lui dit.

## Les fichiers importants

Voici les fichiers clés de notre projet et leur rôle :
- **`chatbot.py`** : Le cœur du chatbot, où on a codé comment il comprend les questions et répond.
- **`conversational_handler.py`** : Gère les discussions interactives, comme les vérifications de conformité.
- **`app.py`** : Lance l’application web avec Flask pour utiliser le chatbot dans un navigateur.
- **`db.py`** : Contient la fonction pour se connecter à MongoDB et gérer la base de données.
- **`data/iso27001.json`** : Notre base de connaissances avec toutes les infos sur ISO 27001.
- **`templates/index.html`** : Une page web simple pour taper les questions et voir les réponses.
- **`static/`** : Contient les fichiers CSS, JavaScript et images pour améliorer l’interface.

chatbot_iso27001/
├── app.py                # Application Flask pour lancer le chatbot
├── chatbot.py            # Logique principale du chatbot
├── conversational_handler.py  # Gestionnaire des conversations
├── data/
│   ├── iso27001.json     # Base de connaissances pour ISO 27001
├── logs/
│   └── chatbot_logs.json # Fichier JSON vide ou généré dynamiquement
├── database/
│   ├── db.py             # Connexion à MongoDB
├── requirements.txt      # Dépendances Python
├── templates/
│   ├── index.html        # Modèle frontal pour l’interface
├── static/
│   ├── css/
│   │   └── style.css     # CSS de base pour styliser l’interface du chatbot
│   ├── js/
│   │   └── main.js       # JavaScript pour gérer les interactions du chat
│   └── images/
│       └── logo.png      # Image placeholder pour le logo
└── README.md             # Documentation du projet

## Comment l’installer et l’utiliser ?

1. Préparer l’environnement :
- Installez **Python** (version 3.8 ou plus).
- Installez **MongoDB** et assurez-vous qu’il fonctionne sur `localhost:27017`.

2. Lancer le chatbot :
Allez dans le dossier du projet avec le terminal.
Tapez : python app.py
Ouvrez un navigateur et allez à http://localhost:5000.

3. Parler au chatbot :
- Sur la page web, tape ta question et clique sur "Envoyer".
- Le chatbot répondra tout de suite !

## Exemples de questions à poser

- "Qu’est-ce que ISO 27001 ?"
- "Comment obtenir la certification ISO 27001 ?"
- "Mon système d’information est-il conforme à ISO 27001 ?"
- "Combien coûte la certification ?"

## Ce qu’on a appris

En faisant ce projet, on a découvert :
- Comment coder un chatbot avec Python et le rendre intelligent.
- Comment connecter une base de données MongoDB et stocker des données.
- Les détails de la norme ISO 27001 (clauses, Annexe A, etc.).
- L’importance de travailler en équipe et d’organiser notre code.

## Problèmes qu’on a eus

- Au début, on n’a pas trouvé assez de données sur ISO 27001 pour travailler, alors on a dû chercher et construire notre base de connaissances nous-mêmes.
- Le chatbot ne comprenait pas bien certaines questions, mais on a amélioré ça avec SpaCy et TF-IDF.
- Configurer MongoDB était un peu dur, surtout pour le faire marcher correctement.

## Merci !

Merci d’avoir lu notre README ! 

**Manal Kassaoui & Douaa El Korti**  