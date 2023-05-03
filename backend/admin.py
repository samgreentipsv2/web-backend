from django.contrib import admin
from .models import User,Plan, Categories, Game, Vip_Odds, Free_Inplay_Odds, FreeCategories, Vip_games, Recent_vip_results

# Register your models here.


admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Categories)
admin.site.register(Game)
admin.site.register(Vip_Odds)
admin.site.register(FreeCategories)
admin.site.register(Vip_games)
admin.site.register(Free_Inplay_Odds)
admin.site.register(Recent_vip_results)