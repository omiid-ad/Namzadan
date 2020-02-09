from django.db import models


class Candidate(models.Model):
    OSOOLGARA = 'OS'
    ESLAHTALAB = 'ES'
    OTHER = 'OT'
    UNKNOWN = 'UN'
    PARTIES = [
        (OSOOLGARA, 'اصولگرا'),
        (ESLAHTALAB, 'اصلاح طلب'),
        (OTHER, 'سایر'),
        (UNKNOWN, 'نامشخص'),
    ]

    profile_picture_url = models.ImageField(blank=True, null=True)  # set default pp for those who dont have one
    full_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, blank=True)
    father_name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    motto = models.TextField(blank=True)
    party = models.CharField(max_length=25, choices=PARTIES, default=UNKNOWN)

    def __str__(self):
        return self.full_name + " - " + self.code


class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    # fill with proper attributes
