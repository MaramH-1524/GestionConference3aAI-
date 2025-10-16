from django.db import models
from django.utils import timezone
import random
import string
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator
# Create your models here.
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,validators=[RegexValidator(r'^[a-zA-Z\s]+$',  'Le titre de la conférence ne doit contenir que des lettres et des espaces (pas de chiffres ou caractères spéciaux).')])
    THEME=[
        ("IA","Computer science and Artificial Intelligence"),
        ("SE","Science and Engineering"),
        ("SC"," Social Sciences & Education"),
        ("IT","Interdiscplinary Themes")
        ]
    
    theme=models.CharField(max_length=255, choices=THEME)
    location=models.CharField(max_length=50)
    description = models.TextField(
    validators=[MaxLengthValidator(500, "Vous avez dépassé la limite")],
    null=True, 
    blank=True
)

    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def clean(self):
      #on doit tester qu'il sont present , c a d je les remplis 
      if self.start_date and self.end_date:
        if self.start_date>=self.end_date:
            raise ValidationError("la date de debut doit etre inferieur a la date de la fin")
def generate_sub_id():
    prefix="SUB"
    random_part=''.join(random.choices(string.ascii_uppercase, k=8))
    return prefix+ random_part

class Submission(models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True, unique=True, default=generate_sub_id, editable=False)
    title=models.TextField()
    abstarct=models.TextField()
    keywords = models.TextField(help_text="separer les mots_cles par des virgules ")
    paper=models.FileField(upload_to="papers/",validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    STATUS = [
    ("submitted", "Submitted"),
    ("under_review", "Under Review"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected"),
]

    status=models.CharField(max_length=50, choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date = models.DateField(default=timezone.now)
    
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    conference=models.ForeignKey("Conference",on_delete=models.CASCADE,related_name="submissions")
    
    def clean(self):
        errors = {}
        if self.conference_id:
            conf=self.conference
            if self.submission_date > conf.start_date:
                raise ValidationError("YOU CAN NOT SUBMIT AFTER THE CONFERENCE HAS STARTED")
      
        if self.keywords:
            """solution avec la boucle for 
            keyword_list=[]
            for i in self.keywords.split(','):
             k=k.strip()
             if k:
              keywords_list.append(k);
        
            """
            #on met d'abord les mots dans les listes avec les espaces puis on eliminer les chaines vides(strip) ,et voila 
            keyword_list = [k.strip() for k in self.keywords.split(',') if k.strip()]
            if len(keyword_list) > 10:
                errors['keywords'] = ValidationError("Maximum 10 mots-clés autorisés.")

        
        if self.conference and self.conference.start_date <= timezone.now().date():
            errors['conference'] = ValidationError(
                "La soumission ne peut être faite que pour une conférence à venir."
            )

        if self.user_id:
            today = timezone.now().date()
            count_today = Submission.objects.filter(
                user=self.user,
                submission_date=today
            ).exclude(pk=self.pk).count()
            if count_today >= 3:
                errors['user'] = ValidationError(
                    "Vous avez déjà soumis 3 conférences aujourd’hui."
                )

        if errors:
            raise ValidationError(errors)
        

    def __str__(self):
        return f"{self.submission_id} - {self.title}"
    
class OrganozingCommitee(models.Model) :
    organizingcommitee_id=models.CharField(max_length=255,primary_key=True, unique=True)
    ROLE=[
("chair","chair"),
("co_chair","co_chair"),
("member","member")    ,    
    ]
    commitee_role=models.CharField(max_length=50, choices=ROLE )
    date_joined=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="committees")
    conference=models.ForeignKey("Conference",on_delete=models.CASCADE,related_name="committees")
    
    


    

