from django.contrib import admin
from .models import Post, Comment, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', "status")
    list_editable = ('status',) #указуємо поля які хочемо змнювати з загальної панелі
    list_filter = ('title', 'author', 'status')#фільтрація
    search_fields = ('title',) #поле пошуку
    ordering = ('-publish', "status")
    date_hierarchy = 'publish' #ієрархія дат
    prepopulated_fields = {'slug': ('title',)} #флрмуємо слаг автоматично


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'active')
    list_filter = ('active', 'post')
    list_editable = ('active',)





admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
