from django.db import models

class Clone(models.Model):
    index = models.AutoField(primary_key=True)
    qsID = models.CharField("QS ID", max_length=20, unique=True)
    altID = models.CharField("Alternate ID", max_length=20)
    species = models.CharField("Species", max_length=50)
    origin = models.TextField("Origin Location", blank=True)
    originCoords = models.CharField("Origin Coordinates", max_length=50, blank=True)
    boxPlatedFrom = models.CharField("Box plated from", max_length=100, blank=True)
    collectDate = models.DateField("Date Collected", null=True, blank=True)
    freezeDate = models.DateField("Date Frozen", null=True, blank=True)
    collectMethod = models.CharField("Collection Method", max_length=20, blank=True)
    cultureMethod = models.CharField("Culture Method", max_length=20, blank=True)
    originSoilSample = models.CharField("Origin Soil Sample", max_length=20, blank=True)
    freezerLoc = models.CharField("Location in Freezer", max_length=20, blank=True)
    boxName = models.CharField("Box Name", max_length=100, blank=True)
    boxInitials = models.CharField("Box Initials", max_length=20, blank=True)
    isClonal = models.BooleanField("Is Clonal", blank=True, null=True) 
    violHapGrp = models.CharField("vio.hap.grp", max_length=10, blank=True)
    sequenced = models.CharField("Sequenced", max_length=20, blank=True)
    isAmo = models.BooleanField("Amoebophilis Endosymbiont", blank=True, null=True)
    isChlam = models.BooleanField("Neochlamydia Endosymbiont", blank=True, null=True)
    chlamHap = models.CharField("Neochlamydia Haplotype", max_length=10, blank=True)
    endoHapID = models.CharField("Endosymbiont Haplotype ID", max_length=50, blank=True)
    endoSeqHit = models.CharField("Endosymbiont 16S Sequence Hit", max_length=100, blank=True)
    burkSpecies = models.CharField("Burkholderia Species", max_length=50, blank=True)

    class Meta: 
        ordering = ['index']

    def __str__(self):
        return self.qsID


class Paper(models.Model):
    index = models.AutoField(primary_key=True)
    doi = models.CharField("DOI", max_length=100, unique=True)
    title = models.TextField()
    firstAuthor = models.CharField("First Author", max_length=50)
    lastAuthor = models.CharField("Last Author", max_length=50)
    journal = models.TextField()
    year = models.PositiveIntegerField()
    clones = models.ManyToManyField(Clone, verbose_name="Clones used")

    class Meta:
        ordering = ['-year']
        

    def __str__(self):
        return self.title 

