from dal import autocomplete

from competition.models import Gymnast


class GymnastAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Gymnast.objects.none()

        qs = Gymnast.objects.all()

        if self.q:
            if str(self.q).isdigit():
                qs = qs.filter(id=self.q)
            else:
                qs = qs.filter(user__ext__last_name__istartswith=self.q)
        return qs