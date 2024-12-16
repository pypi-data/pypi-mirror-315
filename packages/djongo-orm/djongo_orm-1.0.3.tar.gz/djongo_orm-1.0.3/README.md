Solve the problem of djongo adapting to django orm

1. Adaptation issue of decimal128 in mongo and decimalfield in django orm
```python
from djongo_orm.fields import Decimal128Field

class TestModel(models.Model):
    decimal_field = Decimal128Field(max_digits=10, decimal_places=2)
```

2. Query issue of boolean in mongo and django orm, and filter issue in rest framework

Model.py
```python
from djongo_orm.fields import BooleanField

class TestModel(models.Model):
    boolean_field = BooleanField()
```

filter.py
```python
from djongo_orm.fields import BooleanField
from django_filters import filters, filterset

class TestFilter1(filterset.FilterSet):
    boolean_field = filters.CharFilter(method='filter_boolean_field')
    def filter_boolean_field(self, queryset, name, value):
            queryset = queryset.filter(boolean_field=value)
            return queryset
    
    class Meta:
        model = TestModel
        fields = ['boolean_field']

class TestFilter2(filterset.FilterSet):
    
    class Meta:
        model = TestModel
        fields = ['__all__']
        filter_overrides = {
            BooleanField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {},
            },
        }
```

