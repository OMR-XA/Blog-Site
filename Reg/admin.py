from django.contrib import admin

from authentication.models import (UserProfile,BlogPost,
                                   Comment,UserSettings)

admin.site.register(UserProfile)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(UserSettings)

# Register your models here.
