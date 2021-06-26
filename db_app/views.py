from distutils.util import strtobool
from django.http import JsonResponse, HttpResponse
import csv
from datetime import date
from django.shortcuts import render
from .models import Clone, Paper
from django.db.models import Count, Q, query
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'db_app/home.html')

def counts_chart(request):
    labels = []
    data = []

    queryset = Clone.objects.annotate(num_papers=Count('paper')).order_by('-num_papers')[:50]
    for entry in queryset:
        labels.append(entry.qs_id)
        data.append(entry.num_papers)

    return JsonResponse(data={'labels': labels,'data': data,})

def about(request):
    return render(request, "db_app/about.html")

def clones(request, exportCSV):
    
    cloneModel = Clone.objects.all() # get all clone data
    
    if request.method == 'GET':
        # these receive the filter entries
        clone_id_query = request.GET.get('clone_search')
        dicty_species_query = request.GET.get('dicty_species') 
        burk_species_query = request.GET.get('burk_species')
        amo_endo_query = request.GET.get('amo_endo')
        chlam_endo_query = request.GET.get('chlam_endo')
        mating_type_query = request.GET.get('mating_type')
        min_papers_query = request.GET.get('min_papers')

        # we only want to filter if we are receiving filter entries
        if clone_id_query !='' and clone_id_query is not None:
            cloneModel = cloneModel.filter(Q(qs_id__iexact=clone_id_query) | Q(alt_id__iexact=clone_id_query))
        
        if dicty_species_query !='' and dicty_species_query is not None:
            dicty_species_query = request.GET.getlist('dicty_species') # getlist for requests that can have multiple options in them
            cloneModel = cloneModel.filter(species__in=dicty_species_query) # __in is used for mulitple "or" conditions
        
        if burk_species_query !='' and burk_species_query is not None:
            burk_species_query = request.GET.getlist('burk_species')
            cloneModel = cloneModel.filter(burk_species__in=burk_species_query)

        if amo_endo_query !='' and amo_endo_query is not None:
            amo_bool = strtobool(amo_endo_query) # the html form sends over "True" or "False" as strings, so we need to convert them into booleans
            cloneModel = cloneModel.filter(is_amo=amo_bool)
        
        if chlam_endo_query!='' and chlam_endo_query is not None:
            chlam_bool = strtobool(chlam_endo_query)
            cloneModel = cloneModel.filter(is_chlam=chlam_bool)
        
        if mating_type_query!='' and mating_type_query is not None:
            mating_type_query = request.GET.getlist('mating_type')
            mating_type_query = [int(x) for x in mating_type_query] # convert all items in list to string
            cloneModel = cloneModel.filter(mating_type__in=mating_type_query)

        if min_papers_query!='' and min_papers_query is not None:
            cloneModel = cloneModel.annotate(num_papers=Count('paper')).filter(num_papers__gte=int(min_papers_query)).order_by('index')

    if exportCSV:
        return export_clones_csv(cloneModel)

    else:       
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
    
def papers(request, exportCSV):
    paperModel = Paper.objects.all()

    if request.method == 'GET':
        # receive search entry
        paper_query = request.GET.get('paper_search')

        if paper_query !='' and paper_query is not None:
            paperModel = paperModel.filter(Q(title__icontains=paper_query) | Q(first_author__icontains=paper_query))

    if exportCSV:
        return export_papers_csv(paperModel)    
        
    else:      
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

def dynamic_clone_view(request, qs_id, exportCSV):
    clone = Clone.objects.get(qs_id__iexact=qs_id) #__iexact: removes case sensitivity
    papers_containing_clone = clone.paper_set.all() #set of papers that have used a given clone
        
    if exportCSV:
        return export_papers_csv(papers_containing_clone)

    else:        
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

def dynamic_paper_view(request, index, exportCSV):
    paper = Paper.objects.get(index=index)
    clones_from_paper = paper.clones.all() #set of clones used in a given paper
    
    if exportCSV:
        return export_clones_csv(clones_from_paper)

    else:    
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

def export_clones_csv(queryset):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=qsdictyclones_{}.csv'.format(date.today())
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    csv_header = ['QS ID', 'Alternate ID', 'Species', 'Origin Location', 'Origin Coordinates', 'Box Plated From', 'Date Collected', 'Date Frozen', ' Collection Method', 'Culture Method', 'Origin Soil Sample', 'Location in Freezer', 'Box Name', 'Box Initials', 'Is Clonal', 'Mating Type', 'viol.hap.grp', 'Sequenced', 'Amoebophilis Endosymbiont', 'Neochlamydia Endosymbiont', 'Neochlamydia Haplotype', 'Endosymbiont Haplotype ID', 'Endosymbiont 16S Sequence Hit', 'Paraburkholderia Species']
    writer.writerow(csv_header)
    for item in queryset:
        writer.writerow([item.qs_id, item.alt_id, item.species, item.origin, item.origin_coords, item.box_plated_from, item.collect_date, item.freeze_date, item.collect_method, item.culture_method, item.origin_soil_sample, item.freezer_loc, item.box_name, item.box_initials, item.is_clonal, item.mating_type, item.viol_hap_grp, item.sequenced, item.is_amo, item.is_chlam, item.chlam_hap, item.endo_hap_id, item.endo_seq_hit, item.burk_species])
    
    return response

def export_papers_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=qs_papers_{}.csv'.format(date.today())
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    csv_header = ['DOI', 'Title', 'First Author', 'Last Author', 'Journal', 'Year']
    writer.writerow(csv_header)
    for item in queryset:
        writer.writerow([item.doi, item.title, item.first_author, item.last_author, item.journal, item.year])

    return response

