# =========================================================
# toggle.py
# =========================================================
#
# Ce fichier contient des helpers utilitaires permettant
# de convertir des variables d'environnement en booléens.
#
# Pourquoi ?
#
# Les variables d'environnement sont toujours lues
# sous forme de chaînes de caractères :
#
# "true"
# "false"
# "1"
# "0"
#
# et non comme de vrais booléens Python.
#
# Ce helper permet :
#
# - d'éviter les bugs
# - de centraliser la logique de conversion
# - de rendre le .env flexible
# - d'avoir un système de toggles propre
#
# Exemple :
#
# USE_OLLAMA=true
# USE_VISION=no
#
# deviennent :
#
# True
# False
#
# =========================================================


# Valeurs considérées comme True
TRUE_SET = {"1", "true", "yes", "on"}

# Valeurs considérées comme False
FALSE_SET = {"0", "false", "no", "off"}


# =========================================================
# Convertit une variable d'environnement en booléen
# =========================================================
def env_bool(value: str | None, default: bool = False) -> bool:
    
    # Cas où la variable n'existe pas
    if value is None:
        return default

    # Normalisation de la chaîne
    v = value.strip().lower()

    # Vérifie si la valeur correspond à True
    if v in TRUE_SET:
        return True

    # Vérifie si la valeur correspond à False
    if v in FALSE_SET:
        return False

    # Valeur invalide ou inconnue
    return default