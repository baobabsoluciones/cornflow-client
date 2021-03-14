from cornflow_client import SchemaManager
from cornflow_client.constants import DATASCHEMA
from unittest import TestCase
from data.dict_schema_example import dict_example

import json
import os


class TestSchemaManager(TestCase):
    
    def setUp(self):
        self.root_data = os.path.join(os.path.dirname(__file__), 'data')
        pass

    def get_data_file(self, filename):
        return os.path.join(self.root_data, filename)

    def test_schema_dict(self):
        sm = SchemaManager.from_filepath(self.get_data_file('pulp_json_schema.json'))
        dict_schema = sm.jsonschema_to_dict()
        
        self.assertCountEqual(dict_schema["CoefficientSchema"], dict_example["CoefficientSchema"])
        self.assertCountEqual(dict_schema["ObjectiveSchema"], dict_example["ObjectiveSchema"])
        self.assertCountEqual(dict_schema["ConstraintsSchema"], dict_example["ConstraintsSchema"])
        self.assertCountEqual(dict_schema["VariablesSchema"], dict_example["VariablesSchema"])
        self.assertCountEqual(dict_schema["ParametersSchema"], dict_example["ParametersSchema"])
        self.assertCountEqual(dict_schema["Sos1Schema"], dict_example["Sos1Schema"])
        self.assertCountEqual(dict_schema["Sos2Schema"], dict_example["Sos2Schema"])
        self.assertCountEqual(dict_schema[DATASCHEMA], dict_example[DATASCHEMA])
        sm.jsonschema_to_flask()

    def test_flask_schema(self):
        # TODO: I am not sure how to test that
        pass
    
    def test_schema_validation(self):
        sm = SchemaManager.from_filepath(self.get_data_file("pulp_json_schema.json"))
        val = sm.validate_file(self.get_data_file("pulp_example_data.json"))
        self.assertTrue(val)
        sm.jsonschema_to_flask()

    def test_schema_validation_2(self):
        sm = SchemaManager.from_filepath(self.get_data_file("hk_data_schema.json"))
        val = sm.validate_file(self.get_data_file("hk_data_input.json"))
        self.assertTrue(val)
        # Test that it can be transformed into a dict
        dict_schema = sm.jsonschema_to_dict()
        self.assertEqual(dict_schema['JobsSchema'][0],
                         {'name': 'id', 'type': 'Integer', 'required': True, 'allow_none': False, 'many': False})
        self.assertEqual(dict_schema['JobsSchema'][1],
                         {'name': 'successors', 'type': 'Integer', 'many': True, 'required': True})
        flask_schema = sm.dict_to_flask()
        marshmallow_object = flask_schema()
        self.assertEqual(marshmallow_object.fields.keys(), {'resources', 'needs', 'jobs', 'durations'})
        with open(self.get_data_file("hk_data_input.json"), 'r') as f:
            content = json.load(f)
        marshmallow_object.load(content)
        # marshmallow_object.fields['jobs'].nested().fields['successors']
    
    def test_validation_errors(self):
        sm = SchemaManager.from_filepath(self.get_data_file("pulp_json_schema.json"))
        data = {"objective": [], "constraints": [], "variables": []}
        bool = sm.validate_data(data)
        val = sm.get_validation_errors(data)
        self.assertFalse(bool)
        self.assertEqual(len(val), 1)
        self.assertEqual(val[0].message, "[] is not of type 'object'")
        sm.jsonschema_to_flask()
    
    def test_validation_errors2(self):
        sm = SchemaManager.from_filepath(self.get_data_file("pulp_json_schema.json"))
        data = {"objective": [], "constraints": ["notAConstraint"], "variables": ["notAVariable"]}
        val = sm.get_validation_errors(data)
        self.assertEqual(len(val), 3)
        sm.jsonschema_to_flask()

    def test_validation_errors3(self):
        sm = SchemaManager.from_filepath(self.get_data_file("hk_data_schema.json"))
        bool = sm.validate_file(self.get_data_file("data_input_bad.json"))
        val = sm.get_file_errors(self.get_data_file("data_input_bad.json"))
        self.assertFalse(bool)
        self.assertEqual(len(val), 2)
        sm.jsonschema_to_flask()
     
    def test_schema_names(self):
        sm = SchemaManager.from_filepath(self.get_data_file("name_problem_schema.json"))
        dict_schema = sm.jsonschema_to_dict()
        self.assertEqual(len(dict_schema["CoefficientsSchema"]), 2)
        self.assertEqual(len(dict_schema["Coefficients1Schema"]), 1)
        sm.jsonschema_to_flask()

    def test_array_integer(self):
        sm = SchemaManager.from_filepath(self.get_data_file('graph_coloring_input.json'))
        sm.jsonschema_to_flask()

    def test_non_mandatory(self):
        sm = SchemaManager.from_filepath(self.get_data_file('instance-hackathon2.json'))
        schema_marsh = sm.jsonschema_to_flask()
        with open(self.get_data_file('hk_data_input.json'), 'r') as f:
            content = json.load(f)
        schema_marsh().validate(content)
        return

    # TODO: fix this test and uncomment
    # def test_list_of_lists(self):
    #     sm = SchemaManager.from_filepath(self.get_data_file('graph_coloring2_input.json'))
    #     sm.jsonschema_to_flask()
