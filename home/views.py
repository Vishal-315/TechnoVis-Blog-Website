from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    return render (request,'home/home.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"please fill the form correctly")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"your message is successfully sent")

    return render (request,'home/contact.html')

def about(request):    
    return render (request,'home/about.html')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allposts=Post.objects.none()
    else:
        allpoststitle=Post.objects.filter(title__icontains=query)
        allpostsblog=Post.objects.filter(content__icontains=query)
        allposts=allpoststitle.union(allpostsblog)
    if allposts.count() == 0:
        messages.error(request,"NO search is found")
    params={"allposts" : allposts, "query" : query}
    return render(request,'home/search.html',params)

def handlesignup(request):
    if request.method=='POST':
        #get the post parameters
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #check for errorneous imput
        if len(username)>10:
            messages.error(request,"username must be under 10 characters")
            return redirect('home')
        if pass1!=pass2:
            messages.error(request,"passwords do not match")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"username should only contain letters and numbers")
            return redirect('home')

        #create the user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"your iCoder account has successfully created")
        return redirect('home')

    else:
        return HttpResponse('404-Not Found')

def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpass']
        user=authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials please try again")

    return HttpResponse('404-Not Found')    

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('home')