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


# =========================================================
# Valeurs considérées comme True
# =========================================================
#
# Toutes les valeurs de cet ensemble seront converties
# en True.
#
# Exemple :
#
# "true"
# "1"
# "yes"
# "on"
#
# =========================================================

TRUE_SET = {"1", "true", "yes", "on"}


# =========================================================
# Valeurs considérées comme False
# =========================================================
#
# Toutes les valeurs de cet ensemble seront converties
# en False.
#
# Exemple :
#
# "false"
# "0"
# "no"
# "off"
#
# =========================================================

FALSE_SET = {"0", "false", "no", "off"}


# =========================================================
# Convertit une variable d'environnement en booléen
# =========================================================
#
# Paramètres :
#
# value :
# → valeur récupérée depuis os.getenv()
#
# default :
# → valeur retournée si :
#   - la variable n'existe pas
#   - la valeur est invalide
#
# Retour :
#
# bool
#
# =========================================================
#
# Exemple :
#
# env_bool("true")  -> True
# env_bool("false") -> False
# env_bool("yes")   -> True
# env_bool(None)    -> default
#
# =========================================================

def env_bool(value: str | None, default: bool = False) -> bool:


    # =====================================================
    # Cas où la variable n'existe pas
    # =====================================================
    #
    # os.getenv() peut retourner None si la variable
    # n'est pas définie dans le .env.
    #
    # Dans ce cas :
    #
    # on retourne la valeur par défaut.
    # =====================================================

    if value is None:
        return default


    # =====================================================
    # Normalisation de la chaîne
    # =====================================================
    #
    # strip()
    # → supprime les espaces inutiles
    #
    # lower()
    # → transforme en minuscule
    #
    # Exemple :
    #
    # " TRUE "
    #
    # devient :
    #
    # "true"
    # =====================================================

    v = value.strip().lower()


    # =====================================================
    # Vérifie si la valeur correspond à True
    # =====================================================

    if v in TRUE_SET:
        return True


    # =====================================================
    # Vérifie si la valeur correspond à False
    # =====================================================

    if v in FALSE_SET:
        return False


    # =====================================================
    # Valeur invalide ou inconnue
    # =====================================================
    #
    # Exemple :
    #
    # env_bool("bonjour")
    #
    # Retourne la valeur par défaut.
    # =====================================================

    return default