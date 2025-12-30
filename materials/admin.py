from django.contrib import admin

from materials.models import LessonModel, CourseModel, Subscription


# Register your models here.


@admin.register(CourseModel)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(LessonModel)
class LessonAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass