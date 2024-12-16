"""
Invokes django33-admin when the django33 module is run as a script.

Example: python -m django33 check
"""

from django33.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
