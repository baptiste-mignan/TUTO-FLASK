 # Projet Flask - Gestion de Bibliothèque
 ## Présentation

Ce projet a été réalisé dans le cadre d'un travail en groupe de deux, en complément des travaux pratiques sur Flask. L'application permet de gérer une collection de livres avec des fonctionnalités telles que l'authentification, l'ajout et la gestion des auteurs et des livres, ainsi que la gestion des favoris. Le projet étant la continuité du projet fait en cours, c'est la suite du projet d'abord commencer par Baptiste Mignan qui a été choisis pour continuer.

Vous retrouverez le projet sur ce dépôt distant

https://github.com/baptiste-mignan/TUTO-FLASK/graphs/contributors

 ## Composition du Groupe

- #### Baptiste Mignan
- #### Pierre Gangneux

 ## Fonctionnalités Implémentées
 ### Fonctionnalités de base

- Affichage de la liste des livres avec détails au clic.
- Intégration de Bootstrap pour un design amélioré.
- Gestion des auteurs : ajout, édition, suppression.
- Gestion des livres : ajout, édition, suppression.
- Recherche de livres par auteur.
- Commande d'importation des données (loaddb).
- Commande de création des tables (syncdb).
- Authentification utilisateur avec la gestion des comptes (commandes newuser, password) et restrictions d'accès pour certaines fonctionnalités aux utilisateurs authentifiés.

 ### Fonctionnalités avancées

- Ajout d'une table Genres pour catégoriser les livres.
- Relation Many-to-Many entre les livres et les genres.
- Gestion des favoris pour chaque utilisateur.
- Affichage paginé des livres, triés par ordre alphabétique des auteurs.
- Recherche avancée par titre, auteur ou prix.

 ## Installation

Nul besoin de tout installer soit même, un fichier makefile a été prévu a cet effet. Une fois la main sur le code source, il vous suffit de rentrer les commandes suivantes dans le répertoire pour tester notre application, il n'est pas nécessaire d'activé le venv soit même. La base de données est déjà créer.

Pour installer le nécessaire

    make install

Pour lancer l'application web

    make run

Pour recharger les données dans la base de données concernant les auteurs et les livres

    make loaddb

Pour créer un nouvel utilisateur ou changer un mot de passe, il est néanmoins nécessaire d'activé le venv

    source venv/bin/activate

Une fois le venv activé, pour créer un nouvel utilisateur

    newuser <nom> <mot de passe>

Pour changer le mot de passe d'un utilisateur

    passwd <nom> <nouveau mot de passe>

 ## Pour accédez à l'application via votre navigateur : http://127.0.0.1:5000
