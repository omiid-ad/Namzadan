from django.db.models.signals import post_save, pre_save, pre_init
from .models import Candidate


def save_candidate(sender, instance, **kwargs):
    if not sender.profile_picture_url or sender.profile_picture_url is None:
        sender.profile_picture_url = "pps/default.png"
    instance.save()


post_save.connect(save_candidate, sender=Candidate)
pre_save.connect(save_candidate, sender=Candidate)
pre_init.connect(save_candidate, sender=Candidate)
