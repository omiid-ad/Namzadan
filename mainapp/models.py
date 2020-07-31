from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import Truncator
from django.utils.html import strip_tags


class Province(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام استان", unique=True)

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان‌ها"

    def __str__(self):
        return self.name

    def get_city_count(self):
        return self.city_set.count()

    get_city_count.short_description = "تعداد شهرها"


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="استان مربوطه")
    name = models.CharField(max_length=50, unique=True, verbose_name="نام شهر")

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"

    def __str__(self):
        return self.name + " - " + self.province.name


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
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="ناحیه انتخاباتی", default=None)

    def get_profile_picture(self):
        return format_html(
            "<a target='_blank' href='{}'><img width=100 height=75 style='border-radius: 5px;' src='{}'></a>".format(
                self.profile_picture_url.url, self.profile_picture_url.url))

    get_profile_picture.short_description = "عکس"

    def get_resume(self):
        if self.resume:
            return format_html(
                "<a href='{}'>مشاهده</a>".format(reverse('admin:mainapp_resume_change', args=(self.resume.id,)))
            )

    get_resume.short_description = "رزومه"

    class Meta:
        verbose_name = "نامزد"
        verbose_name_plural = "نامزدها"

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
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, verbose_name="نامزد")
    age = models.IntegerField(blank=True, null=True, verbose_name="سن")
    degree = models.CharField(max_length=50, blank=True, choices=DEGREES, default=UNKNOWN, verbose_name="مدرک تحصیلی")
    field = models.CharField(max_length=50, blank=True, verbose_name="رشته تحصیلی")
    moarefi_barnameha = models.TextField(blank=True, verbose_name="معرفی برنامه ها")
    records = models.TextField(blank=True, verbose_name="سوابق")
    banner1 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True,
                                verbose_name="پوستر۱")  # 240*320
    banner2 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True, verbose_name="پوستر۲")
    banner3 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True, verbose_name="پوستر۳")
    banner4 = models.ImageField(upload_to="banners", default="banners/default.jpg", blank=True, verbose_name="پوستر۴")

    class Meta:
        verbose_name = "رزومه"
        verbose_name_plural = "رزومه‌ها"

    def __str__(self):
        return self.candidate.full_name

    def get_truncated_moarefi_barnameha(self):
        stripped = strip_tags(self.moarefi_barnameha)
        return Truncator(stripped).words(15)

    get_truncated_moarefi_barnameha.short_description = "معرفی برنامه‌ها"


class GlobalAds(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="نامزد", blank=True, null=True)
    banner = models.ImageField(upload_to="global", default="global/default.jpg", blank=True, verbose_name="پوستر")

    class Meta:
        verbose_name = "تبلیغ سراسری"
        verbose_name_plural = "تبلیغات سراسری"

    def save(self, *args, **kwargs):
        if self.banner is None:
            self.banner = "media/global/default.jpg"
        super().save()

    def __str__(self):
        if self.candidate:
            return self.candidate.full_name
        else:
            return super(GlobalAds, self).__str__()

    def get_banner_thumb(self):
        return format_html(
            "<a target='_blank' href='{}'><img width=100 height=75 style='border-radius: 5px;' src='{}'></a>".format(
                self.banner.url, self.banner.url))
    get_banner_thumb.short_description = "بنر تبلیغاتی (برای مشاهده در سایز اصلی،کلیک کنید)"
