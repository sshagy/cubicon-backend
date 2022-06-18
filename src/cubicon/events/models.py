import enum

from django.db import models


class Contest(models.Model):
    name = models.CharField(max_length=50, unique=True)
    information = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=50)
    # countryid = models.ForeignKey(Country, models.DO_NOTHING)
    organised_by = models.ForeignKey('accounts.User', models.PROTECT)
    is_published = models.BooleanField()
    links = models.JSONField()
    # eventspecs = models.CharField(db_column='eventSpecs', max_length=256, blank=True, null=True)
    # wcadelegate = models.TextField(db_column='wcaDelegate', blank=True, null=True)
    # cellname = models.CharField(db_column='cellName', max_length=45)
    # latitude = models.IntegerField(blank=True, null=True)
    # longitude = models.IntegerField(blank=True, null=True)


class RoundType(models.TextChoices):
    AVERAGE_OF_5 = enum.auto()
    MEAN_OF_3 = enum.auto()


class Round(models.Model):
    name = models.CharField(max_length=50, unique=True)
    contest = models.ForeignKey(Contest, models.CASCADE)
    type = models.CharField(max_length=30, choices=RoundType.choices)


class Result(models.Model):
    round = models.ForeignKey(Round, models.CASCADE)
    performed_by = models.ForeignKey('accounts.User', models.PROTECT)
    # eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventId')
    # roundtypeid = models.ForeignKey(RoundType, models.DO_NOTHING, db_column='roundTypeId')
    attempt1 = models.FloatField()
    attempt2 = models.FloatField()
    attempt3 = models.FloatField()
    attempt4 = models.FloatField()
    attempt5 = models.FloatField()
    best = models.FloatField()
    average = models.FloatField()
    pos = models.SmallIntegerField()
    # personcountryid = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    # formatid = models.ForeignKey(Format, models.DO_NOTHING, db_column='formatId')
    # regionalsinglerecord = models.CharField(db_column='regionalSingleRecord', max_length=3, blank=True, null=True)
    # regionalaveragerecord = models.CharField(db_column='regionalAverageRecord', max_length=3, blank=True, null=True)
