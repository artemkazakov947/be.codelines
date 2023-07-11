from django.contrib import admin

from apps.website.models import (Role,
                                 Employee,
                                 Skill,
                                 Job,
                                 Post,
                                 Service)

admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Post)
admin.site.register(Service)
