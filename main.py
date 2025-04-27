from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Définir un modèle de données pour la requête utilisateur
class ChatRequest(BaseModel):
    message: str

# Créer une instance FastAPI
app = FastAPI(
    title="MindCare Backend avec UV",
    description="Backend FastAPI pour connecter le frontend à UV ou un modèle IA",
    version="1.0.0",
)

# Fonction pour interroger le moteur UV
def query_uv_model(message: str, model: str = "mental-health-model") -> str:
    """
    Fonction pour envoyer un message au moteur UV et récupérer une réponse.
    """
    uv_url = "http://localhost:1234/api/v1/chat"  # Remplacez par l'URL de votre service UV
    payload = {
        "model": model,
        "input": message,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(uv_url, json=payload, headers=headers)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        return response.json().get("response", "Je suis désolé, je n'ai pas compris.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur avec UV : {str(e)}")

# Endpoint pour gérer les messages de l'utilisateur
@app.post("/api/response", tags=["Chat"])
async def get_chat_response(request: ChatRequest):
    user_message = request.message

    try:
        # Appeler le moteur UV
        bot_response = query_uv_model(user_message)
    except HTTPException as e:
        raise e

    # Retourner la réponse au frontend
    return {"reply": bot_response}

# Endpoint pour tester si l'API est en ligne
@app.get("/", tags=["Health Check"])
async def health_check():
    return {"status": "OK", "message": "MindCare Backend avec UV en cours d'exécution"}