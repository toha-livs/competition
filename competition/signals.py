from django.db.models.signals import post_save
from django.dispatch import receiver

from competition.models import SubCompetition, SubCompetitionManager, SubCompetitionSettings


@receiver(post_save, sender=SubCompetition)
def extensions(sender, instance, created, *args, **kwargs):
    if created:
        SubCompetitionManager.objects.create(sub_competition=instance)
        SubCompetitionSettings.objects.create(sub_competition=instance)

