from django.db import models

class Spine(models.Model):
    image_path = models.CharField(max_length=200)
    avg_color = models.CharField(max_length=200)
    dominant_color = models.CharField(max_length=200)
    color_palette = models.CharField(max_length=200)
    height = models.FloatField()
    width = models.FloatField()
    text = models.TextField()
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    possible_matches = models.TextField()
    scan = models.ForeignKey('Scan', on_delete=models.CASCADE, null=True, related_name='spines')

class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    date_published = models.DateField()
    description = models.TextField()
    isbn = models.CharField(max_length=200)
    isbn10 = models.CharField(max_length=200)
    isbn13 = models.CharField(max_length=200)
    pages = models.IntegerField()
    binding = models.CharField(max_length=200)
    image_path = models.CharField(max_length=200)
    confidence = models.FloatField()
    spine = models.ForeignKey(Spine, on_delete=models.CASCADE, null=True, related_name='books')

class Scan(models.Model):
    uploaded_image = models.ImageField(upload_to='uploaded_images/')
    object_creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-object_creation_date']

    def serialize(self):
        return {
            "id": self.id,
            "uploaded_image": self.uploaded_image.url,
            "object_creation_date": self.object_creation_date.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username if self.user else "Unknown"
        }
    
    def __str__(self):
        return f"Scan {self.id} on {self.object_creation_date.strftime('%b %d %Y, %I:%M %p')}"
