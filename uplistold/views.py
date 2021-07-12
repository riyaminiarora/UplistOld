from django.shortcuts import render,redirect
from django.contrib.auth.models import  User
from django.contrib.auth import authenticate,login,logout
from .models import Category,Location,Postad,UserProfile,Message
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        user=User.objects.create_user(username,email,password)
        udata=UserProfile(user=user)
        udata.save()
        return redirect('signin')
    else:
        return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('profile')
        else:
            return render(request, 'signin.html',{"error":"Invalid Username/Password"})
    else:
        return render(request, 'signin.html')

@login_required(login_url='/signin')
def profile(request):
    if request.method == 'POST':
        info = request.POST.get('info')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        user_image = request.FILES.get('profile_pic')
        if user_image:
            user_image = request.FILES.get('profile_pic')
        else:
            user_image = "images/profile/default.png"
        uobj=UserProfile.objects.get(user=request.user)
        uobj.first_name=fname
        uobj.last_name=lname
        uobj.city=city
        uobj.phone_no=phone
        uobj.info=info
        uobj.profile_pic=user_image
        uobj.save()
        udata = UserProfile.objects.get(user=request.user)
        return render(request, 'profile.html', {'udata': udata})


    else:
        udata=UserProfile.objects.get(user=request.user)
        return render(request, 'profile.html',{'udata':udata})

def addetail(request,id):
    ad_data=Postad.objects.get(pk=id)
    relatedads=Postad.objects.filter(ad_category=ad_data.ad_category)
    return render(request, 'addetail.html',{'ad':ad_data,'relatedads':relatedads})

@login_required(login_url='/signin')
def myads(request):
    uname=request.user
    data=Postad.objects.filter(ad_postedby=uname)
    return render(request,'myads.html',{"ads":data})

@login_required(login_url='/signin')
def changepass(request):
    if request.method=="POST":
        newpass=request.POST.get("newpass")
        userid=request.user.id
        udata=User.objects.get(pk=userid)
        udata.set_password(newpass)
        udata.save()
        return render(request,"changepass.html",{'success':"Password changed successfully"})
    else:
        return render(request,'changepass.html')


def adsbycat(request,id):
    adbycat=Postad.objects.filter(ad_category=id)
    return render(request, 'adsbycat.html',{'adbycat':adbycat})


def inbox(request):
    #udata=UserProfile.objects.get(user=request.user)
    idata=Message.objects.filter(reciever=request.user)
    return render(request, 'inbox.html',{'messages':idata})

def outbox(request):
    odata=Message.objects.filter(sender=request.user)
    return render(request, 'outbox.html',{'messages':odata})

def ad_delete(request,id=None):
    Postad.objects.get(pk=id).delete()
    uname = request.user
    data = Postad.objects.filter(ad_postedby=uname)
    return render(request, 'myads.html', {"ads": data})

@login_required(login_url='/signin')
def editad(request,id=None):
    if request.method=="POST":
        title = request.POST.get('ad_title')
        desc = request.POST.get('ad_desc')
        catid = request.POST.get('ddlcat')
        locid = request.POST.get('ddlloc')
        image1 = request.FILES.get('ad_image1')
        image2 = request.FILES.get('ad_image2')
        image3 = request.FILES.get('ad_image3')
        phone = request.POST.get('ad_phone')
        price = request.POST.get('ad_price')
        ad=Postad.objects.get(pk=id)
        ad.ad_title=title
        ad.ad_category=Category.objects.get(pk=catid)
        ad.ad_location=Location.objects.get(pk=locid)
        ad.ad_desc=desc
        if image1:
            ad.ad_image1=image1
        if image2:
            ad.ad_image2=image2
        if image3:
            ad.ad_image3=image3
        ad.ad_phoneno=phone
        ad.ad_price=price
        ad.save()
        addata = Postad.objects.get(pk=id)
        locdata = Location.objects.all();
        cdata = Category.objects.all();
        return render(request, "editad.html", {'ad': addata, 'categories': cdata, 'locations': locdata,"success":"Ad updated successfully"})

    else:
        addata=Postad.objects.get(pk=id)
        locdata=Location.objects.all();
        cdata=Category.objects.all();
        return  render(request,"editad.html",{'ad':addata,'categories':cdata,'locations':locdata})

@login_required(login_url='/signin')
def sendmessage(request,id):
    if(request.method=="POST"):
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        sender=request.user #login
        ad=Postad.objects.get(pk=id)
        receiver=ad.ad_postedby #ad post
        msobj=Message(sub=subject,msg=message,
            sender=request.user,ad_id=Postad.objects.get(pk=id),reciever=receiver)
        msobj.save()
        ad_data = Postad.objects.get(pk=id)
        return render(request, 'addetail.html', {'ad': ad_data})
    else:
        ad_data = Postad.objects.get(pk=id)
        return render(request, 'addetail.html',{'ad':ad_data})

def home(request):
    ad_list = Postad.objects.all()
    page = request.GET.get('page', 1)#
    paginator = Paginator(ad_list, 3)#3 pages(1-3  3-6 7)
    try:
        addata = paginator.page(page)
    except PageNotAnInteger:
        addata = paginator.page(1)
    except EmptyPage:
        addata = paginator.page(paginator.num_pages)

    locdata = Location.objects.all()
    catdata = Category.objects.all();

    return render(request, 'index.html', {'addata': addata, 'catdata': catdata, 'loc': locdata})

@login_required(login_url='/signin')
def postad(request):
    if request.method=='POST':
        title=request.POST.get('ad_title')
        desc=request.POST.get('ad_desc')
        catid=request.POST.get('ddlcat')
        locid=request.POST.get('ddlloc')
        image1=request.FILES.get('ad_image1')
        image2=request.FILES.get('ad_image2')
        image3=request.FILES.get('ad_image3')
        phone=request.POST.get('ad_phone')
        price=request.POST.get('ad_price')
        adobj=Postad(ad_title=title,ad_desc=desc,ad_price=price,
               ad_image1=image1,ad_image2=image2,ad_image3=image3,
               ad_phoneno=phone,ad_category=Category.objects.get(pk=catid),
               ad_location=Location.objects.get(pk=locid),
               ad_postedby=User.objects.get(pk=request.user.id))
        adobj.save()
        return  redirect('myads')

    else:
        catdata=Category.objects.all();
        locdata=Location.objects.all();
        return render(request, 'postad.html',{'categories':catdata,'locdata':locdata})