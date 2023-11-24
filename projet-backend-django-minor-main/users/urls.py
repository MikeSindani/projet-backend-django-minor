from django.urls import path
from .views import GetUserDetailsView

urlpatterns = [
       path('get-user-details/', GetUserDetailsView.as_view()),
       # other urls...
   ]
