from django.db import models

class CounsellingEnquiry(models.Model):
    COUNSELLING_TYPES=[
        ("career", "Career"),
        ("mental_health", "Mental Health"),
        ("relationship", "Relationship"),
        ("academic", "Academic"),
        ("family", "Family"),
        ("financial", "Financial Wellness"),
        ("addiction", "Addiction Support"),
        ("trauma", "Trauma-informed"),
    ]

    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    counselling_type = models.CharField(max_length=50, choices=COUNSELLING_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_counselling_type_display()}"