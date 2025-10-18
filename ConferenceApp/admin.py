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

@admin.action(description="marquer les soumissions comme payés")
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)
@admin.action
def mark_as_accepted(m,rq,q):
    q.update(status="accepted") 


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display =("title", "status", "payed","submission_date")
    fieldsets =(
        ("Information general", {
            "fields":("title","abstract","keywords")
        }),
        ("document", {
            "fields":("paper","user","conference")
        }),
        ("Status", {
            "fields":("status","payed")
        })
    )
    actions =[mark_as_payed,mark_as_accepted]