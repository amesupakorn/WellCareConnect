from django.db import models


class Disease(models.Model):
    disease_name = models.CharField(max_length=255, unique=True)  # ชื่อของโรค
    description = models.TextField()  # คำอธิบายเกี่ยวกับโรค
    symptoms = models.TextField()  # อาการของโรค
    treatment = models.TextField()  # วิธีการรักษาเบื้องต้น
    medication = models.TextField()  # ยารักษาโรค

    def __str__(self):
        return self.disease_name
