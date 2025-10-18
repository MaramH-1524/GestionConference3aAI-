from django.urls import path
from .views import ConferenceList, ConferenceDetails, ConferenceCreate

urlpatterns = [
    path("liste/", ConferenceList.as_view(), name="liste_conferences"),
    path("details/<int:pk>/", ConferenceDetails.as_view(), name="conference_details"),
    path("add/", ConferenceCreate.as_view(), name="conference_add"),
]
