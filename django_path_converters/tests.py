from django.test import TestCase
from django.urls.converters import get_converters

class PathConverterTest(TestCase):
    def assertValidPathConverterExample(self, path_converter, example):
        target_type = path_converter.accepts[0]
        target_type = getattr(target_type, '__origin__', target_type)
        self.assertRegex(example, path_converter.regex)
        obj1 = path_converter.to_python(example)
        self.assertIsInstance(obj1, target_type)
        fragment1 = path_converter.to_url(obj1)
        self.assertRegex(fragment1, path_converter.regex)
        obj2 = path_converter.to_python(fragment1)
        self.assertEqual(obj1, obj2)
        self.assertIsInstance(obj2, target_type)
        fragment2 = path_converter.to_url(obj2)
        self.assertEqual(fragment1, fragment2)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from django.contrib.auth.models import User, Group
        User.objects.create(pk=12, username='Foo')
        Group.objects.create(pk=123, name='Foo')
        from django_path_converters.models import Group
        Group.objects.create(level=-12)
        Group.objects.create(level=14)
        Group.objects.create(level=25)

    def test_path_converter_examples(self):
        for converter in get_converters().values():
            for example in getattr(converter, 'examples', ()):
                with self.subTest(converter=converter, example=example):
                    self.assertValidPathConverterExample(converter, example)