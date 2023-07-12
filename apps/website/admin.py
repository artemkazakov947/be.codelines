from django.contrib import admin

from apps.website.helpers import send_new_post_notification
from apps.website.models import (Role,
                                 Employee,
                                 Skill,
                                 Job,
                                 Post,
                                 Service,
                                 EmailForPostNotification)

admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(Job)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        send_new_post_notification(obj)
        super().save_model(request, obj, form, change)


admin.site.register(Service)
admin.site.register(EmailForPostNotification)
