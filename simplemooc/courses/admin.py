from django.contrib import admin
from simplemooc.accounts.models import User
from .models import Course, Announcements, Comments, Enrollment, Lesson, Material

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'startDate', 'createdAt']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}


class MaterialInlineAdmin(admin.StackedInline):
    model = Material

class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description', 'number']
    list_filter = ['created_at']

    inlines = [MaterialInlineAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcements, Comments, User,])
admin.site.register(Lesson, LessonAdmin)