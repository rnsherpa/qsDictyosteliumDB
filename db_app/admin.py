from django.contrib import admin
from .models import Clone, Paper
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin

class CloneResource(resources.ModelResource):

    class Meta:
        model = Clone
        import_id_fields = ['index']

class PaperResource(resources.ModelResource):

    clones = fields.Field(
        attribute='clones',
        widget=ManyToManyWidget(Clone, field='qs_id')
    )
    
    class Meta:
        model = Paper
        import_id_fields = ['index']
        fields = ('index','doi','title','first_author','last_author','journal','year')
    

class CloneAdmin(ImportExportModelAdmin):
    resource_class = CloneResource

class PaperAdmin(ImportExportModelAdmin):
    list_display = ('doi','title','first_author','last_author','journal','year')

    resource_class = PaperResource

admin.site.register(Clone,CloneAdmin) #register Clone model
admin.site.register(Paper,PaperAdmin) #register Paper model

