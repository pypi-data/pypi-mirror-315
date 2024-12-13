
We provide a test framework to generically test all models, serializers, representation viewsets and viewsets of all applications. This test framework works with  [pytest-django](https://pytest-django.readthedocs.io/en/latest/)

## Configurations
Make sure DJANGO_SETTINGS_MODULE is defined (see Configuring Django settings) and make [your tests discoverable](https://pytest-django.readthedocs.io/en/latest/):

- pytest.ini
```python
    [pytest]
    DJANGO_SETTINGS_MODULE = projects.settings
    # -- recommended but optional:
    DJANGO_CONFIGURATION = Dev
    addopts = --nomigrations --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing:skip-covered
    python_files = tests.py test_*.py *_tests.py
```
- .coveragerc

This file `.coveragerc` is useful to  to control the coverage. You can exclude from the coverage some lines or functions which are not necessary in the evaluation of the coverage of the test.
[more information](https://coverage.readthedocs.io/en/6.3.1/config.html)

```python
[report]
exclude_lines =
    print()
    if hasattr
    raise Exception
    raise Http404
    except:

[run]
omit = */migrations/*
    manage.py
    */tests/*
    */test_project/*
```

Run your tests with pytest:

```python
    $ pytest
    $ pytest -vs # more details on the test
```
### Factory

To test our models we need to define the factories of the defined models. We recommend the use of [FactoryBoy](https://factoryboy.readthedocs.io/en/stable/)




## Test Framework

This framework can be run either in an application or for an entire project.
To run the test framework in your project, you need to import the configuration `default_config` and the Test Generic class `GenerateTest`

```python
from wbcore.tests import default_config, GenerateTest
```

* default_config : It is a dictionary whose keys are `models`, `serializers`, `representations`, `viewsets`.
    This config represents the parameters of our Generic Test, this dictionary groups all the items that will be tested.

### Override the default list in the config
If you don't want an item to be tested, you can override the lists of models, serializer, representations and viewsets obtained

    from wbcore.tests import default_config
    from app.models import TestModel
    config = default_config
    i.e config = {"models": [TestModel]} # in this case the serializers, representations and viewsets will be empty, so not tested
    config["models"] = [TestModel] # the list of models to test will contain only TestModel


### Confest.py
`conftest.py` is used to import external plugins or modules. By defining the following global variable, pytest will load the module and make it available for its test. Plugins are generally files defined in your project or other modules which might be needed in your tests. You can also load a set of predefined plugins as explained here.

So we defined a signal `get_specific_modules` and we import it into conftest to filter the modules imported into our config to those desired in this case from our application `myapp`. Otherwise all modules of all applications will be imported. you can customize this function to return the desired dataset in the `default_config`

```python
from wbcore.tests.signals import get_specific_modules

@receiver(get_specific_modules)
def receive_specfics_module(sender, *args, **kwargs):
    modules = filter(lambda x: x.__module__.startswith("myapp"), sender)
    return modules
```

### GenerateTest

Our generic test includes the following tests:

    * test_models :
        - test_get_endpoint_basename
        - test_representation_endpoint
        - test_representation_value_key
        - test_representation_label_key
        - test_str
        - test_field
    * test_serializers
        - test_serializers
    * test_representationviewsets
        - test_representationviewset
        - test_instancerepresentationviewset
    * test_modelviewsets
        - test_option_request
        - test_get_request
        - test_aggregation
        - test_get_endpoint
        - test_post_request
        - test_post_endpoint
        - test_destroy_multiple
        - test_get_list_title
        - test_get_instance_title
        - test_get_create_title
        - test_retrieve_request
        - test_delete_request
        - test_update_request
        - test_patch_request


It is possible to override these functions and define the desired behavior of each test


### Override the GenerateTest
```
from wbcore.tests import default_config, GenerateTest

class CustomGenerateTest(GenerateTest):
    def test_models(self, _model):
        pass

    def test_serializers(self, _serializer):
        pass

    def test_representationviewsets(self, rvs):
        pass

    def test_modelviewsets(self, mvs, client):
        pass


@pytest.mark.django_db
@CustomGenerateTest(default_config)
class TestProject:
    pass
```


### Define more Generic test
You can add to the generic test to the previously defined test
```
from wbcore.tests import default_config, GenerateTest

@pytest.mark.django_db
@GenerateTest(default_config)
class TestProject:
    # Do something with the config to generate other generic tests
    @pytest.mark.parametrize("_model", config.get("models", []))
    def test_models_generic(self, _model):
        assert True

    @pytest.mark.parametrize("_model", config.get("serializers", []))
    def test_serializers_generic(self, _model):
        assert True

    @pytest.mark.parametrize("_model", config.get("representations", []))
    def test_representationviewsets_generic(self, _model):
        assert True

    @pytest.mark.parametrize("_model", config.get("viewsets", []))
    def test_modelviewsets_generic(self, _model):
        assert True

```

### modular for specific tests
The test framework modulates enough and can be used as many times as desired according to the config, define some specific test on a set of modules.


```
from wbcore.tests import default_config, GenerateTest
from myapp.models import TestModel, TestModel2
from myapp.viewsets import TestRepresentation

@pytest.mark.django_db
@GenerateTest(default_config)
class GenericTest:
    pass

# config = default_config
config = {"models":[TestModel, TestModel2], "serializers":[], "representation":[TestRepresentation]}
@pytest.mark.django_db
@GenerateTest(config)
class TestSomething:
    # Do something specific with the config
    @pytest.mark.parametrize("_model", config.get("models", []))
    def test_models_generic(self, _model):
        assert True


CustomGenerateTest(GenerateTest):
    def test_models(self, _model):
        pass

@pytest.mark.django_db
@CustomGenerateTest(config)
class OtherTest:
    @pytest.mark.parametrize("_model", config.get("models", []))
    def test_models_generic(self, _model):
        assert True
```
