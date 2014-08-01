# -*- coding: utf-8 -*-
# 14-8-1
# create by: snower

from django.contrib.admin.filters import *

BaseFieldListFilter = FieldListFilter

class FieldListFilter(FieldListFilter):
    _field_list_filters = []
    _take_priority_index = 0


# This should be registered last, because it's a last resort. For example,
# if a field is eligible to use the BooleanFieldListFilter, that'd be much
# more appropriate, and the AllValuesFieldListFilter won't get used for it.
class AllValuesFieldListFilter(AllValuesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull,
                                                 None)
        parent_model, reverse_path = reverse_field_path(model, field_path)
        queryset = parent_model._default_manager.all()
        # optional feature: limit choices base on existing relationships
        # queryset = queryset.complex_filter(
        #    {'%s__isnull' % reverse_path: False})
        limit_choices_to = get_limit_choices_to_from_path(model, field_path)
        queryset = queryset.filter(limit_choices_to)

        self.lookup_choices = (queryset
                               .distinct(field.name))
        BaseFieldListFilter.__init__(self,
            field, request, params, model, model_admin, field_path)

FieldListFilter.register(lambda f: True, AllValuesFieldListFilter)
