from django.core.exceptions import ValidationError
from djongo import models


# region 自定义MongoDB字段类型
class Decimal128Field(models.DecimalField):
    """ 重写DecimalField，解决mongo中decimal类型为Decimal128的问题 """

    def to_python(self, value):
        if value is None or value == "":
            return None
        return float(str(value))

    def get_db_prep_save(self, value, connection):
        if value is None or value == "":
            return None
        prep_save_value = self.context.create_decimal_from_float(self.to_python(value))
        return connection.ops.adapt_decimalfield_value(prep_save_value, self.max_digits, self.decimal_places)


class BooleanField(models.Field):
    """ 重写BooleanField，解决ORM查询问题
     ！！！注意：
     1.名称必须为BooleanField，避免生成proto文件时字段类型错误
     2.需要在FilterSet中自定义filter_method或者在class Meta中添加filter_overrides
     a.自定义filter_method：
     is_aggregate = filters.CharFilter(method='filter_bool_field')
        def filter_bool_field(self, queryset, name, value):
            filter_kwargs = {name: value}
            queryset = queryset.filter(**filter_kwargs)
            return queryset
    b.添加filter_overrides：
    class Meta:
        model = my_models.model
        fields = '__all__'
        filter_overrides = {
            BooleanField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {},
            },
        }
     """

    def to_python(self, value):
        if self.null and value in self.empty_values:
            return None
        if value in (True, False):
            # 1/0 are equal to True/False. bool() converts former to latter.
            return bool(value)
        if value in ("t", "True", "1"):
            return True
        if value in ("f", "False", "0"):
            return False
        raise ValidationError(
            self.error_messages["invalid_nullable" if self.null else "invalid"],
            code="invalid",
            params={"value": value},
        )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return self.to_python(value)
# endregion
