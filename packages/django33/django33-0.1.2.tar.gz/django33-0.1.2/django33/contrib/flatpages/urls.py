from django33.contrib.flatpages import views
from django33.urls import path

urlpatterns = [
    path("<path:url>", views.flatpage, name="django33.contrib.flatpages.views.flatpage"),
]
