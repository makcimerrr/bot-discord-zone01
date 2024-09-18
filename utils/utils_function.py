import re
from utils.config_loader import forbidden_words

def get_query_intern(self):
    """Renvoie la valeur actuelle de query_intern."""
    return self.query_intern

def get_query_fulltime(self):
    """Renvoie la valeur actuelle de query_fulltime."""
    return self.query_fulltime

def contains_forbidden_words(text):
    """Vérifie si un texte contient des mots interdits."""
    if text:
        text = text.lower()
        for word in forbidden_words:
            if word.lower() in text:
                return True
    return False

def extract_technologies(description, technologies):
    """Extrait les technologies mentionnées dans la description."""
    extracted_techs = []
    for tech in technologies:
        if re.search(rf"\b{tech}\b", description, re.IGNORECASE):
            extracted_techs.append(tech)
    return extracted_techs