from django.test import TestCase

# Create your tests here.

class Servers(odels.Model):
    nombre = models.CharField(max_length=100)