import csv
from django.shortcuts import render
from .models import Clone, Paper
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'db_app/home.html')

def clones(request):
    cloneModel = Clone.objects.all() # get all clone data
    page = request.GET.get('page', 1)
    paginator = Paginator(cloneModel, 10) # 10 clones per page
    try:
        clones = paginator.page(page)
    except PageNotAnInteger:
        clones = paginator.page(1)
    except EmptyPage:
        clones = paginator.page(paginator.num_pages)

    speciesList = Clone.objects.order_by('species').values('species').distinct() # get a list of the species from the Clone model
    burkList = Clone.objects.order_by('burk_species').values('burk_species').distinct().exclude(burk_species__exact='')

    context = {'clones': clones, 'speciesList': speciesList, 'burkList': burkList}
    return render(request, 'db_app/clones.html', context)
    
def papers(request):
    paperModel = Paper.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(paperModel, 10) # 10 clones per page
    try:
        papers = paginator.page(page)
    except PageNotAnInteger:
        papers = paginator.page(1)
    except EmptyPage:
        papers = paginator.page(paginator.num_pages)

    context = {'papers': papers}
    return render(request, 'db_app/papers.html', context)

def dynamic_clone_view(request, qs_id):
    clone = Clone.objects.get(qs_id__iexact=qs_id) #__iexact: removes case sensitivity
    papers_containing_clone = clone.paper_set.all() #set of papers that have used a given clone
    page = request.GET.get('page', 1)
    paginator = Paginator(papers_containing_clone, 10) # 10 papers per page
    try:
        papers = paginator.page(page)
    except PageNotAnInteger:
        papers = paginator.page(1)
    except EmptyPage:
        papers = paginator.page(paginator.num_pages)

    context = {'clone': clone, 'papers': papers}
    return render(request, "db_app/clone_details.html", context)

def dynamic_paper_view(request, index):
    paper = Paper.objects.get(index=index)
    clones_from_paper = paper.clones.all() #set of clones used in a given paper
    page = request.GET.get('page', 1)
    paginator = Paginator(clones_from_paper, 10) # 10 clones per page
    try:
        clones = paginator.page(page)
    except PageNotAnInteger:
        clones = paginator.page(1)
    except EmptyPage:
        clones = paginator.page(paginator.num_pages)

    context = {'paper': paper, 'clones': clones}
    return render(request, "db_app/paper_details.html", context)

def stats(request):
    paperCount = Clone.objects.annotate(num_papers=Count('paper')).order_by('-num_papers')[:5]
    context = {'paperCount': paperCount}
    return render(request, "db_app/stats.html", context)

def about(request):
    return render(request, "db_app/about.html")

# def searchClone(request):
#     return redirect(reverse(searchClone) + '')

    