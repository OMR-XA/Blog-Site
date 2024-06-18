from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from Reg.views import (NewBlogPostPage, UpdateBlogPost, UpdateUserProfile,
                       deletepage, myblogpostspage, scrollpage, viewblogpost,
                       userpage, search, settingspage, homepage)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('authentication.urls')),  # Assuming authentication.urls is correctly defined

    # Your custom views
    path('NewBlogPost/', NewBlogPostPage, name='new_blog_post'),
    path('', homepage, name='homepage'),
    path('update-<slug>/', UpdateBlogPost, name='update_blog_post'),
    path("update/", UpdateUserProfile, name='update_user_profile'),
    path('delete/', deletepage, name='delete_page'),
    path('myblogposts/', myblogpostspage, name='my_blog_posts'),
    path("scroll/", scrollpage, name='scrollpage'),  # Make sure the name matches here
    path("view-<slug:slug>", viewblogpost, name='view_blog_post'),  # Adjusted for slug parameter
    path('look-<username>/', userpage, name='user_page'),
    path("search/", search, name='search'),
    path("mysettings/", settingspage, name='settings_page'),
    # re_path(r'^.*$', homepage)
]

# Serve static and media files during development
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


