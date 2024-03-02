from django.db import models
from django.utils import timezone
from accounts.models import UserAccount

class ConversionRecord(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    pdf_file = models.BinaryField()
    pdf_file_name = models.CharField(max_length=100, default='default_name')
    word_file = models.BinaryField(blank=True, null=True) 
    word_file_name = models.CharField(max_length=100, default='default_name') 
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, default='default_status')

    def __str__(self):
        return str(self.pdf_file)

class UsageLog(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    conversion = models.ForeignKey(ConversionRecord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    usage_type = models.CharField(max_length=255)
