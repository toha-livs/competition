from competition.choices.apparatus import ApparatusChoices
from competition.choices.sex import SexChoices
from competition.models import Gymnast


def get_all_around_result(competition):
    result = []
    for gymnast in Gymnast.objects.filter(team__competition__competition=competition).order_by('level', '-score'):
        _gymnast = []
        result.append(_gymnast)
        if gymnast.team.competition.manager.sex == SexChoices.MALE:
            for apparatus in range(ApparatusChoices.get_competition_choices(gymnast.team.competition, day_off=False)):
                _gymnast.append()