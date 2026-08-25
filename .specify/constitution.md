\# 📜 Constitution d'Ingénierie \& Standards de Développement Universels

Ce document définit les règles d'architecture, de conception, de codage et de documentation ABSOLUES pour ce projet. 

Tout agent IA (Spec Kit, Antigravity,opencode,claude code) ou développeur humain travaillant sur cette base de code DOIT respecter strictement ces directives.

\---


\## 1. Principes Fondamentaux de Conception (Core Engineering Principles)


\* \*\*KISS (Keep It Simple, Stupid) :\*\* Préférer toujours la solution la plus simple et la plus lisible à une solution sur-ingéniérée. La clarté prime sur la démonstration de complexité.

\* \*\*YAGNI (You Ain't Gonna Need It) :\*\* Ne JAMAIS développer une fonctionnalité, une abstraction ou une anticipation d'architecture qui n'est pas explicitement requise par la spécification actuelle.

\* \*\*SOLID \& DRY :\*\*

&#x20; \* \*\*Single Responsibility :\*\* Une classe, un composant ou un service = une seule raison de changer.

&#x20; \* \*\*DRY (Don't Repeat Yourself) :\*\* Centraliser la logique métier, la validation et les calculs pour éviter toute duplication.

\* \*\*Simplicity and Focus :\*\* Chaque module doit répondre à un besoin métier précis. Pas de dépendances inutiles, pas de code mort.


\---


\## 2. Standards de Documentation \& Explications de Code


\* \*\*Documentation Système \& API (Exigence Obligatoire) :\*\*

&#x20; \* \*\*Documentation API :\*\* Le Backend doit auto-générer une documentation OpenAPI 3.0 / Swagger accessible à l'URL `/swagger-ui.html`. Chaque endpoint REST doit comporter une description explicite des codes HTTP de retour et des DTOs.

&#x20; \* \*\*Architecture \& Stack :\*\* Maintenir à jour un document décrivant la stack technique retenue, les choix stratégiques d'architecture (patterns, sécurité, modèles de données) et la matrice de flux.

\* \*\*Commentaires dans le Code :\*\* 

&#x20; \* Interdiction d'écrire des commentaires triviaux qui répètent ce que fait le code (ex: `// Incrémente i`).

&#x20; \* Tout commentaire doit expliquer le \*\*POURQUOI\*\* (intention métier, contrainte technique complexe) et non le \*\*COMMENT\*\*.

&#x20; \* Utiliser le format Standard (Javadoc / TypeDoc) uniquement sur les signatures publiques (interfaces, méthodes de services métier).

\* \*\*Code Auto-Documenté :\*\* Nommage explicite et expressif des variables, méthodes et classes.


\---


\## 3. Structure des READMEs \& Prise en Main (Global \& Individuels)


Tout projet doit comporter une structure de documentation à double niveau :


\### A. Niveau Racine (`./README.md`) — Vue d'Ensemble du Projet

\* \*\*Présentation \& Architecture globale :\*\* Explication synthétique du système, schémas de communication (Back $\\leftrightarrow$ Front), stack complète (Spring Boot, Angular, PostgreSQL, etc.).

\* \*\*Quickstart Monorepo / Global :\*\* Instructions pour cloner, configurer les variables d'environnement globales, et tout lancer en une seule commande (ex: via `docker-compose`).

\* \*\*Guide de Déploiement :\*\* Procédure complète pour le déploiement multi-services (Conteneurisation Docker, variables de production, CI/CD).



\### B. Niveau Backend (`./backend/README.md`) — Guide Développeur Backend

\* \*\*Stack \& Prérequis :\*\* Version du JDK (Java 17/21), Maven/Gradle, dépendances majeures (Spring Security, JPA, MapStruct).

\* \*\*Guide de Prise en Main :\*\*

&#x20; 1. Configuration de la base de données locale (PostgreSQL / MySQL).

&#x20; 2. Variables d'environnement nécessaires (`application-dev.yml`).

&#x20; 3. Commandes pour compiler, lancer le serveur et exécuter les tests.

\* \*\*Documentation API \& Swagger :\*\* Lien local vers le Swagger UI et exemples de requêtes cURL pour tester les endpoints principaux.



\### C. Niveau Frontend (`./frontend/README.md`) — Guide Développeur Frontend

\* \*\*Stack \& Prérequis :\*\* Version de Node.js, npm/pnpm, Angular CLI.

\* \*\*Guide de Prise en Main :\*\*

&#x20; 1. Installation des dépendances (`npm install`).

&#x20; 2. Configuration de l'URL du Backend (`environment.ts`).

&#x20; 3. Commandes pour lancer le serveur de dev (`ng serve`), le linter et les tests unitaires (`ng test`).

\* \*\*Architecture des Composants :\*\* Description de l'arborescence des modules/components standalone, gestion du state (Signals/RxJS) et routing.



\---



\## 4. Architecture \& Méthodologie Twelve-Factor (Deployability)



Le code doit être prêt pour le déploiement continu, conteneurisé et cloud-native (12-Factor App) :



\* \*\*Scalability \& Portability :\*\* 

&#x20; \* L'application doit être totalement stateless (sans état en mémoire) au niveau du serveur Web pour permettre un passage à l'échelle horizontal rapide.

&#x20; \* Aucune dépendance liée à l'OS sous-jacent.

\* \*\*Configuration par l'Environnement (Factor III) :\*\* 

&#x20; \* ZÉRO secret, URL ou clé d'API en dur dans le code. Tout passe par des variables d'environnement (`application.yml` lit des variables `${...}`).

\* \*\*Services Appariés / Backing Services (Factor IV) :\*\* 

&#x20; \* La BDD, les caches, et les services tiers sont traités comme des ressources attachées configurables via URL/identifiants.

\* \*\*Logs en Flux (Factor XI) :\*\* 

&#x20; \* Écrire les logs sur la sortie standard (`stdout`) au format JSON structuré, sans gestion interne de fichiers de logs locaux.



\---



\## 5. Standards Backend (Spring Boot / Java)



\* \*\*Architecture en Couches Stricte :\*\* `Controller` $\\rightarrow$ `Service` $\\rightarrow$ `Repository`.

\* \*\*Découplage DTO / Entités JPA :\*\*

&#x20; \* Les entités JPA ne doivent JAMAIS être exposées via les contrôleurs REST.

&#x20; \* Utiliser systématiquement des DTOs pour les requêtes et réponses, convertis via un mapper dédié (ex: MapStruct).

\* \*\*Immutabilité \& Temps :\*\*

&#x20; \* Préférer l'immutabilité (`record` Java pour les DTOs).

&#x20; \* Les dates/timestamps doivent OBLIGATOIREMENT être gérés en UTC via le type `Instant` (Java) 

\* \*\*Gestion Globale des Erreurs :\*\* 

&#x20; \* Centraliser toutes les exceptions métier via un `@ControllerAdvice` renvoyant un format d'erreur JSON normalisé (Status, Timestamp, Message, Errors).

\* \*\*Bases de Données \& Performance :\*\*

&#x20; \* Utiliser des pools de connexion optimisés (HikariCP).

&#x20; \* Optimiser les requêtes JPA pour éviter rigoureusement le problème N+1 (utilisation de `JOIN FETCH` ou `@EntityGraph`).



\---



\## 6. Standards Frontend (Angular / TypeScript)



\* \*\*Typage Strict (No `any`) :\*\* Le type `any` est STRICTEMENT INTERDIT. Tout modèle, réponse d'API et variable doit être typé via des interfaces ou types dédiés.

\* \*\*Composants Standalone \& Modularité :\*\* Préférer l'architecture Standalone à responsabilité unique.

\* \*\*Réactivité Propre :\*\* Utiliser Angular Signals et RxJS. Tout abonnement (`subscribe`) à un Observable doit être automatiquement nettoyé pour éviter les fuites de mémoire.



\---



\## 7. Stratégie de Test (Thorough Testing)



\* \*\*Couverture Ciblée :\*\* Chaque service contenant de la logique métier DOIT avoir ses tests unitaires.

\* \*\*Tests aux Limites (Edge Cases) :\*\* Ne pas tester uniquement le "Happy Path". Les tests doivent obligatoirement vérifier la gestion des erreurs, les valeurs nulles/limites et les levées d'exceptions.

\* \*\*Indépendance des Tests :\*\* Les tests unitaires et d'intégration doivent être isolés, déterministes et exécutables dans n'importe quel ordre.



\## 8. Modélisation \& Diagrammes de Domaine

\* S'il existe des diagrammes UML (PDF, PlantUML ou Mermaid) dans le dossier `.specify/diagrams/`, l'agent DOIT s'y conformer strictement pour la création des entités JPA, des interfaces et des relations.

\* Aucune entité ou méthode majeure non présente ou non justifiée par le diagramme ne doit être inventée (respect de YAGNI).



\## 9. Modélisation \& Architecture Cible du Projet



\* \*\*Architecture en Couches / Hexagonale Stricte :\*\* 

&#x20; \* \*\*Backend (Spring Boot) :\*\* Structuration obligatoire par domaine/feature :

&#x20;   \* `config/` : Configurations globales (Security, CORS, Swagger, Database).

&#x20;   \* `entity/` : Modèles métiers JPA internes.

&#x20;   \* `dto/` : Objets de transfert de données immuables (`records` Java).

&#x20;   \* `mapper/` : Interfaces de mapping (MapStruct).

&#x20;   \* `repository/` : Interfaces Spring Data JPA.

&#x20;   \* `service/` : Interfaces et implémentations de la logique métier.

&#x20;   \* `controller/` : Contrôleurs REST, DTOs de requête/réponse et gestion des erreurs.

&#x20; \* \*\*Frontend (Angular) :\*\* Modularité par fonctionnalité (Feature-Driven Architecture) :

&#x20;   \* `core/` : Services singletons, guards, interceptors HTTP.

&#x20;   \* `shared/` : Composants UI réutilisables, pipes, directives.

&#x20;   \* `features/` : Modules fonctionnels isolés (ex: `menu/`, `order/`, `payment/`) contenant leurs propres composants standalone, services et modèles.



\---



\## 10. Stratégie de Commits Git \& Versionnement Atomique



\* \*\*Commits Automatisés par Fonctionnalité :\*\* 

&#x20; \* À la fin de chaque implémentation de module, tranche ou fonctionnalité validée, l'agent DOIT créer un commit Git atomique.

&#x20; \* Aucun code non fonctionnel ou non testé ne doit être commit.

\* \*\*Norme Conventional Commits :\*\* Les messages de commit doivent respecter rigoureusement le format :

&#x20; \* `feat(<scope>): <description courte en minuscules>` (pour une nouvelle fonctionnalité).

&#x20; \* `fix(<scope>): <description du correctif>` (pour un bugfix).

&#x20; \* `refactor(<scope>): <description du refactoring>` (pour une amélioration sans changement comportemental).

&#x20; \* `docs(<scope>): <mise à jour de la documentation ou README>`.

&#x20; \* \*Exemple :\* `feat(order): implementation of state machine and order service`

