from datetime import date, timezone
import datetime
from django.core import serializers
from django.http import HttpResponse
from django import views
from django.contrib import auth
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User, Plan, VipOdd, Categorie, Game, FreeInplayOdd, VipGame, FreeCategorie, RecentVipResult, FreePrediction, DailyBet

from django.contrib.auth import authenticate, login, logout
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status
import json
import jsonpickle
from json import JSONEncoder
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseBadRequest




class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        
        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
        return serializer_class(*args, **kwargs)
    
    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
  
  # Get user by email  
@api_view()
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def get_user(request, email):
    user = User.objects.filter(email =email).values('id','first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_vip')
    if len(user) == 0:
        raise Exception("User Not Found!")
    return Response({"user": user})




# Get All users
@api_view()
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def users(request):
    all_users = User.objects.all().values('id','first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_vip')
    return Response({"users": all_users})

    
    
    
# Get all plans
@api_view()
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def plans(request):
    all_plans = Plan.objects.all().values('id', 'name', 'price', 'duration' )
    return Response({"plans": all_plans})



#Get plan by name
@api_view()
@renderer_classes([JSONRenderer])
@permission_classes([AllowAny])
def get_plan(request, name):
    plan = Plan.objects.filter(name=name).values('id', 'name', 'price', 'duration')
    return Response({"plan": plan})


# #Update user to Vip
# @api_view(['GET', 'POST'])
# @renderer_classes([JSONRenderer])
# @permission_classes([IsAuthenticated])
# def add_to_vip(request, email):
#     if request.method == 'POST':
#         user = User.objects.filter(email =email).values('id','first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_vip')
#         if len(request.body) > 0:
#             if user.values('is_vip') == False:
#                 user.update(is_vip = True)
#             else:
#                 return Response('Already subscribed to VIP')
#     return Response(200)



#add user to a plan
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def add_to_plan(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get("email", "")
        plan = data.get("plan", "")
        day_subscribed = datetime.date.today()
        user = User.objects.get(email = email)
        plan_sub =  Plan.objects.get(name = plan)
        if len(request.body) > 0:
            if user.is_vip == False:
                user.is_vip = True
                user.plan_sub = plan_sub
                user.day_subscribed = day_subscribed
                user.save(update_fields=['is_vip','plan_sub','day_subscribed'])
            else:
                return Response(f'Already Subscribed to {plan}')
    return Response(f"{email} subscribed to {plan}")
    


#remove user from a plan
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def plan_expire(request):
    user = request.user 
    email = user.email
    plan = user.plan_sub
    if user.day_subscribed + plan.duration >= datetime.date.today():
        if user.is_vip == True:
            user.is_vip = False
            user.plan_sub = None
            user.day_subscribed = None
            user.save(update_fields=['is_vip','plan_sub', 'day_subscribed'])
        else:
            return Response(f'User Not Subscribed To {plan}')
    return Response(f"{email} removed from {plan}")
    
    
    
# Get all free inplay tips
@api_view()
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def freeinplay(request):
    all_freepred = FreeInplayOdd.objects.all().values('id', 'match', 'prediction', 'time').order_by('-time')
    return Response({"Freeinplaygames": all_freepred})



# vip GET and POST       
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer]) 
@permission_classes([IsAuthenticated])
def getvipodds(request, category):
    if request.method == 'GET':
        vip_games = VipGame.objects.filter(category__category_name=category).values('id', 'match', 'Prediction','odd', 'time').order_by('-time')
        vip_odds = VipOdd.objects.filter(category__category_name=category).values('id','games','total_odds','category__category_name','betking_code','onexbet_code','twentytwobet_code','sportybet_code','bet9ja_code','Helabet_code', 'date').order_by('-date')
        return Response({"vipgames":vip_games ,"vipodds": vip_odds})
    
    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     games = data.get("games", "")
    #     total_odds = data.get("total_odds", "")
    #     category = data.get("category", "")
    #     betking_code = data.get("betking_code", "")
    #     onexbet_code = data.get("onexbet_code", "")
    #     twentytwobet_code = data.get("twentytwobet_code", "")
    #     sportybet_code = data.get("sportybet_code", "")
    #     bet9ja_code = data.get("bet9ja_code", "")
    #     Helabet_code = data.get("Helabet_code", "")
    #     date = data.get("date", "")
    #     model = Vip_Odds(games, total_odds, betking_code,onexbet_code,twentytwobet_code,sportybet_code,bet9ja_code,Helabet_code, date)
    #     model.save()
    #     return Response(f"Games added to {category}")
    
    
#get VIP categories    
    
@api_view(['GET'])
@renderer_classes([JSONRenderer]) 
@permission_classes([IsAuthenticated])
def getvipcat(request):
    cat = Categorie.objects.all().values('id','category_name')
    return Response({"categories": cat})



@api_view(['GET'])
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def getfreecat(request):
    cat = FreeCategorie.objects.all().values('id','category_name')
    return Response({"categories": cat})



        
        
# class GameSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Game
#         fields = '__all__'
        
        

# class DailybetSerializer(serializers.ModelSerializer):
#     games = GameSerializer(many=True)
#     class Meta:
#         model = DailyBet
#         fields = '__all__'



# Get bet of the day

@api_view(['GET'])
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def get_betoftheday(request):
    # game = DailybetSerializer().data
    model = DailyBet.objects.all()
    ser_game = serializers.serialize('json', model)
    des_game = serializers.deserialize('json' , ser_game)
    
    
    games = []
    
    for obj in des_game:
        instance = obj.object
        games.append([{"id": instance.id ,"time":instance.time,"matches":[{"id":game.id, "league":game.league, "match":game.match, "prediction":game.prediction} for game in instance.games.all()]}]) # Get games values from deserialized data
        

    
    
    return Response({"betoftheday": games})


 

# Get free prediction
@api_view(['GET'])
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def get_freepredictions(request):
    model = FreePrediction.objects.all()
    ser_game = serializers.serialize('json', model)
    des_game = serializers.deserialize('json' , ser_game)
    
    
    games = []
    
    for obj in des_game:
        instance = obj.object
        games.append([{"id": instance.id ,"time":instance.time,"matches":[{"id":game.id, "league":game.league, "match":game.match, "prediction":game.prediction} for game in instance.games.all()]}])
        
        
    return Response({"games": games})



# Get Recent Results
@api_view(['GET'])
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def get_recent_results(request):
     results= RecentVipResult.objects.all().order_by('day')[:5].values('id', 'status', 'day')
     return Response({"results": results})
 
 

#Get predictions by category

@api_view(['GET'])
@renderer_classes([JSONRenderer]) 
@permission_classes([AllowAny])
def games_by_category(request, category):
    games  =  Game.objects.filter(category__category_name=category).values('id', 'category__category_name', 'prediction', 'match','league')
    
    return Response({"games": games})











User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Password reset successful!")
        else:
            form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        return HttpResponseBadRequest("Invalid password reset link.")



















        
        
        









    