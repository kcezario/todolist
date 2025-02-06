import django_filters
from .models import Task
from tasks.constants import *

class TaskFilter(django_filters.FilterSet):
    """
    Filtra tarefas por status e due_date
    """
    status = django_filters.ChoiceFilter(choices=TaskStatus)
    due_date = django_filters.DateFilter()
    due_date__gte = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")
    due_date__lte = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["status", "due_date", "due_date__gte", "due_date__lte"]
