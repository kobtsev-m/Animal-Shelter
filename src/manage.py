import os
import sys


def main():
    if not os.environ.get('DJANGO_SETTINGS_MODULE'): 
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError('Django import error.') from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
