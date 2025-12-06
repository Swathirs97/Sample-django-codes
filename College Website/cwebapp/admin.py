from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Department, Faculty, Course, Event, News, ImportantDate, PlacementRecord, PlacementStatistic, RecruitingCompany, StudentApplication

# Customize admin site header and title
admin.site.site_header = "EduCollege Administration"
admin.site.site_title = "EduCollege Admin"
admin.site.index_title = "Dashboard"

# Add custom dashboard link
class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['dashboard_url'] = reverse('admin_dashboard')
        return super().index(request, extra_context)

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'established_year']
    search_fields = ['name', 'head']
    list_per_page = 20
    ordering = ['name']
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'head', 'established_year')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'email', 'phone']
    list_filter = ['department', 'designation']
    search_fields = ['name', 'email', 'department__name']
    list_per_page = 20
    ordering = ['name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'designation', 'department', 'photo')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone')
        }),
        ('Qualifications', {
            'fields': ('qualifications',)
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'duration']
    list_filter = ['department', 'duration']
    search_fields = ['name', 'code', 'department__name']
    list_per_page = 20
    ordering = ['code']
    
    fieldsets = (
        ('Course Details', {
            'fields': ('name', 'code', 'department', 'duration')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'venue']
    list_filter = ['date']
    search_fields = ['title', 'venue', 'description']
    date_hierarchy = 'date'
    list_per_page = 20
    ordering = ['-date']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'venue', 'photo')
        }),
        ('Schedule', {
            'fields': ('date', 'time')
        }),
        ('Details', {
            'fields': ('description',)
        }),
    )

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date']
    list_filter = ['published_date']
    search_fields = ['title', 'content']
    date_hierarchy = 'published_date'
    list_per_page = 20
    ordering = ['-published_date']
    readonly_fields = ['published_date']
    
    fieldsets = (
        ('News Information', {
            'fields': ('title', 'photo', 'file')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Publication Date', {
            'fields': ('published_date',),
            'description': 'This is automatically set when creating news'
        }),
    )

@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'display_order']
    search_fields = ['title', 'date']
    list_per_page = 20
    ordering = ['display_order', 'id']
    
    fieldsets = (
        ('Date Information', {
            'fields': ('title', 'date', 'display_order')
        }),
    )

@admin.register(PlacementRecord)
class PlacementRecordAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'company_name', 'package', 'department', 'year']
    list_filter = ['year', 'department', 'company_name']
    search_fields = ['student_name', 'company_name', 'department__name']
    list_per_page = 20
    ordering = ['-year', 'company_name']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'department', 'year', 'photo')
        }),
        ('Placement Details', {
            'fields': ('company_name', 'package')
        }),
    )

@admin.register(PlacementStatistic)
class PlacementStatisticAdmin(admin.ModelAdmin):
    list_display = ['year', 'total_students', 'students_placed', 'placement_percentage', 'highest_package', 'average_package']
    search_fields = ['year']
    list_per_page = 20
    ordering = ['-year']
    
    fieldsets = (
        ('Year', {
            'fields': ('year',)
        }),
        ('Statistics', {
            'fields': ('total_students', 'students_placed', 'highest_package', 'average_package')
        }),
    )
    
    def placement_percentage(self, obj):
        return f"{obj.placement_percentage}%"
    placement_percentage.short_description = 'Placement %'

@admin.register(RecruitingCompany)
class RecruitingCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order']
    search_fields = ['name']
    list_per_page = 20
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'logo_url', 'display_order')
        }),
    )

@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'program_type', 'course', 'percentage', 'status', 'application_date']
    list_filter = ['status', 'program_type', 'application_date', 'gender']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'parent_name']
    list_per_page = 20
    ordering = ['-application_date']
    readonly_fields = ['application_date']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Academic Information', {
            'fields': ('program_type', 'course', 'previous_school', 'percentage')
        }),
        ('Parent/Guardian Information', {
            'fields': ('parent_name', 'parent_phone', 'parent_email')
        }),
        ('Application Status', {
            'fields': ('status', 'application_date')
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Student Name'
    
    actions = ['mark_under_review', 'mark_approved', 'mark_rejected']
    
    def mark_under_review(self, request, queryset):
        queryset.update(status='under_review')
    mark_under_review.short_description = "Mark selected as Under Review"
    
    def mark_approved(self, request, queryset):
        queryset.update(status='approved')
    mark_approved.short_description = "Mark selected as Approved"
    
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "Mark selected as Rejected"
