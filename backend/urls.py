from django.urls import path

from . import views

urlpatterns = [
    path("user/<str:email>", views.get_user, name="user"),
    path("users", views.users, name="users"),
    path("", views.plan_expire, name=""),
    path("plans", views.plans, name="plans"),
    path("plan/<str:name>", views.get_plan, name="plan"),
    path("addvip", views.add_to_plan, name="addvip"),
    path("delvip", views.plan_expire, name="delvip"),
    path("freeinplay", views.freeinplay, name="freeinplay"),
    path("vipodd/<str:category>", views.getvipodds, name="vipodd"),
    path("vipcat", views.getvipcat, name="vipcat"),
    path("freecat", views.getfreecat, name="freecat"),
    path("botd", views.get_betoftheday, name="botd"),
    path("freepred", views.get_freepredictions, name="freepred"),
    path("results", views.get_recent_results, name="results"),
    path("gamebycat/<str:category>", views.games_by_category, name="gamebycat"),
     path("password/reset/confirm/<uidb64>/<token>", views.password_reset_confirm, name="password-reset-confirm"),
]



