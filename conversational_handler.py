from chatbot import ISO27001Chatbot
from flask import jsonify

class GestionnaireConversation:
    def __init__(self):
        self.chatbot = ISO27001Chatbot()
        self.etape_actuelle = 0
        self.reponses_utilisateur = []
        self.controle = next(
            ctrl for cat in self.chatbot.knowledge_base["iso_27001_2022"]["controles_annexe_A"]["categories"]
            for ctrl in cat["controles"] if ctrl["id"] == "A.5.1"
        )
        self.questions = self.controle["conformite_check"]
        self.actions_correctives = self.controle["actions_correctives"]

    def reinitialiser(self):
        """Réinitialise l'état pour une nouvelle conversation."""
        self.etape_actuelle = 0
        self.reponses_utilisateur = []

    def demarrer_verification(self, requete_utilisateur):
        """Démarre la vérification de conformité si la requête concerne la conformité du SI."""
        requete = requete_utilisateur.lower()
        if "conforme" in requete and ("si" in requete or "système d'information" in requete or "politique de sécurité" in requete):
            self.reinitialiser()
            self.etape_actuelle = 1
            return {
                "response": self.questions[0],
                "etape": self.etape_actuelle,
                "en_attente_reponse": True
            }
        return None

    def traiter_reponse(self, requete_utilisateur):
        """Traite la réponse de l'utilisateur et passe à la question suivante ou au résultat si valide."""
        reponse = requete_utilisateur.lower().strip()

        if self.etape_actuelle > len(self.questions):
            return self.generer_resultat()

        if reponse not in ["oui", "non"]:
            return {
                "response": f"Veuillez répondre par 'oui' ou 'non' uniquement. {self.questions[self.etape_actuelle - 1]}",
                "etape": self.etape_actuelle,
                "en_attente_reponse": True
            }

        self.reponses_utilisateur.append(reponse == "oui")
        if self.etape_actuelle < len(self.questions):
            self.etape_actuelle += 1
            return {
                "response": self.questions[self.etape_actuelle - 1],
                "etape": self.etape_actuelle,
                "en_attente_reponse": True
            }
        else:
            return self.generer_resultat()

    def generer_resultat(self):
        """Génère le résultat final basé sur les réponses de l'utilisateur."""
        if len(self.reponses_utilisateur) != len(self.questions):
            reponse = "Erreur : toutes les questions n'ont pas été répondues correctement."
        elif all(self.reponses_utilisateur):
            reponse = "D'après vos réponses, il semble que votre politique de sécurité soit conforme à ISO 27001 (A.5.1)."
        else:
            points_non_conformes = [q for q, ans in zip(self.questions, self.reponses_utilisateur) if not ans]
            # Remplacer manuellement le texte arabe par du français si présent
            actions_fr = [action.replace("n'existe pas", "n'existe pas") for action in self.actions_correctives]
            reponse = (
                "Votre politique de sécurité n'est pas conforme à ISO 27001 (A.5.1) pour les raisons suivantes :\n" +
                "\n".join(f"- {q}" for q in points_non_conformes) +
                "\n\nActions correctives suggérées :\n" +
                "\n".join(f"- {action}" for action in actions_fr[:len(points_non_conformes)])
            )
        self.reinitialiser()
        return {
            "response": reponse,
            "etape": "terminee",
            "en_attente_reponse": False
        }

def chat_ameliore(requete_utilisateur, gestionnaire):
    """Fonction améliorée pour gérer les interactions conversationnelles."""
    if gestionnaire.etape_actuelle == 0 or gestionnaire.etape_actuelle == "terminee":
        reponse_initiale = gestionnaire.demarrer_verification(requete_utilisateur)
        if reponse_initiale:
            return jsonify(reponse_initiale)
        if "coût" in requete_utilisateur.lower() and "certification" in requete_utilisateur.lower():
            return jsonify({
                "response": "Le coût de la certification ISO 27001 varie entre 5 000 $ et 200 000 $ selon la taille de votre organisation et la complexité de votre SI. Contactez un organisme de certification pour une estimation précise.",
                "etape": "terminee",
                "en_attente_reponse": False
            })
        return jsonify({"response": gestionnaire.chatbot.get_response(requete_utilisateur)})
    else:
        return jsonify(gestionnaire.traiter_reponse(requete_utilisateur))