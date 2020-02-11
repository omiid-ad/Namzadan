from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام استان", unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="استان مربوطه")
    name = models.CharField(max_length=50, verbose_name="نام شهر")

    def __str__(self):
        return self.name + " - " + self.province.name


class Zone(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر مربوطه")
    name = models.CharField(max_length=20, verbose_name="نام یا کد ناحیه")

    def __str__(self):
        return self.name + " - " + self.city.name


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

    profile_picture_url = models.ImageField(upload_to='images', default="images/default.png",
                                            blank=True, null=True,
                                            verbose_name="عکس پروفایل")  # 120*162px
    full_name = models.CharField(max_length=50, verbose_name="نام و نام خانوادگی")
    nickname = models.CharField(max_length=50, blank=True, verbose_name="نام مستعار(مشهور به)")
    father_name = models.CharField(max_length=50, verbose_name="نام پدر")
    code = models.CharField(max_length=10, unique=True, verbose_name="کد انتخاباتی")
    motto = models.TextField(blank=True, verbose_name="شعار انتخاباتی")
    party = models.CharField(max_length=25, choices=PARTIES, default=UNKNOWN, verbose_name="حزب")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="ناحیه", default=None)

    def __str__(self):
        return self.full_name + " - " + self.code

    def save(self, *args, **kwargs):
        if not self.profile_picture_url or self.profile_picture_url is None:
            self.profile_picture_url = "pps/default.png"
        super().save()


class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="نامزد")
    # fill with proper attributes
