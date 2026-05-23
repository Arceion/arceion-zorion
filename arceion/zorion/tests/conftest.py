"""
pytest configuration for arceion-zorion package tests.

This module configures Django for pytest-django when running tests
for the arceion-zorion library.
"""

import os
import django
from pathlib import Path
from django.conf import settings

# Configure Django settings before importing anything else
if not settings.configured:
    # Set minimal Django settings for testing
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
            'arceion.zorion.apps.zorionConfig',
        ],
        SECRET_KEY='test-secret-key-for-pytest',
        USE_TZ=True,
        MIDDLEWARE=[],
    )
    
    django.setup()
