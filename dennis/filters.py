import django_filters
from dennis.models import *
from django_filters import DateFilter

class Order_filter(django_filters.FilterSet):

    #field_name => set to the 'order' table field value
    # lookup_expr => set the expression you are looking for.
    start_date = DateFilter(field_name="placed_on",lookup_expr="gte")
    end_date = DateFilter(field_name="placed_on",lookup_expr="lte")


    class Meta:
        model = Order
        fields = "__all__"
        exclude = ['placed_by','placed_on']