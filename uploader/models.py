# -*- coding: utf-8 -*-
from django.db import models
from enum import Enum
from jsonfield import JSONField


class Video(models.Model):
    name = models.CharField(max_length=500)
    videofile = models.FileField(
        upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)


class StatusChoice(Enum):
    Uploading = "Uploading"
    Processing = "Processing"
    Complete = "Complete"
    Failed = "Failed"


class Job(models.Model):
    display_name = models.CharField(max_length=500)
    s3_obejct_key = models.CharField(max_length=500)
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=5,
        choices=[(tag, tag.value)
                 for tag in StatusChoice]
    )


class Result(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    result = JSONField()
