from django.test import TestCase

from django_meta_og.models import Content, Namespace, Property
from django_meta_og.templatetags.django_meta_og import django_meta_og_prefix


class DjangoMetaOGPrefixTest(TestCase):
    def test(self):
        ns, _ = Namespace.objects.get_or_create(prefix="og", uri="https://ogp.me/ns#")
        prop, _ = Property.objects.get_or_create(namespace=ns, name="type")
        Content.objects.create(property=prop, content="website")
        self.assertEqual(django_meta_og_prefix(), "og: https://ogp.me/ns#")
