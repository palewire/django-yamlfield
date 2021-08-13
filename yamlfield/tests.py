import json
import collections

from django.core.exceptions import ValidationError
from django.db import models
from .fields import YAMLField
from django.test import TestCase
from django.db import connection


class YAMLModel(models.Model):
    yaml = YAMLField()


class YAMLFieldTest(TestCase):
    """
    YAMLField Wrapper Tests
    """
    def test_yaml_field_create(self):
        """
        Test saving a YAML object in our YAMLField
        """
        yaml_obj = {
            "item_1": "this is a yaml blah",
            "blergh": "hey, hey, hey"
        }
        obj = YAMLModel.objects.create(yaml=yaml_obj)
        new_obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.yaml, yaml_obj)

    def test_yaml_field_modify(self):
        """
        Test modifying a YAML object in our YAMLField
        """
        yaml_obj_1 = {'a': 1, 'b': 2}
        yaml_obj_2 = {'a': 3, 'b': 4}
        obj = YAMLModel.objects.create(yaml=yaml_obj_1)
        self.failUnlessEqual(obj.yaml, yaml_obj_1)
        obj.yaml = yaml_obj_2
        self.failUnlessEqual(obj.yaml, yaml_obj_2)
        obj.save()
        self.failUnlessEqual(obj.yaml, yaml_obj_2)
        self.assert_(obj)

    def test_yaml_field_load(self):
        """
        Test loading a YAML object from the DB
        """
        yaml_obj_1 = {'a': 1, 'b': 2}
        obj = YAMLModel.objects.create(yaml=yaml_obj_1)
        new_obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.yaml, yaml_obj_1)

    def test_yaml_list(self):
        """
        Test storing a yaml list
        """
        yaml_obj = ["my", "list", "of", 1, "objs", {"hello": "there"}]
        obj = YAMLModel.objects.create(yaml=yaml_obj)
        new_obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.yaml, yaml_obj)

    def test_blank_yaml_field(self):
        # When there's no yaml...
        obj = YAMLModel.objects.create()
        # It should come out to python as None
        new_obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.yaml, None)
        # But be stored as an empty string in the database
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM yamlfield_yamlmodel;")
        row = cursor.fetchone()
        self.failUnlessEqual(row[1], "")

    def test_bad_yaml_to_python(self):
        with self.assertRaises(ValidationError) as exc:
            YAMLField().to_python('2013-01-65')
        self.assertEqual("Enter valid YAML", exc.exception.message)

    def test_value_from_object(self):
        yaml_obj = {
            "item_1": "this is a yaml blah",
            "blergh": "hey, hey, hey"
        }
        obj = YAMLModel.objects.create(yaml=yaml_obj)
        YAMLModel._meta.get_field('yaml').value_from_object(obj)

        obj2 = YAMLModel.objects.create(yaml='')
        YAMLModel._meta.get_field('yaml').value_from_object(obj2)

    def test_ordereddict(self):
        """
        Test storing an OrderedDict
        """
        ordered_data = collections.OrderedDict(
            [('one', 1), ('two', 2), ('five', 5), ('seven', 7), ('ten', 10)]
        )
        obj = YAMLModel.objects.create(yaml=[ordered_data])
        new_obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.yaml, [ordered_data])
        ordered_data.pop('seven')
        ordered_data['seven'] = 7
        self.assertEqual(dict(ordered_data), dict(new_obj.yaml[0]))
        self.failIfEqual(new_obj.yaml, [ordered_data])

    def test_nested_ordereddict(self):
        """
        Test an ordered dict nested in the YAML data
        """
        data = """{
          "pk": 11,
          "model": "core.chaineditem",
          "fields": {
            "chain": [
              "1fs-article-default-forced-utf8"
            ],
            "parameters": "OrderedDict([('download',OrderedDict([\
('force_encoding', 'utf-8')]))])",
            "notes_fr": "...",
            "is_active": true,
            "check_error": null,
            "item_type": [
              "core",
              "processingchain"
            ],
            "is_valid": true,
            "notes_nt": "",
            "item_id": 2,
            "position": 0,
            "notes_en": ""
          }
        }
        """
        data = json.loads(data)
        obj = YAMLModel.objects.create(yaml=data)
        obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(obj.yaml, data)
