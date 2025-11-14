Déploiement Kubernetes – Projet de Tiffanie & Dhaoui

Ce dépôt correspond à la partie du projet réalisée par Tiffanie et Dhaoui, qui consiste à déployer une application FastAPI reliée à une base PostgreSQL dans un cluster Kubernetes, avec surveillance, stockage persistant et autoscaling.

Objectifs de notre partie du projet :

- Containeriser l’application FastAPI
- Déployer l'application dans Kubernetes
- Déployer PostgreSQL de manière persistante
- Gérer la configuration et les secrets
- Mettre en place un Ingress pour un accès externe
- Activer l’autoscaling (HPA)
- Tester la communication entre les pods
- Mettre en place les outils de monitoring Kubernetes

1. STRUCTURE DU PROJET

Voici tous les fichiers constituant notre déploiement Kubernetes :

.
├── main.py
├── Dockerfile
├── requirements.txt
│
├── deployment.yaml              # Déploiement de l’application FastAPI
├── service.yaml                 # Service ClusterIP de l'application├── ingress.yaml                 # Accès externe (Traefik + URL notreapp.local)
├── hpa.yaml                     # Autoscaling Horizontal
│
├── postgres-statefulset.yaml    # PostgreSQL avec stockage persistant
├── postgres-service.yaml        # Service de PostgreSQL
├── pv.yaml                      # Volume physique
├── pvc.yaml                     # Claim du volume
│
└── README.md

2. DESCRIPTION DE L'ARCHITECTURE

Application FastAPI

- Exposée sur le port 80
- Routes :
  - GET /items : liste les items 
  - POST /items?name=xxx : ajoute un item
- Stocke les données dans PostgreSQL via SQLAlchemy

PostgreSQL (StatefulSet)

- Déployé comme StatefulSet pour garantir :
 - une identité de pod stable
 - un disque propre au pod

- Utilise :
 - un PersistentVolume (1Gi)
 - un PersistentVolumeClaim

Nous avons créé :
✔ la DB app_db
✔ l’utilisateur adminuser
✔ le mot de passe correspondant
✔ la table items

Gestion des secrets 

Un secret Kubernetes stocke :
- POSTGRES_HOST
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

Ces variables sont injectées dans l’application au lancement.

Ingress + Traefik

Un Ingress permet d’accéder à l’application via :
http://notreapp.local
(Entrée ajoutée dans /etc/hosts de la VM)

Autoscaling (HPA)

HorizontalPodAutoscaler configuré :
- min : 2 pods
- max : 5 pods
- scale si CPU > 60%

Metrics-server a été activé pour permettre le monitoring des pods.

3. Étapes d’installation / déploiement

3.1 Prérequis
- Minikube
- kubectl
- Docker (lié à Minikube)
- Traefik activé (minikube addons enable ingress)
- Metrics-server activé (minikube addons enable metrics-server)

4. Déploiement complet

Lancer les commandes suivantes dans cet ordre :

1) Construire l'image Docker dans Minikube
eval $(minikube docker-env)
docker build -t notre_application .

2️) Déployer PostgreSQL
kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f postgres-service.yaml

Créer l’utilisateur + DB :

kubectl exec -it postgres-0 -- bash
psql -U postgres

CREATE USER adminuser WITH PASSWORD 'monmotdepasse';
CREATE DATABASE app_db OWNER adminuser;
\c app_db

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT
);


3) Créer le secret PostgreSQL
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_HOST=postgres \
  --from-literal=POSTGRES_DB=app_db \
  --from-literal=POSTGRES_USER=adminuser \
  --from-literal=POSTGRES_PASSWORD=monmotdepasse

4) Déployer l’application FastAPI
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

5) Déployer l’Autoscaler
kubectl apply -f hpa.yaml

6) Vérifier le cluster
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl top pods

5. Tests de fonctionnement

➤ Ajouter un item
curl -X POST "http://notreapp.local/items?name=bonjour"

Réponse attendue :
{"status":"ok","name":"bonjour"}

➤ Récupérer les items
curl http://notreapp.local/items

Réponse :
[{"id":1,"name":"bonjour"}]

6. Monitoring

Nous avons utilisé :

- kubectl top pods
- kubectl top nodes
- Metrics-server

Permet :
✔ surveillance CPU/mémoire
✔ HPA fonctionnel

7. Ce que nous avons accompli

✔ Containerisation complète de l’application
✔ Déploiement Kubernetes professionnel
✔ Mise en place d’une base PostgreSQL persistante
✔ Configuration des secrets
✔ Ingress + DNS local fonctionnel
✔ Autoscaling avec HPA
✔ Monitoring du cluster
✔ Tests complets API + DB validés
✔ Structure propre et reproductible

8. Auteurs

Projet réalisé par :
Tiffanie & Dhaoui
Partie Kubernetes du projet DevOps.
