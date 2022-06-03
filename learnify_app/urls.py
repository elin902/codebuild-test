from django.urls import path
from . import views


app_name = 'learnify_app'
urlpatterns = [
    # Strona główna.
    path('', views.index, name='index'),
    # Strona tematów
    path('topics/', views.topics, name='topics'),
    # Strona szczegółowa dotycząca pojedynczego tematu.
    path('topics/(<int:topic_id>)/', views.topic, name='topic'),
    # Strona do dodawania nowych tematów
    path('new_topic/', views.new_topic, name='new_topic'),
    # Strona przeznaczona do dodawania nowego wpisu.
    path('new_entry/<int:topic_id>)/', views.new_entry, name='new_entry'),
    # Strona przeznaczona do edycji wpisów
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # delete entry
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),

]
