# -------------------------------
# Imports nécessaires
# -------------------------------
import os
import django
from fastmcp import FastMCP  # Classe FastMCP pour créer un serveur MCP
from asgiref.sync import sync_to_async  # Pour convertir les fonctions synchrones en asynchrones (compatible Django ORM)

# -------------------------------
# Initialisation de l'environnement Django
# -------------------------------
# Remplacer 'firstProject' par le nom réel de ton projet Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference3IA2.settings")
django.setup()

# -------------------------------
# Import des modèles Django
# -------------------------------
from ConferenceApp.models import Conference  # Modèle pour les conférences
from SessionApp.models import Session        # Modèle pour les sessions

# -------------------------------
# Création du serveur MCP
# -------------------------------
mcp = FastMCP("Conference Assistant")  # Nom du serveur MCP
#-------------------------
# -------------------------------
# Outil MCP pour lister toutes les conférences
# -------------------------------
#question 1/a
@mcp.tool()
async def list_conferences() -> str:
    """Liste toutes les conférences disponibles."""

    # Fonction interne synchrone pour récupérer les conférences depuis la base de données
    @sync_to_async  # Permet d'utiliser l'ORM Django dans un contexte asynchrone
    def _get_conferences():
        return list(Conference.objects.all())

    # Appel asynchrone pour récupérer les conférences
    conferences = await _get_conferences()

    # Vérification si aucune conférence n'est trouvée
    if not conferences:
        return "No conferences found."

    # Construction d'une chaîne formatée avec le nom et les dates des conférences
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

#question 1/b
# -------------------------------
# Outil MCP pour obtenir les détails d'une conférence spécifique
# -------------------------------

@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Obtenir les détails d'une conférence spécifique par son nom."""

    # Fonction interne synchrone pour récupérer la conférence depuis la base de données
    @sync_to_async
    def _get_conference():
        try:
            # Recherche de la conférence dont le nom contient la chaîne 'name'
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None  # Aucune conférence trouvée
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"  # Plusieurs conférences trouvées

    # Appel asynchrone pour récupérer la conférence
    conference = await _get_conference()

    # Gestion des cas particuliers
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conference:
        return f"Conference '{name}' not found."

    # Construction d'une chaîne formatée avec les détails de la conférence
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )
#question 1/c
# -------------------------------
# Outil MCP pour lister les sessions d'une conférence spécifique
# -------------------------------

@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """Lister les sessions pour une conférence spécifique par son nom."""

    # Fonction interne synchrone pour récupérer les sessions depuis la base de données
    @sync_to_async
    def _get_sessions():
        try:
            # Recherche de la conférence correspondant au nom
            conference = Conference.objects.get(name__icontains=conference_name)
            # Retourne la liste des sessions et l'objet conférence
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None  # Conférence non trouvée
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None  # Plusieurs conférences trouvées

    # Appel asynchrone pour récupérer les sessions
    result, conference = await _get_sessions()

    # Gestion des cas particuliers
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    if conference is None:
        return f"Conference '{conference_name}' not found."

    sessions = result

    # Vérification si aucune session n'est disponible
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."

    # Construction de la liste formatée des sessions
    session_list = [
        f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n  Topic: {s.topic}"
        for s in sessions
    ]

    return "\n".join(session_list)
#question 1/d
# -------------------------------
# Outil MCP libre : filtrer les conférences par thème
# -------------------------------

@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filtrer les conférences selon un thème spécifique."""

    # Fonction interne synchrone pour récupérer les conférences correspondant au thème
    @sync_to_async
    def _get_conferences_by_theme():
        return list(Conference.objects.filter(theme__icontains=theme))

    # Appel asynchrone pour récupérer les conférences
    conferences = await _get_conferences_by_theme()

    # Vérification si aucune conférence n'est trouvée
    if not conferences:
        return f"No conferences found with theme '{theme}'."

    # Construction de la liste formatée
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

# -------------------------------
# Lancement du serveur
# -------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")  # Transport stdio (console)
