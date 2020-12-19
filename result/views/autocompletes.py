from dal import autocomplete

from result.models import Result


class ResultAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Result.objects.none()

        qs = Result.objects.all()

        if self.q:
            qs = qs.filter(id=self.q)

        return qs