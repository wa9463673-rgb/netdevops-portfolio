import yaml
from jinja2 import Environment, FileSystemLoader
import os


def generate_config():
    """Reads YAML and renders the Jinja2 template using absolute paths."""
    # Calculate the absolute path to the project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

    inventory_file = os.path.join(base_dir, 'inventory', 'r1_data.yml')
    template_dir = os.path.join(base_dir, 'templates')

    with open(inventory_file, 'r') as file:
        device_data = yaml.safe_load(file)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('router_config.j2')

    return template.render(device_data)


if __name__ == '__main__':
    # This block only runs if you execute this file directly
    print(generate_config())