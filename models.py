from django.db import models

class Result(models.Model):
    pdf_url = models.CharField(max_length=200)
    template_path = models.CharField(max_length=200)
    result_csv = models.TextField()

    class Meta:
        app_label = 'myapp'
        db_table = 'myapp_result'
