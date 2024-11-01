from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import Students, Schools

User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm # 編集画面
    add_form = UserCreationForm # ユーザー作成画面
    # 一覧で表示知るフィールド
    list_display = ('username', 'email', 'is_staff')
    
    fieldsets = (
        ('ユーザー情報', {
                'fields': ('username', 'email', 'password', 'website', 'picture')
            }),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )
    add_fieldsets = (
        (
            'ユーザー情報', {
                'fields': ('username', 'email', 'password1', 'password2'),
            }
        ),
    )
    

admin.site.register(User, CustomizeUserAdmin)
# admin.site.register(Students)
# admin.site.register(Schools)

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    fields = ('name', 'score', 'age', 'school')
    list_display = ('id', 'name', 'age', 'score', 'school')
    list_display_links = ('id',)
    search_fields = ('name', 'age')
    list_filter = ('name', 'age', 'score', 'school')
    list_editable = ('name', 'age', 'score', 'school')

@admin.register(Schools)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')
    
    def student_count(self, obj):
        count = obj.students.count()
        return count
    
    student_count.short_description = '生徒数'