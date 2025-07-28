from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path("", views.home, name="home"),

    #Once logged in brings to the home pagev
    path("accounts/profile/", views.profile_view, name="profile"),

    #When logged out, redirects to home page
    path("accounts/logout/", LogoutView.as_view(next_page="/"), name="logout"),

    #Path for about us page
    path("about/", views.about, name="about"),

    #Path for about us page
    path("pricing/", views.pricing, name="pricing"),

    path("register/", views.register, name="register"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("transactions/", views.transactions_view, name="transactions"),


    path("budget/", views.budget, name="budget"),

    path("categories/", views.categories, name="categories"),

    path("goals/", views.goals, name="goals"),

    path('transactions/edit/<int:id>/', views.edit_transaction, name='edit_transaction'),

    path('transactions/delete/<int:id>/', views.delete_transaction, name='delete_transaction')


]