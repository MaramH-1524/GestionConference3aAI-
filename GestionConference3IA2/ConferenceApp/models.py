from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
import uuid

# -------------------------------
# Utility function
# -------------------------------
def generate_submission_id():
    """
    Génère un identifiant unique pour une soumission,
    sous la forme SUBXXXXXXXX (8 caractères hexadécimaux).
    """
    return "SUB" + uuid.uuid4().hex[:8].upper()


# -------------------------------
# Conference Model
# -------------------------------
class Conference(models.Model):
    """
    Modèle représentant une conférence.
    """
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text="Nom de la conférence")
    
    THEME = [
        ("IA", "Computer science & AI"),
        ("SE", "Science & Engineering"),
        ("SC", "Social sciences"),
    ]
    theme = models.CharField(max_length=255, choices=THEME, help_text="Thème de la conférence")
    
    location = models.CharField(max_length=50, help_text="Lieu de la conférence")
    
    description = models.TextField(
        validators=[MaxLengthValidator(30, "Vous avez dépassé la limite de mots autorisés")],
        help_text="Description courte de la conférence (max 30 caractères)"
    )
    
    start_date = models.DateField(help_text="Date de début")
    end_date = models.DateField(help_text="Date de fin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Affiche un résumé lisible de la conférence.
        """
        return f"Conférence : {self.name}"

    def clean(self):
        """
        Validation personnalisée : la date de début doit être antérieure à la date de fin.
        """
        if self.start_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")


# -------------------------------
# Submission Model
# -------------------------------
class Submission(models.Model):
    """
    Modèle représentant une soumission pour une conférence.
    """
    submission_id = models.CharField(
        max_length=255, primary_key=True, unique=True, editable=False,
        help_text="ID unique généré automatiquement"
    )
    title = models.CharField(max_length=50, help_text="Titre de la soumission")
    abstract = models.TextField(help_text="Résumé de la soumission")
    keywords = models.TextField(help_text="Mots-clés séparés par des virgules")
    
    paper = models.FileField(upload_to="papers/", help_text="Fichier PDF de la soumission")
    
    STATUS = [
        ("submitted", "Submitted"),
        ("under review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=50, choices=STATUS, help_text="Statut de la soumission")
    payed = models.BooleanField(default=False, help_text="Indique si la soumission est payée")
    
    submission_date = models.DateField(auto_now_add=True, help_text="Date de soumission")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    # Relations
    user = models.ForeignKey(
        "UserApp.User", on_delete=models.CASCADE, related_name="submissions",
        help_text="Utilisateur ayant soumis"
    )
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, related_name="submissions",
        help_text="Conférence associée à la soumission"
    )

    def save(self, *args, **kwargs):
        """
        Génère un submission_id unique avant de sauvegarder.
        """
        if not self.submission_id:
            newid = generate_submission_id()
            # Vérifie que l'ID est unique
            while Submission.objects.filter(submission_id=newid).exists():
                newid = generate_submission_id()
            self.submission_id = newid
        super().save(*args, **kwargs)
