from django.db import models


class Work(models.Model):
    class Oa_status(models.TextChoices):
        gold = 'gold',
        green = 'green',
        hybrid = 'hybrid',
        bronze = 'bronze',
        closed = 'closed',

    aid = models.CharField(max_length=16)
    title = models.TextField()
    publication_date = models.DateField()
    oa_status = models.CharField(max_length=6, choices=Oa_status.choices)
    language = models.CharField(max_length=32)
    cited_by_count = models.IntegerField()
    landing_page_url = models.URLField()
    referenced_works = models.ManyToManyField('self')
    related_works = models.ManyToManyField('self')
    updated_date = models.DateField()
    created_date = models.DateField()


class Concept(models.Model):
    aid = models.CharField(max_length=16)
    wikidata = models.URLField()
    display_name = models.CharField(max_length=64)
    level = models.IntegerField()
    description = models.TextField()
    works_count = models.IntegerField()
    cited_by_count = models.IntegerField()
    image_url = models.URLField()
    ancestors = models.ManyToManyField('self')
    related_concepts = models.ManyToManyField('self')
    updated_date = models.DateField()
    created_date = models.DateField()


class KeyWord(models.Model):
    keyword = models.CharField(max_length=32)


class WorkKeyWordRelation(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    keyword = models.ForeignKey(KeyWord, on_delete=models.CASCADE)
    score = models.FloatField()


class Institution(models.Model):
    class Type(models.TextChoices):
        Education = 'Education',
        Healthcare = 'Healthcare',
        Company = 'Company',
        Archive = 'Archive',
        Nonprofit = 'Nonprofit',
        Government = 'Government',
        Facility = 'Facility',
        Other = 'Other',

    aid = models.CharField(max_length=16)
    ror = models.URLField(null=True)
    display_name = models.CharField(max_length=128)
    type = models.CharField(choices=Type.choices, max_length=10)
    homepage_url = models.URLField()
    image_url = models.URLField()
    cited_by_count = models.IntegerField()
    city = models.CharField(max_length=64)
    country_code = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    associated_institutions = models.ManyToManyField('self')
    updated_date = models.DateField()
    created_date = models.DateField()


class Author(models.Model):
    aid = models.CharField(max_length=16)
    orcid = models.CharField(max_length=64)
    display_name = models.CharField(max_length=128)
    last_known_institution = models.ForeignKey(Institution, null=True, on_delete=models.SET_NULL)
    updated_date = models.DateField()
    created_date = models.DateField()


class Source(models.Model):
    class Type(models.TextChoices):
        journal = 'journal',
        repository = 'repository',
        conference = 'conference',
        ebook = 'ebook',
        platform = 'platform',
        bookseries = 'book series'

    aid = models.CharField(max_length=16)
    issn_l = models.CharField(max_length=16, null=True)
    host_origanization_name = models.CharField(max_length=64, null=True)
    display_name = models.CharField(max_length=128)
    works_count = models.IntegerField()
    cited_by_count = models.IntegerField()
    is_oa = models.BooleanField()
    is_in_doaj = models.BooleanField()
    homepage_url = models.URLField()
    country_code = models.CharField(max_length=2)
    type = models.CharField(choices=Type.choices, max_length=12)
    updated_date = models.DateField()
    created_date = models.DateField()


class Location(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    is_oa = models.BooleanField()
    landing_page_url = models.URLField()
    pdf_url = models.URLField()
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)
    license = models.CharField(max_length=16)
    version = models.CharField(max_length=32)
    is_accepted = models.BooleanField()
    is_published = models.BooleanField()


class CountsByYear(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, null=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, null=True, on_delete=models.CASCADE)
    year = models.IntegerField()
    works_count = models.IntegerField()
    cited_by_count = models.IntegerField()


class ConceptRelation(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, null=True, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    score = models.FloatField()


class SummaryStats(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, null=True, on_delete=models.CASCADE)
    twoyr_mean_citedness = models.FloatField()
    h_index = models.IntegerField()
    i10_index = models.IntegerField()
