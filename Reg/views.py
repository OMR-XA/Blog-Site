from django.shortcuts import (render,redirect,get_object_or_404)
from authentication.models import BlogPost,UserProfile,Comment,UserSettings
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .nudedetector import check_image_safety, save_temp_image
import os
import re


def scrollpage(request):
    # Adjust the query to match your models' field names and choices
    posts = BlogPost.objects.filter(
        Q(publish=True) & (
            Q(user__usersettings__posts_visibility="public") & (
                Q(user__usersettings__account_privacy="public")
            )
        )
    )
    
    comments = None  # Initialize comments to None to avoid reference before assignment error

    if request.method == "POST":
        postcre = re.compile(r"postc(\d+)")
        commentpostre = re.compile(r"viewpostc(\d+)")
        
        for key in request.POST.keys():
            match = postcre.match(key)
            match2 = commentpostre.match(key)
            
            if match:
                post_id = match.group(1)
                comment_content = request.POST.get("comment-data")
                
                if comment_content and request.user.is_authenticated:
                    blog_post = get_object_or_404(BlogPost, id=post_id)
                    pic = request.FILES.get("pic")
                    
                    if pic:
                        temp_image_path = save_temp_image(pic)
                        pic_result = check_image_safety(temp_image_path)
                        os.remove(temp_image_path)  # Delete the temp file after checking

                        if pic_result == "Not Safe":
                            context = {"Posts": posts, "comments": comments,"message":"Pic not safe"}
                            return render(request, "Scroll.html", context)

                        else:
                            new_comment = Comment(
                                bp=blog_post,
                                user=request.user,
                                content=comment_content,
                                date=timezone.now().date(),
                                time=timezone.now().time(),
                                pic=pic
                            )
                            new_comment.save()
                            messages.success(request, "Comment posted successfully with photo")
                    else:
                        new_comment = Comment(
                            bp=blog_post,
                            user=request.user,
                            content=comment_content,
                            date=timezone.now().date(),
                            time=timezone.now().time()
                        )
                        new_comment.save()
                        messages.success(request, "Comment posted successfully")
                else:
                    if not request.user.is_authenticated:
                        messages.error(request, "You must be logged in to comment")
                        return redirect("/signup")
                    else:
                        messages.error(request, "Comment content cannot be empty")
            
            elif match2:
                post_id = match2.group(1)
                comments = Comment.objects.filter(bp_id=post_id)
                break  # Exit loop after handling the first matched key

    context = {"Posts": posts, "comments": comments}
    return render(request, "Scroll.html", context)

