from django.contrib import admin
from .models import User,Plan, Categorie, Game, VipOdd, FreeInplayOdd, FreeCategorie, VipGame, RecentVipResult,SubRecord, FreePrediction, DailyBet

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name',]


admin.site.register(User, UserAdmin)
admin.site.register(Plan)
admin.site.register(Categorie)
admin.site.register(Game)
admin.site.register(VipOdd)
admin.site.register(FreeCategorie)
admin.site.register(VipGame)
admin.site.register(FreeInplayOdd)
admin.site.register(RecentVipResult)
admin.site.register(FreePrediction)
admin.site.register(DailyBet)
# admin.site.register(SubRecord)



