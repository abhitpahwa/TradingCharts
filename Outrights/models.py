from django.db import models
from import_export import widgets
from django.utils import timezone

class CommonModel(models.Model):
    def __str__(self):
        return self.date
    date=models.CharField(null=True,max_length=20,unique=True)
    class Meta:
        abstract=True

labels=["contract"+str(i) for i in range(180)]
for label in labels:
    CommonModel.add_to_class(label,models.FloatField(null=True,blank=True))


class EuriborData(CommonModel):
    pass

class SterlingData(CommonModel):
    pass

class EuroSwissData(CommonModel):
    pass