def search(request):
    if request.method == "POST":
        search_query = request.POST.get("search")

        # Update the query to use icontains for more flexible matching
        posts = BlogPost.objects.filter(
            Q(slug__icontains=search_query) | 
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query), 
            publish=True
        )
        users = UserProfile.objects.filter(
            Q(username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
        results = [users,posts]
        
        if not posts and not users:
            context = {"result": "No search match"}
        else:
            context = {"result": results}
        
        return render(request, "Search.html", context)

    return render(request, "Search.html")

        
        

def userpage(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
        posts = BlogPost.objects.filter(user = user_profile.user)
        context = {"user": user_profile.user, "user": user_profile, "posts": posts}
        return render(request, "userprofile.html", context)
    except ObjectDoesNotExist:
        return render(request, "userprofile.html", {"username": username})



def viewblogpost(request, slug):
    blogpost = BlogPost.objects.get(slug=slug)
    comments = Comment.objects.filter(bp=blogpost)
    if blogpost:
        context = {"post": blogpost,"comments":comments}
        if request.method == "POST" :
            if "postc" in request.POST:
                commentdata = request.POST.get("commentdata")
                comment = Comment(bp=blogpost, user=request.user, content=commentdata)
                comment.save()           
    else:
        context = {"post_not_found": True, "slug": slug}
    return render(request, "viewpost.html",context)



def homepage(request):
    if request.user.is_authenticated:
        return redirect("/scroll")
    return render(request, "home.html")


def myblogpostspage(request):
    Blogposts = BlogPost.objects.filter(user = request.user)
    context = {"Blogposts": Blogposts}
    return render(request, "myblogposts.html", context)


def NewBlogPostPage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        slug = request.POST.get("slug")
        pic = request.FILES.get("image")

        if not title or not content or not slug:
            return render(request, 'NBP.html', {"message": "Title, content, and slug are required."})

        publish = "send" in request.POST

        if pic:
            temp_image_path = save_temp_image(pic)
            pic_result = check_image_safety(temp_image_path)
            os.remove(temp_image_path)  # Delete the temp file after checking

            if pic_result == "Not Safe":
                return render(request, 'NBP.html', {"message": "Picture Not Safe"})

            bp = BlogPost(
                user=request.user,
                title=title,
                content=content,
                slug=slug,
                pic=pic,
                publish=publish
            )
        else:
            bp = BlogPost(
                user=request.user,
                title=title,
                content=content,
                slug=slug,
                publish=publish
            )

        bp.save()

        return render(request, 'NBP.html', {"message": "Post saved successfully." if publish else "Draft saved successfully."})

    return render(request, 'NBP.html')


def UpdateBlogPost(request, slug):
    try:
        obj = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return render(request, 'updatebp.html', {"message": "Post not found."})
    
    if request.method == "POST":
        if "update" in request.POST or "sad" in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            slug = request.POST.get('slug')
            pic = request.FILES.get('pic')
            
            # Handle image upload and safety check
            if pic:
                temp_image_path = save_temp_image(pic)
                pic_result = check_image_safety(temp_image_path)
                os.remove(temp_image_path)  # Clean up temporary image file
                
                if pic_result == "Not Safe":
                    return render(request, 'updatebp.html', {"obj": obj, "error_message": "Picture Not Safe"})
                else:
                    obj.pic = pic
            
            obj.title = title
            obj.content = content
            obj.slug = slug
            obj.publish = True if "update" in request.POST else False
            obj.save()
            
            if "update" in request.POST:
                message = "Post updated successfully."
            else:
                message = "Post saved as draft."
            return render(request, 'updatebp.html', {"obj": obj, "message": message})
        
        elif "delete" in request.POST:
            obj.delete()
            return redirect("/")
    
    # Default context if not a POST request or "sad" is not in request.POST
    context = {"obj": obj}
    return render(request, "updatebp.html", context)


def UpdateUserProfile(request):
    obj = UserProfile.objects.get(user=request.user)
    
    if request.method == "POST":
        if "update" in request.POST:
            name1 = request.POST.get("first_name")
            name2 = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = request.POST.get("username")
            pic = request.FILES.get("pic")

            if UserProfile.objects.filter(user__email=email).exclude(user=request.user).exists():
                return render(request, "update.html", {"obj": obj, "message": "Email already exists"})
            elif UserProfile.objects.filter(username=username).exclude(user=request.user).exists():
                return render(request, "update.html", {"obj": obj, "message": "Username already exists"})
            else:
                if pic:
                    temp_image_path = save_temp_image(pic)
                    pic_result = check_image_safety(temp_image_path)
                    os.remove(temp_image_path)  # Clean up temporary image file
                    
                    if pic_result == "Not Safe":
                        return render(request, 'update.html', {"obj": obj, "error_message": "Picture Not Safe"})
                    else:
                        obj.pic = pic

                obj.user.first_name = name1
                obj.user.last_name = name2
                obj.user.email = email
                obj.username = username
                if password:  # Ensure password is provided
                    obj.user.set_password(password)  # Use set_password to hash the password
                obj.user.save()
                obj.save()
                return render(request, "update.html", {"obj": obj, "message2": "Profile updated successfully"})

        elif "delete" in request.POST:
            return redirect("/delete")  # Redirect to home or any appropriate page

        elif "logout" in request.POST:
            logout(request)
            return redirect("/signup")  # Redirect to home or login page
    
    return render(request, "update.html", {"obj": obj})

def deletepage(request):
    error_message = None  # Initialize error message

    if request.method == "POST":
        entered_password = request.POST.get("password")

        if entered_password == request.user.password:
            # Correct credentials: Delete the user and redirect
            
            userp = UserProfile.objects.get(user=request.user)
            userp.delete()
            userp.user.delete()
            return redirect("/")
        else:

            error_message = "Wrong password. Please try again."

    return render(request, "delete.html", {"error_message": error_message})



def settingspage(request):
    if request.user.is_authenticated:
        us, created = UserSettings.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            # Get boolean values from checkboxes
            us.email_notifications = 'email_notifications' in request.POST
            us.notifications = 'notifications' in request.POST
            
            # Get other form values
            us.posts_visibility = request.POST.get('posts_visibility')
            us.account_privacy = request.POST.get('account_privacy')
            us.theme = request.POST.get('theme')
            us.language = request.POST.get('language')
        
            us.save()
            
        context = {"us": us}
        return render(request, "settings.html", context)
    else:
        return redirect('/signup')  # Redirect to login if not authenticated

