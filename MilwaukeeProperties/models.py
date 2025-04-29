from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=45, unique=True)
    email = models.CharField(max_length=45, null=True, blank=True)
    first_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45, null=True, blank=True)



class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)


class CondoProject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True)


class Alderman(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45, null=True, blank=True)
    year_elected = models.IntegerField(null=True, blank=True)


class District(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    alderman = models.ForeignKey(
        Alderman,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

class Property(models.Model):
    id = models.IntegerField(primary_key=True)
    prop_id = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    type = models.CharField(max_length=45, null=True, blank=True)
    taxkey = models.CharField(max_length=45, null=True, blank=True)
    condo = models.ForeignKey(
        CondoProject,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    district = models.ForeignKey(
        District,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    nbhd = models.CharField(max_length=4)
    style = models.CharField(max_length=45, null=True, blank=True)
    extwall = models.CharField(max_length=45, null=True, blank=True)
    stories = models.DecimalField(max_digits=1, decimal_places=0, null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    finished_sqft = models.IntegerField(null=True, blank=True)
    units = models.IntegerField(null=True, blank=True)
    full_bath = models.IntegerField(null=True, blank=True)
    half_bath = models.IntegerField(null=True, blank=True)
    lot_size = models.IntegerField(null=True, blank=True)


class RealtorCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True)


class Realtor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45, null=True, blank=True)
    company = models.ForeignKey(
        RealtorCompany,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )


class Sale(models.Model):
    id = models.IntegerField(primary_key=True)
    property = models.ForeignKey(
        Property,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    realtor = models.ForeignKey(
        Realtor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    price = models.CharField(max_length=45, null=True, blank=True)
    date = models.DateField(null=True, blank=True)


class Favorite(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    property = models.ForeignKey(
        Property,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    date_added = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    comment = models.CharField(max_length=280, null=True, blank=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    property = models.ForeignKey(
        Property,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    date = models.DateTimeField(null=True, blank=True)
