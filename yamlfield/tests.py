import datetime
from fields import YAMLField
from django.db import models
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




