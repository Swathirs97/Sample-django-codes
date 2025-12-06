from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    head = models.CharField(max_length=100)
    head_photo = models.ImageField(upload_to='department_heads/', null=True, blank=True)
    established_year = models.IntegerField()
    
    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    qualifications = models.TextField()
    photo = models.ImageField(upload_to='faculty_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    duration = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='news_photos/', null=True, blank=True)
    file = models.FileField(upload_to='news_files/', null=True, blank=True, help_text="Upload PDF, DOC, or other files")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']

class ImportantDate(models.Model):
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['display_order', 'id']

class PlacementRecord(models.Model):
    student_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    package = models.CharField(max_length=50, help_text="e.g., 12 LPA")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField(help_text="Placement year")
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.company_name}"
    
    class Meta:
        ordering = ['-year', 'company_name']

class PlacementStatistic(models.Model):
    year = models.IntegerField(unique=True)
    total_students = models.IntegerField()
    students_placed = models.IntegerField()
    highest_package = models.CharField(max_length=50)
    average_package = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Placement Statistics {self.year}"
    
    class Meta:
        ordering = ['-year']
    
    @property
    def placement_percentage(self):
        if self.total_students > 0:
            return round((self.students_placed / self.total_students) * 100, 2)
        return 0

class RecruitingCompany(models.Model):
    name = models.CharField(max_length=200)
    logo_url = models.URLField(blank=True, help_text="Optional: Company logo URL")
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Recruiting Companies"

class StudentApplication(models.Model):
    PROGRAM_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('diploma', 'Diploma'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Academic Information
    program_type = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    previous_school = models.CharField(max_length=200)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Previous exam percentage")
    
    # Parent/Guardian Information
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField()
    
    # Application Details
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program_type}"
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = "Student Application"
        verbose_name_plural = "Student Applications"
