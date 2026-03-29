from django.db import models
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 20971520: # 20MB
        raise ValidationError("The maximum file size that can be uploaded is 20MB.")
    return value

class EvidenceItem(models.Model):
    case = models.ForeignKey('cases.Case', on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField(upload_to='evidence_uploads/', validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence for {self.case.case_id}"
