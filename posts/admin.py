from django.contrib import admin
from .models import Posts, Images, Categories

@admin.register(Posts)
class PosttAdmin(admin.ModelAdmin):
    model = Posts
    list_display = ("title", "description", "date_publication", "user")
    list_filter = ("title", "date_publication", "user")
    search_fields = ("title", "user__username")  

@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    model = Images
    list_display = ("image", "post")
    list_filter = ("post",) 
    search_fields = ("post__title",) 

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)

