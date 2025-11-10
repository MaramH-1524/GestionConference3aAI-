from django.contrib import admin
from .models import Conference,Submission,OrganozingCommitee
# Register your models here.
admin.site.site_title="Gestion CConference 25/26"
admin.site.site_header="Gestion Conference"
admin.site.index_title="django App Conference"
#admin.site.register(Conference)
admin.site.register(OrganozingCommitee)
#PERSONALISATION 
#ajouter au formulaire de conference une partie pour la submission pour etre plus facile 
#class SubmissionInline(admin.TabularInline):sous forme de tableau 
class SubmissionInline(admin.StackedInline):
    model= Submission
    extra=1
    readonly_fields=("submission_date",)
    
    
@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display=("name", "theme", "start_date", "end_date", "duration")
    #on veux faire l'odre des conferences selon start_date , l'ordering prend des tuples ,c'est pouquoi on a mis ,
    ordering=("start_date",)
    list_filter=("theme",)
    search_fields=("description","name", )
    date_hierarchy='start_date'
    fieldsets=(
        ("information génèrale",{
            "fields":("conference_id","name","theme","description")}),
        ("logistiques info",{
            "fields":("location","start_date", "end_date")
        })
    )
    #cela nous permet d'afficher l'id , car sinon il va nous afficher une erreur , puisque c'est un primary key donc cette ligne me permet just de read it , affichage c'est tout 
    readonly_fields=("conference_id",)
    def duration(self, objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date-objet.start_date)
        return"RAS"
    duration.short_description="Duration(days)"
    #INLINES 
    inlines=[SubmissionInline]

@admin.register(Submission)
class AdminSubmissionModel(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "user",
        "conference",
        "submission_date",
        "payed",
        "short_abstract",
    )
    list_filter = ("status", "payed", "conference", "submission_date")
    search_fields = ("title", "keywords", "user__username")
    list_editable = ("status", "payed")
    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstarct", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )
    readonly_fields = ("submission_id", "submission_date")

    def short_abstract(self, obj):
        return (obj.abstarct[:50] + "...") if len(obj.abstarct) > 50 else obj.abstarct
    short_abstract.short_description = "Résumé court"
    # Action pour marquer plusieurs soumissions comme payées
    def mark_as_payed(self, request, queryset):
      updated = queryset.update(payed=True)
      self.message_user(request, f"{updated} soumission(s) marquée(s) comme payée(s).")
    mark_as_payed.short_description = "Marquer les soumissions sélectionnées comme payées"


    def accept_submissions(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"
    
    actions = [mark_as_payed, accept_submissions]
