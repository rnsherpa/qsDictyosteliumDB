from distutils.util import strtobool
from django.http import JsonResponse
import csv
from django.shortcuts import render
from .models import Clone, Paper
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'db_app/home.html')

def clones(request):
    cloneModel = Clone.objects.all() # get all clone data
    
    # these receive the filter entries
    clone_id_query = request.GET.get('clone_search')
    dicty_species_query = request.GET.get('dicty_species')
    burk_species_query = request.GET.get('burk_species')
    amo_endo_query = request.GET.get('amo_endo')
    chlam_endo_query = request.GET.get('chlam_endo')
    mating_type_query = request.GET.get('mating_type')

    # we only want to filter if we are receiving filter entries
    if clone_id_query !='' and clone_id_query is not None:
        cloneModel = cloneModel.filter(Q(qs_id__iexact=clone_id_query) | Q(alt_id__iexact=clone_id_query))
    
    if dicty_species_query !='' and dicty_species_query is not None:
        cloneModel = cloneModel.filter(species=dicty_species_query)
    
    if burk_species_query !='' and burk_species_query is not None:
        cloneModel = cloneModel.filter(burk_species=burk_species_query)

    if amo_endo_query !='' and amo_endo_query is not None:
        amo_bool = strtobool(amo_endo_query) # the html form sends over "True" or "False" as strings, so we need to convert them into booleans
        cloneModel = cloneModel.filter(is_amo=amo_bool)
    
    if chlam_endo_query!='' and chlam_endo_query is not None:
        chlam_bool = strtobool(chlam_endo_query)
        cloneModel = cloneModel.filter(is_chlam=chlam_bool)
    
    if mating_type_query!='' and mating_type_query is not None:
        cloneModel = cloneModel.filter(mating_type=int(mating_type_query))

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

    # receive search entry
    paper_id_query = request.GET.get('paper_search')

    if paper_id_query !='' and paper_id_query is not None:
        paperModel = paperModel.filter(title__icontains=paper_id_query)

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
    # paperCount = Clone.objects.annotate(num_papers=Count('paper')).order_by('-num_papers')[:20]
    # context = {'paperCount': paperCount}
    return render(request, "db_app/stats.html")

def counts_chart(request):
    labels = []
    data = []

    queryset = Clone.objects.annotate(num_papers=Count('paper')).order_by('-num_papers')[:20]
    for entry in queryset:
        labels.append(entry.qs_id)
        data.append(entry.num_papers)

    return JsonResponse(data={'labels': labels,'data': data,})

def about(request):
    return render(request, "db_app/about.html")