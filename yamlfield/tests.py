# -*- coding:utf-8 -*-

import datetime
import yaml
from fields import YAMLField
from forms import YAMLFormField
from django.db import models
from django.forms.util import ValidationError
from django.test import TestCase
from django.db import connection

class YAMLModel(models.Model):
    yaml = YAMLField()

class YAMLFieldTest(TestCase):
    """YAMLField Wrapper Tests"""
    
    def test_yaml_field_create(self):
        """Test saving a YAML object in our YAMLField"""
        yaml_obj =  {
            "item_1": "this is a yaml blah",
            "blergh": "hey, hey, hey"
        }
        obj = YAMLModel.objects.create(yaml=yaml_obj)
        new_obj = YAMLModel.objects.get(id=obj.id) 
        self.failUnlessEqual(new_obj.yaml, yaml_obj)
    
    def test_yaml_field_modify(self):
        """Test modifying a YAML object in our YAMLField"""
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
        """Test loading a YAML object from the DB"""
        yaml_obj_1 = {'a': 1, 'b': 2}
        obj = YAMLModel.objects.create(yaml=yaml_obj_1)
        new_obj = YAMLModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.yaml, yaml_obj_1)

    def test_yaml_field_load_unicode(self):
        """Test loading a YAML object with unicode from the DB"""
        yaml_obj_1 = {'a': 1, 'b': u'привет'}
        obj = YAMLModel.objects.create(yaml=yaml_obj_1)
        u_obj = YAMLModel.objects.get(id=obj.id)
        self.assertEqual(u_obj.yaml.get('b'), u'привет')

    def test_yaml_field_load_bad(self):
        """Test loading a bad YAML object from the DB"""
        bad_str = """
        vary bad string
        """
        obj = YAMLModel.objects.create(yaml=bad_str)
        bad_obj = YAMLModel.objects.get(id=obj.id)
        self.assertEqual(type(bad_obj.yaml), str)

    def test_yaml_list(self):
        """Test storing a yaml list"""
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


class YAMLFormFieldTest(TestCase):
    """YAMLFormField Tests"""

    def test_clean_bad(self):
        """Test validating bad YAMLFormField value"""
        field = YAMLFormField()
        self.assertRaises(ValidationError, lambda:
        field.clean("""
            bad YAML
        """))

    def test_clean_good(self):
        """Test validating good YAMLFormField value"""
        field = YAMLFormField()
        self.assertEqual(
            isinstance(field.clean("""
            a: 4
            b:
              - 1
              - 3
            c:
              1: a
              2: b
        """), dict),
        True)