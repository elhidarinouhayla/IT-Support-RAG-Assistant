# IT-Support-RAG-Assistant


> Un assistant intelligent basé sur RAG (Retrieval-Augmented Generation) pour le support IT, déployé en production avec MLOps



##  Vue d'ensemble

L'**Assistant RAG IT Support** est une solution d'intelligence artificielle conçue pour améliorer l'efficacité des équipes support IT. Il permet de :

-  Répondre rapidement aux questions récurrentes
-  Guider les techniciens lors d'incidents
-  Standardiser les procédures IT
-  Réduire le temps de résolution des tickets
-  Capitaliser sur la connaissance interne

Le système exploite un PDF de procédures IT comme source de connaissance et utilise le RAG pour générer des réponses contextuelles précises.


---

##  Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Utilisateurs IT                       │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Backend FastAPI (Auth JWT)                  │
│  Endpoints: /auth/login, /query, /history, /health      │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ PostgreSQL   │ │   RAG Engine │ │   MLflow     │
│   Database   │ │  (LangChain) │ │   Tracking   │
│              │ │              │ │              │
│ - Users      │ │ - Retriever  │ │ - Metrics    │
│ - Queries    │ │ - LLM        │ │ - Artifacts  │
│ - Clusters   │ │ - ChromaDB   │ │ - Registry   │
└──────────────┘ └──────────────┘ └──────────────┘
                        │
                        ▼
                ┌──────────────┐
                │  Vector DB   │
                │  (ChromaDB)  │
                │              │
                │ - Embeddings │
                │ - Metadata   │
                └──────────────┘
```

### Workflow RAG

```
User Question → Embedding → Vector Search → Context Retrieval
                                                     ↓
Response ← LLM Generation ← Prompt + Context ← Top-K Chunks
```

---

##  Fonctionnalités

###  Authentification & Sécurité
- Système JWT pour l'authentification
- Gestion des utilisateurs avec comptes activables/désactivables
- Mots de passe hashés (bcrypt)

###  Moteur RAG
- **Ingestion de PDF** : Extraction et chunking intelligent du contenu
- **Embeddings** : Génération via HuggingFace (modèle open-source)
- **Recherche sémantique** : ChromaDB pour la similarité vectorielle
- **Génération** : LLM (Gemini/HuggingFace) avec prompts contrôlés
- **Contextualisation** : Réponses basées uniquement sur le contenu du PDF

###  Machine Learning Non Supervisé
- **Clustering des questions** : KMeans sur les embeddings
- **Analyse des tendances** : Identification des sujets fréquents
- **Métriques de qualité** : Score de similarité, latence

###  Monitoring & Traçabilité
- **MLflow Tracking** : Traçage des expérimentations
- **MLflow Registry** : Versionnement des modèles
- **Historique complet** : Questions, réponses, latences, clusters
- **Audit trail** : Traçabilité de tous les usages

###  Production-Ready
- **API RESTful** : Documentation Swagger automatique
- **Containerisation** : Docker & Docker Compose
- **Orchestration** : Kubernetes avec Lens Desktop
- **CI/CD** : GitHub Actions (tests, lint, build, deploy)
- **Health checks** : Endpoint de monitoring

---

##  Technologies

### Backend & API
- **FastAPI** : Framework web moderne et performant
- **PostgreSQL** : Base de données relationnelle
- **SQLAlchemy** : ORM Python
- **JWT** : Authentification stateless
- **Pydantic** : Validation des données

### Machine Learning & NLP
- **LangChain** : Framework RAG
- **HuggingFace Transformers** : Modèles d'embeddings
- **ChromaDB** : Base de données vectorielle
- **Gemini / HuggingFace** : LLM pour la génération
- **scikit-learn** : Clustering (KMeans)

### MLOps
- **MLflow** : Tracking & Registry
- **PyPDFLoader** : Extraction de PDF
- **Docker** : Containerisation
- **Kubernetes** : Orchestration
- **Lens Desktop** : Interface K8s

### DevOps
- **GitHub Actions** : CI/CD
- **Docker Compose** : Orchestration locale
- **kubectl** : CLI Kubernetes
- **Minikube** : Cluster local

---



##  Installation

### 1. Clone du repository

```bash
git clonehttps://github.com/elhidarinouhayla/IT-Support-RAG-Assistant.git
cd IT-Support-RAG-Assistant
```

### 2. Environnement virtuel

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Installation des dépendances

```bash
# Installation complète
pip install -r requirements.txt
```


##  Configuration

### Configuration du PDF

Placer votre PDF de support IT dans le dossier `data/` :

```bash
mkdir -p data/pdf
cp votre-manuel-it.pdf data/pdf/support_it.pdf
```

---

##  Utilisation

### Lancement local avec Docker Compose

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Services disponibles :
# - API FastAPI : http://localhost:8000
# - MLflow UI : http://localhost:5000
# - PostgreSQL : localhost:5432
```

### Lancement manuel (développement)

```bash
# Terminal 1 : PostgreSQL (via Docker)
docker run -d \
  --name postgres-rag \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=rag_it_assistant \
  -p 5432:5432 \
  postgres:15

# Terminal 2 : MLflow
mlflow server --host 0.0.0.0 --port 5000

# Terminal 3 : FastAPI
uvicorn app.main:app --reload
```





##  MLOps & Monitoring

### MLflow Tracking

Chaque requête est trackée automatiquement avec :

- **Paramètres** :
  - Modèle LLM utilisé
  - Température
  - Nombre de chunks récupérés (top_k)
  - Configuration du retriever

- **Métriques** :
  - Latence de la requête (ms)

- **Artifacts** :
  - Question posée
  - Réponse générée
  - Chunks contextuels utilisés
  - Prompt complet


## 🔄 CI/CD

### GitHub Actions Pipeline

Le workflow `.github/workflows/ci-cd.yml` automatise :

#### 1. **Tests & Quality**
```yaml
jobs:
  test:
    - Lint (flake8, black)
    - Tests unitaires (pytest)
    - Coverage report
```

#### 2. **Build**
```yaml
  build:
    - Build Docker image
    - Tag avec version
    - Push vers registry
```





##  Déploiement

### Kubernetes avec Lens Desktop

#### 1. Configuration du cluster local

```bash
# Démarrer Minikube
minikube start --cpus=4 --memory=8192

# Vérifier le cluster
kubectl cluster-info
```

#### 2. Créer les ressources

```bash
# Namespace
kubectl create namespace rag-it-assistant

# ConfigMap pour les variables
kubectl create configmap rag-config \
  --from-env-file=.env \
  -n rag-it-assistant

# Secret pour les credentials
kubectl create secret generic rag-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=secret-key=$SECRET_KEY \
  -n rag-it-assistant
```


---

## 🧪 Tests

### Tests unitaires

```bash
# Exécuter tous les tests
pytest
```




## 📁 Structure du projet

```
IT-Support-RAG-Assistant/
├── app/
│   ├── models/
│   │   ├── queries_model.py
│   │   └── users_model.py
│   ├── schemas/
│   │   ├── queries_schema.py
│   │   └── users_schema.py
│   ├── services/
│   │   ├── kmeans_service.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   └── main.py
│   ├── cluster/
│   └── data/
├── mlflow/
│   └── mlflow.py
├── tests/
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   └── test_full_pipeline.py
│   ├── test_loading.py
│   ├── test_query.py
│   ├── test_rag_pipeline.py
│   └── conftest.py
├── utils/
│   ├── embedding.py
│   ├── pdf_loading.py
│   └── text_splitter.py
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secrets.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```
---






