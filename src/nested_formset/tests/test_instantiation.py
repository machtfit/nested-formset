from unittest import TestCase

from django.forms.models import BaseInlineFormSet
from nested_formset.tests import models as test_models

from nested_formset import nested_formset_factory


class InstantiationTests(TestCase):

    def setUp(self):

        self.formset_class = nested_formset_factory(
            test_models.Block,
            test_models.Building,
            test_models.Tenant,
        )

    def test_takes_parent_discovers_children(self):

        block = test_models.Block.objects.create()

        for i in range(10):
            test_models.Building.objects.create(block=block)

        formset = self.formset_class(instance=block)

        self.assertEqual(
            len(formset.forms), 10 + formset.extra
        )

    def test_child_form_contains_nested_formset(self):

        block = test_models.Block.objects.create()
        test_models.Building.objects.create(block=block)

        formset = self.formset_class(instance=block)

        self.assertTrue(
            isinstance(formset.forms[0].nested, BaseInlineFormSet)
        )
