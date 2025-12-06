from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid

# -------------------------------
# Utility functions
# -------------------------------
def generate_user_id():
    """
    Génère un identifiant unique pour un utilisateur,
    sous la forme USERXXXX (4 caractères hexadécimaux en majuscules).
    """
    return "USER" + uuid.uuid4().hex[:4].upper()

def verify_email(email):
    """
    Vérifie que l'email appartient à un domaine universitaire autorisé.
    Domains autorisés : esprit.tn, seasame.com, tek.tn, central.net
    """
    domaines = ["esprit.tn", "seasame.com", "tek.tn", "central.net"]
    email_domaine = email.split("@")[1]
    if email_domaine not in domaines:
        raise ValidationError(
            "L'email est invalide et doit appartenir à un domaine universitaire privé"
        )

# Regex validator pour les noms
name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message="Ce champ ne doit contenir que des lettres et des espaces"
)


# -------------------------------
# User Model
# -------------------------------
class User(AbstractUser):
    """
    Modèle représentant un utilisateur.
    Hérite de AbstractUser pour inclure les fonctionnalités Django standard.
    """
    user_id = models.CharField(
        max_length=8, primary_key=True, unique=True, editable=False,
        help_text="ID unique généré automatiquement"
    )
    first_name = models.CharField(
        max_length=255, validators=[name_validator],
        help_text="Prénom de l'utilisateur (lettres et espaces uniquement)"
    )
    last_name = models.CharField(
        max_length=255, validators=[name_validator],
        help_text="Nom de l'utilisateur (lettres et espaces uniquement)"
    )

    ROLE = [
        ("participant", "Participant"),
        ("commitee", "Organizing committee member"),
    ]
    role = models.CharField(
        max_length=255, choices=ROLE, default="participant",
        help_text="Rôle de l'utilisateur"
    )

    affiliation = models.CharField(max_length=255, help_text="Affiliation académique ou institutionnelle")
    email = models.EmailField(unique=True, validators=[verify_email], help_text="Email universitaire valide")
    nationality = models.CharField(max_length=255, help_text="Nationalité de l'utilisateur")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Génère un user_id unique avant de sauvegarder l'utilisateur.
        """
        if not self.user_id:
            newid = generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid = generate_user_id()
            self.user_id = newid
        super().save(*args, **kwargs)


# -------------------------------
# Organizing Committee Model
# -------------------------------
class OrganizingCommittee(models.Model):
    """
    Modèle représentant un membre du comité organisateur pour une conférence.
    """
    COMMITTEE_ROLE_CHOICES = [
        ("chair", "Chair"),
        ("co-chair", "Co-chair"),
        ("member", "Member"),
    ]
    commitee_role = models.CharField(
        max_length=255, choices=COMMITTEE_ROLE_CHOICES,
        help_text="Rôle du membre dans le comité"
    )

    join_date = models.DateField(help_text="Date de début dans le comité")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Relations
    user = models.ForeignKey(
        "UserApp.User", on_delete=models.CASCADE, related_name="committees",
        help_text="Utilisateur membre du comité"
    )
    conference = models.ForeignKey(
        "ConferenceApp.Conference", on_delete=models.CASCADE, related_name="committees",
        help_text="Conférence associée au comité"
    )
