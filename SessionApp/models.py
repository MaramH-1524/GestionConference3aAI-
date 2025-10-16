

from django.db import models
from ConferenceApp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time = models.TimeField()
    room=models.CharField(max_length=255, validators=[RegexValidator(r'^[A-Za-z0-9\s]+$', "le nom de la salle ne doit contenir que des lettres et des chiffres pas de caractere speciaux")])
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    #conference=models.ForeignKey("ConferenceApp.Conference")ou bien 
    conference=models.ForeignKey(Conference, on_delete=models.CASCADE,
                                 related_name="sessions")
    def clean(self):
     errors = {}

    #Vérifie d’abord que la FK existe dans la base
     if self.conference_id and self.session_day:
        conf = Conference.objects.filter(pk=self.conference_id).first()
        if conf and conf.start_date and conf.end_date:
            if not (conf.start_date <= self.session_day <= conf.end_date):
                errors['session_day'] = ValidationError(
                    "La date de la session doit être comprise entre les dates de la conférence."
                )

     if self.start_time and self.end_time:
        if self.end_time <= self.start_time:
            errors['end_time'] = ValidationError(
                "L’heure de fin doit être supérieure à l’heure de début."
            )

     if errors:
        raise ValidationError(errors)

