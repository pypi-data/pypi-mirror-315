from faker import Faker
from fraud.core.utils import find_placeholders
from fraud.utils._decorators import set_module
from fraud.core.base import Template, Templater, BasicGenerator
default_faker_instance = Faker()

class FakerTemplater(Templater):
    def __init__(self, template, faker_instance):
        self.faker = faker_instance
        super().__init__(template)
    
    def apply(self):
        placeholders = find_placeholders(self.template.structure)
        faker_data = {}
        
        try: # this applies the same value for different instances of a placeholder, for example "{name} meet {name}" = "John meet John"
            for placeholder in placeholders:
                faker_data[placeholder] = placeholder_to_faker_func(placeholder, self.faker)()
            
        except Exception as e:
            raise ValueError(f"Faker Function Mapping Missing: {e}")

        return super().apply(faker_data)

def placeholder_to_faker_func(placeholder: str, faker_instance):
    faker_func = getattr(faker_instance, placeholder)
    return faker_func

class FakerGenerator(BasicGenerator):
    def __init__(self, template, faker_instance=default_faker_instance):
        self.template = template
        self.templater = FakerTemplater(self.template,faker_instance)

    def make_fake(self):
        return self.templater.apply()

@set_module("fraud")
def make_fake(template: str, count: int):
    temp = Template(template)
    gen = FakerGenerator(temp)
    return gen.make(count)