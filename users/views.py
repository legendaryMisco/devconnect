from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Profile,skill,Message
from django.db.models import Q
from django.contrib import messages
from .forms import CustomUser, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles,paginationProfiles
#Create your views here.



def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'username dont exist')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'username or password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'user logout successfully')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUser()
    if request.method == 'POST':
        form = CustomUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "user account was created")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occur during registration')
    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html',context)


def profiles(request):
    profiles, search = searchProfiles(request)
    custom_range, profiles = paginationProfiles(request,profiles,3)
    context = {'profiles':profiles,'search':search,'custom_range':custom_range}
    return render(request, 'users/profiles.html',context)


def  userprofile(request,pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile':profile,'topskills':topSkills,'otherskills':otherSkills}
    return render(request, 'users/user_profile.html',context)



def userAccount(request):
    profile = request.user.profile
    context = {'profile':profile}
    return render(request, 'users/user_account.html',context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html',context)

@login_required(login_url="login")
def userSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/create_skill.html',context)

@login_required(login_url="login")
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            skill.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/create_skill.html',context)

@login_required(login_url="login")
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'project':skill}
    return render(request, 'delete.html',context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url="login")
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, "your message was successfully sent")
            return redirect('user-profile',pk=recipient.id)

    context = {'recipient':recipient,'form':form}
    return render(request, 'users/message_form.html', context)







