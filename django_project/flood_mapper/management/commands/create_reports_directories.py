__author__ = 'christian'
from django.core.management.base import BaseCommand

from flood_mapper.utilities.utilities import create_reports_directories


class Command(BaseCommand):
    args = ''
    help = 'Create the reports directories'
    def handle(self, *args, **options):
        create_reports_directories()
