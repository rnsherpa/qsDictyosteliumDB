from django.db import models

class Clone(models.Model):
    index = models.AutoField(primary_key=True)
    qs_id = models.CharField("QS ID", max_length=20, unique=True)
    alt_id = models.CharField("Alternate ID", max_length=20)
    species = models.CharField("Species", max_length=50)
    origin = models.TextField("Origin Location", blank=True)
    origin_coords = models.CharField("Origin Coordinates", max_length=50, blank=True)
    box_plated_from = models.CharField("Box plated from", max_length=100, blank=True)
    collect_date = models.DateField("Date Collected", null=True, blank=True)
    freeze_date = models.DateField("Date Frozen", null=True, blank=True)
    collect_method = models.CharField("Collection Method", max_length=20, blank=True)
    culture_method = models.CharField("Culture Method", max_length=20, blank=True)
    origin_soil_sample = models.CharField("Origin Soil Sample", max_length=20, blank=True)
    freezer_loc = models.CharField("Location in Freezer", max_length=20, blank=True)
    box_name = models.CharField("Box Name", max_length=100, blank=True)
    box_initials = models.CharField("Box Initials", max_length=20, blank=True)
    is_clonal = models.BooleanField("Is Clonal", blank=True, null=True)
    mating_type = models.PositiveIntegerField("Mating Type", blank=True, null=True) 
    viol_hap_grp = models.CharField("vio.hap.grp", max_length=10, blank=True)
    sequenced = models.CharField("Sequenced", max_length=20, blank=True)
    is_amo = models.BooleanField("Amoebophilis Endosymbiont", blank=True, null=True)
    is_chlam = models.BooleanField("Neochlamydia Endosymbiont", blank=True, null=True)
    chlam_hap = models.CharField("Neochlamydia Haplotype", max_length=10, blank=True)
    endo_hap_id = models.CharField("Endosymbiont Haplotype ID", max_length=50, blank=True)
    endo_seq_hit = models.CharField("Endosymbiont 16S Sequence Hit", max_length=100, blank=True)
    burk_species = models.CharField("Burkholderia Species", max_length=50, blank=True)

    class Meta: 
        ordering = ['index']

    def __str__(self):
        return self.qs_id


class Paper(models.Model):
    index = models.AutoField(primary_key=True)
    doi = models.CharField("DOI", max_length=100, unique=True)
    title = models.TextField()
    first_author = models.CharField("First Author", max_length=50)
    last_author = models.CharField("Last Author", max_length=50)
    journal = models.TextField()
    year = models.PositiveIntegerField()
    clones = models.ManyToManyField(Clone, verbose_name="Clones used")

    class Meta:
        ordering = ['-year']
        

    def __str__(self):
        return self.title 

