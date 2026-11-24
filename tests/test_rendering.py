import sys
import os

# Add the automation/python directory to the path so we can import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../automation/python')))

from render_config import generate_config


def test_generate_config_contains_hostname():
    """Test that the rendered config contains the correct hostname."""
    # We need to change the working directory to automation/python
    # because render_config uses relative paths (../../)
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../automation/python')))

    config = generate_config()

    # Assertions (the tests that must pass)
    assert "hostname R1-Core" in config
    assert "interface GigabitEthernet0/1" in config
    assert "ip address 203.0.113.1 255.255.255.252" in config


def test_config_length():
    """Test that the config isn't empty."""
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../automation/python')))
    config = generate_config()
    assert len(config) > 50