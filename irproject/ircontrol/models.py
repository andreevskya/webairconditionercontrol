# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from django.db import models

class IrCommand(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(null=True, blank=True, max_length=256)
    frequency = models.IntegerField(default=36)
    command = ArrayField(models.IntegerField(), size=512)
    
    def __str__(self):
        return self.name
    
class CommandLogEntry(models.Model):
    executor = models.GenericIPAddressField()
    when = models.DateTimeField()
    command = models.ForeignKey(IrCommand)
    
    def __str__(self):
        return "%s %s %s" % (self.executor, self.command.name, self.when)
