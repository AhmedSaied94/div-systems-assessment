from .views import UserDetailsView, login
from django.urls import path



urlpatterns = [
    path('signup/', UserDetailsView.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('status/', UserDetailsView.as_view(), name='status')
]
