from django.shortcuts import render,redirect
from projects.forms import ProjectForm, ReviewForm
from projects.models import Project,Tag
from  django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.utils import searchProject,paginationProjects
# Create your views here.

def projects(request):
    project,search = searchProject(request)
    custom_range, project = paginationProjects(request, project, 6)
    context = {'projects':project,'search':search,'custom_range':custom_range}
    return render(request, 'projects/projects.html',context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            projectObj.getVoteCount
            messages.success(request, 'Review submitted successfully')
            return  redirect('project', pk=projectObj.id)



    context = {'project':projectObj,'form':form}
    return render(request, 'projects/single-project.html', context)
@login_required(login_url= "login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST' :
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            form.save()
            messages.success(request, 'Project created successfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html',context)
@login_required(login_url= "login")
def UpdateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST' :
        form = ProjectForm(request.POST, request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html',context)
@login_required(login_url= "login")
def DeleteeProject(request, pk):
    profile = request.user.profile
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'project':project}
    return render(request, 'delete.html',context)




















