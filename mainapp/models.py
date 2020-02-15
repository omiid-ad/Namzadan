from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام استان", unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="استان مربوطه")
    name = models.CharField(max_length=50, unique=True, verbose_name="نام شهر")

    def __str__(self):
        return self.name + " - " + self.province.name


# class Zone(models.Model):
#     city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر مربوطه")
#     name = models.CharField(max_length=20, verbose_name="نام یا کد ناحیه")

#     def __str__(self):
#         return self.name + " - " + self.city.name


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
    father_name = models.CharField(max_length=50, verbose_name="نام پدر", blank=True, null=True)
    code = models.CharField(max_length=10, verbose_name="کد انتخاباتی", blank=True, null=True)
    motto = models.TextField(blank=True, verbose_name="شعار انتخاباتی")
    party = models.CharField(max_length=25, choices=PARTIES, default=UNKNOWN, verbose_name="حزب")
    # zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="ناحیه", default=None)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="ناحیه انتخاباتی", default=None)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.profile_picture_url or self.profile_picture_url is None:
            self.profile_picture_url = "media/images/default.png"
        super().save()


class Resume(models.Model):
    SIKL = 'SI'
    DIPLOM = 'DI'
    FOQEDIPLOM = 'FD'
    LISANS = 'LI'
    FOQELISANS = 'FL'
    DOCTOR = 'DO'
    FOQEDOCTOR = 'FDD'
    HOZAVI = 'HO'
    UNKNOWN = 'UN'
    DEGREES = [
        (SIKL, 'سیکل'),
        (DIPLOM, 'دیپلم'),
        (FOQEDIPLOM, 'فوق دیپلم'),
        (LISANS, 'لیسانس'),
        (FOQELISANS, 'فوق لیسانس'),
        (DOCTOR, 'دکتری'),
        (FOQEDOCTOR, 'فوق دکتری'),
        (HOZAVI, 'حوزوی'),
        (UNKNOWN, 'نامشخص'),
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="نامزد")
    age = models.IntegerField(blank=True, null=True, verbose_name="سن")
    degree = models.CharField(max_length=50, blank=True, choices=DEGREES, default=UNKNOWN, verbose_name="مدرک تحصیلی")
    field = models.CharField(max_length=50, blank=True, verbose_name="رشته تحصیلی")
    moarefi_barnameha = models.TextField(blank=True, verbose_name="معرفی برنامه ها")
    # birth_locate = models.CharField(max_length=50, blank=True, verbose_name="محل تولد")
    # biography = models.TextField(blank=True, verbose_name="زندگی نامه")
    records = models.TextField(blank=True, verbose_name="سوابق")
    banner1 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True,
                                verbose_name="پوستر۱")  # 240*320
    banner2 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True, verbose_name="پوستر۲")
    banner3 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True, verbose_name="پوستر۳")
    banner4 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True, verbose_name="پوستر۴")

    def __str__(self):
        return self.candidate.full_name
