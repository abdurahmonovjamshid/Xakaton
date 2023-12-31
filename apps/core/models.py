from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name
