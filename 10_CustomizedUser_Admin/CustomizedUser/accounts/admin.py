from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm
from .models import Students, Schools

User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm # ユーザ編集画面でつかうForm
    add_form = UserCreationForm # ユーザ作成画面

    # 一覧画面で表示する
    list_display = ('username', 'email', 'is_staff')

    # ユーザ編集画面で表示する要素
    fieldsets = (
        ('ユーザ情報', {'fields': ('username', 'email', 'password', 'website', 'picture')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        ('ユーザ情報', {
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
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
class SchoolsAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')

    def student_count(self, obj):
        # print(type(obj))
        # print(dir(obj))
        count = obj.students_set.count()
        return count
    
    student_count.short_description = '生徒数'