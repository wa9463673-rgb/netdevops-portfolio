import yaml
from jinja2 import Environment, FileSystemLoader

# Notice the ../../ - this tells Python to go up two folders to find the root
with open('../../inventory/r1_data.yml', 'r') as file:
    device_data = yaml.safe_load(file)

# Same here: go up two folders, then into the templates folder
env = Environment(loader=FileSystemLoader('../../templates'))
template = env.get_template('router_config.j2')

generated_config = template.render(device_data)

print(generated_config)