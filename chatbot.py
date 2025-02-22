import json
import os
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

class ISO27001Chatbot:
    def __init__(self, knowledge_base_path="data/iso27001.json"):
        """Initialize chatbot with SpaCy and TF-IDF."""
        self.nlp = spacy.load("fr_core_news_md")
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)
        self.corpus = []
        self.responses = []
        self.spaCy_vectors = []
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_vectors = None
        self.prepare_corpus()

    def load_knowledge_base(self, path):
        """Load ISO 27001 knowledge base from JSON."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def prepare_corpus(self):
        """Prepare corpus for SpaCy and TF-IDF matching."""
        kb = self.knowledge_base["iso_27001_2022"]
        documents = []

        # Metadata
        metadata_text = f"{kb['metadata']['title']} {kb['metadata']['version']} Sections principales : {', '.join(kb['metadata']['sections_principales'])}"
        documents.append(metadata_text)
        self.responses.append({"type": "metadata", "content": metadata_text})

        # Exigences clés
        for req in kb["exigences_cles"]:
            doc = f"{req['titre']} {req['description']}"
            documents.append(doc)
            self.responses.append({
                "type": "exigence",
                "section": req["section"],
                "titre": req["titre"],
                "description": req["description"],
                "conformite_check": req.get("conformite_check", []),
                "actions_correctives": req.get("actions_correctives", [])
            })

        # Contrôles Annexe A
        for category in kb["controles_annexe_A"]["categories"]:
            category_text = f"{category['nom']} (Catégorie {category['id']})"
            documents.append(category_text)
            self.responses.append({"type": "category", "content": category_text})
            for control in category["controles"]:
                doc = f"{control['titre']} {control['description']} {control.get('exigences', '')} {' '.join(control.get('mots_cles', []))}"
                documents.append(doc)
                self.responses.append({
                    "type": "controle",
                    "section": control["id"],
                    "titre": control["titre"],
                    "description": control["description"],
                    "exigences": control.get("exigences", ""),
                    "bonnes_pratiques": control.get("bonnes_pratiques", []),
                    "conformite_check": control.get("conformite_check", []),
                    "actions_correctives": control.get("actions_correctives", [])
                })

        # Workflow typique
        for phase in kb["workflow_typique"]["phases"]:
            doc = f"{phase['phase']} : {' '.join(phase['etapes'])}"
            documents.append(doc)
            self.responses.append({
                "type": "workflow",
                "phase": phase["phase"],
                "etapes": phase["etapes"]
            })

        # FAQ Chatbot
        for faq in kb["faq_chatbot"]:
            question = faq["question"]
            documents.append(question)
            self.responses.append({
                "type": "faq",
                "question": question,
                "content": faq["reponse"] if isinstance(faq["reponse"], str) else "\n".join(faq["reponse"])
            })

        self.corpus = documents
        self.tfidf_vectors = self.tfidf_vectorizer.fit_transform(documents)
        self.spaCy_vectors = np.array([self.nlp(doc).vector for doc in documents])

    def is_gibberish(self, text):
        """Check if input is gibberish."""
        vowels = set('aeiouéèàêôûùîï')
        text = text.lower()
        total_chars = len(text)
        if total_chars < 3:
            return True
        meaningful_chars = sum(1 for char in text if char in vowels or char.isspace())
        return total_chars > 5 and (meaningful_chars / total_chars < 0.2)

    def split_questions(self, user_query):
        """Split user input into separate questions with improved detection."""
        separators = [" et aussi ", " et ", ",", ";", "?", "!"]
        question_starters = ["qu'est-ce que", "comment", "pourquoi", "quels", "quelle", "est-ce que", "combien"]
        temp_query = user_query.strip()
        
        for sep in separators:
            temp_query = temp_query.replace(sep, f"|||SEP_{sep}|||")

        parts = temp_query.split("|||")
        questions = []
        current_question = ""

        for part in parts:
            if "SEP_" in part:
                if current_question and not self.is_gibberish(current_question):
                    questions.append(current_question.strip())
                current_question = ""
                sep = part.replace("SEP_", "")
                if sep in ["?", "!"]:
                    current_question += sep
            else:
                current_question += part

        if current_question and not self.is_gibberish(current_question):
            questions.append(current_question.strip())

        if len(questions) <= 1 and not any(sep in user_query for sep in separators):
            temp_questions = []
            current = ""
            words = user_query.split()
            for i, word in enumerate(words):
                if any(word.lower().startswith(starter.split()[0]) for starter in question_starters) and current:
                    temp_questions.append(current.strip())
                    current = word
                else:
                    current += " " + word if current else word
            if current:
                temp_questions.append(current.strip())
            questions = temp_questions

        return [q for q in questions if q and len(q) > 10 and not self.is_gibberish(q)]

    def compute_combined_similarity(self, user_query):
        """Compute combined SpaCy and TF-IDF similarity."""
        query_doc = self.nlp(user_query)
        query_spaCy_vector = query_doc.vector
        spaCy_similarities = np.dot(self.spaCy_vectors, query_spaCy_vector) / (
            np.linalg.norm(self.spaCy_vectors, axis=1) * np.linalg.norm(query_spaCy_vector) + 1e-8
        )

        query_tfidf = self.tfidf_vectorizer.transform([user_query])
        tfidf_similarities = np.array([
            np.dot(query_tfidf.toarray()[0], self.tfidf_vectors[i].toarray()[0]) / (
                np.linalg.norm(query_tfidf.toarray()[0]) * np.linalg.norm(self.tfidf_vectors[i].toarray()[0]) + 1e-8
            ) for i in range(len(self.corpus))
        ])

        return 0.7 * spaCy_similarities + 0.3 * tfidf_similarities

    def build_response(self, matched_item, user_query):
        """Build a formatted response."""
        response_type = matched_item["type"]
        user_query_lower = user_query.lower()

        if response_type == "faq":
            return matched_item["content"]
        elif response_type == "metadata":
            return f"Informations générales : {matched_item['content']}"
        elif response_type == "exigence":
            response = f"{matched_item['titre']} (Clause {matched_item['section']}) : {matched_item['description']}"
            if "conforme" in user_query_lower or "vérifier" in user_query_lower:
                if matched_item["conformite_check"]:
                    response += "\n\nVérification de conformité :\n" + "\n".join(f"- {q}" for q in matched_item["conformite_check"])
                    if "non" in user_query_lower and matched_item["actions_correctives"]:
                        response += "\n\nActions correctives :\n" + "\n".join(f"- {action}" for action in matched_item["actions_correctives"])
            return response
        elif response_type == "category":
            return f"Catégorie : {matched_item['content']}"
        elif response_type == "controle":
            response = f"{matched_item['titre']} (A.{matched_item['section']}) : {matched_item['description']}"
            if matched_item["exigences"]:
                response += f"\nExigences : {matched_item['exigences']}"
            if matched_item["bonnes_pratiques"]:
                response += "\nBonnes pratiques :\n" + "\n".join(f"- {bp}" for bp in matched_item["bonnes_pratiques"])
            if "conforme" in user_query_lower or "vérifier" in user_query_lower:
                if matched_item["conformite_check"]:
                    response += "\n\nVérification de conformité :\n" + "\n".join(f"- {q}" for q in matched_item["conformite_check"])
                    if "non" in user_query_lower and matched_item["actions_correctives"]:
                        response += "\n\nActions correctives :\n" + "\n".join(f"- {action}" for action in matched_item["actions_correctives"])
            return response
        elif response_type == "workflow":
            return f"Phase : {matched_item['phase']}\nÉtapes :\n" + "\n".join(f"- {step}" for step in matched_item["etapes"])
        return "Réponse non formatée, veuillez vérifier la base de connaissances."

    def get_response(self, user_query):
        """Find and return a single cohesive response for multiple questions."""
        print(f"Recherche en cours pour : '{user_query}'...")
        if self.is_gibberish(user_query):
            return "Je ne comprends pas votre saisie. Posez-moi une question claire sur ISO 27001 !"

        questions = self.split_questions(user_query)
        if not questions:
            return "Aucune question valide détectée. Posez-moi une question sur ISO 27001 !"

        responses = []
        for q in questions:
            print(f"  Traitement de la question : '{q}'...")
            combined_scores = self.compute_combined_similarity(q)
            best_match_idx = combined_scores.argmax()
            similarity_score = combined_scores[best_match_idx]

            if similarity_score > 0.65:
                matched_item = self.responses[best_match_idx]
                response = self.build_response(matched_item, q)
                print(f"  Trouvé une correspondance avec un score de {similarity_score:.2f}")
                responses.append(response)
            else:
                print(f"  Aucune correspondance pertinente trouvée pour '{q}'.")
                responses.append(f"Je n’ai pas trouvé de réponse pertinente dans iso27001.json pour '{q}'.")

        if len(responses) == 1:
            return responses[0]
        else:
            combined_response = "Voici les réponses à vos questions : "
            for i, resp in enumerate(responses):
                combined_response += resp
                if i < len(responses) - 1:
                    combined_response += " Par ailleurs, "
            return combined_response

    def log_query(self, user_query, response, db=None):
        """Log query and response."""
        log_entry = {
            "query": user_query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        log_path = "logs/chatbot_logs.json"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []
        else:
            logs = []
        logs.append(log_entry)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

        # Use explicit None check for MongoDB logging
        if db is not None:
            try:
                db["conversations"].insert_one(log_entry)
                print(f"Conversation enregistrée dans MongoDB : {user_query}")
            except Exception as e:
                print(f"Erreur lors de l'enregistrement dans MongoDB : {e}")

if __name__ == "__main__":
    chatbot = ISO27001Chatbot()
    print("Chatbot ISO 27001\nLogo\nBonjour ! Comment puis-je vous aider avec ISO 27001 ?")
    
    # Test cases
    test_queries = [
        "Comment maintenir la certification ISO 27001 ? ISO 27001 aide-t-elle à respecter le RGPD ?",
        "ISO 27001 aide-t-elle à respecter le RGPD ,,,,Comment maintenir la certification ISO 27001",
        "ISO 27001 aide-t-elle à respecter le RGPD ,Comment maintenir la certification ISO 27001",
        "Comment maintenir la certification ISO 27001 ISO 27001 aide-t-elle à respecter le RGPD"
    ]
    
    for query in test_queries:
        print(f"\nUtilisateur : {query}")
        response = chatbot.get_response(query)
        print(f"Chatbot : {response}")
        chatbot.log_query(query, response)