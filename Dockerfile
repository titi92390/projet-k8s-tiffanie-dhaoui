# Utilisation d'une image Python légère
FROM python:3.10-slim

# Définition du dossier de travail
WORKDIR /app

# Copie du fichier requirements (dépendances)
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code
COPY . .

# L'application écoutera sur le port 80
EXPOSE 80

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
