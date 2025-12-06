from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Department, Faculty, Course, Event, News, ImportantDate, PlacementRecord, PlacementStatistic, RecruitingCompany, StudentApplication

# Create your views here.

@staff_member_required
def admin_dashboard(request):
    import json
    from django.db.models import Count
    
    # Get statistics
    total_students = PlacementRecord.objects.count()
    total_faculty = Faculty.objects.count()
    total_departments = Department.objects.count()
    
    # Calculate average placement percentage
    stats = PlacementStatistic.objects.all()
    if stats:
        avg_placement = sum(stat.placement_percentage for stat in stats) / len(stats)
        placement_percentage = round(avg_placement, 1)
    else:
        placement_percentage = 0
    
    # Get recent data
    recent_applications = StudentApplication.objects.all()[:5]
    upcoming_events = Event.objects.all()[:4]
    recent_news = News.objects.all()[:4]
    recent_placements = PlacementRecord.objects.all()[:5]
    
    # Chart data - Placement trends
    placement_stats_ordered = PlacementStatistic.objects.all().order_by('year')
    placement_years = json.dumps([str(stat.year) for stat in placement_stats_ordered])
    placement_counts = json.dumps([stat.students_placed for stat in placement_stats_ordered])
    total_student_counts = json.dumps([stat.total_students for stat in placement_stats_ordered])
    
    # Chart data - Department distribution
    dept_data = PlacementRecord.objects.values('department__name').annotate(count=Count('id')).order_by('-count')[:8]
    department_names = json.dumps([item['department__name'] for item in dept_data])
    department_counts = json.dumps([item['count'] for item in dept_data])
    
    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_departments': total_departments,
        'placement_percentage': placement_percentage,
        'recent_applications': recent_applications,
        'upcoming_events': upcoming_events,
        'recent_news': recent_news,
        'recent_placements': recent_placements,
        'placement_years': placement_years,
        'placement_counts': placement_counts,
        'total_student_counts': total_student_counts,
        'department_names': department_names,
        'department_counts': department_counts,
    }
    
    return render(request, 'admin/dashboard.html', context)

def home(request):
    latest_news = News.objects.all()[:3]
    upcoming_events = Event.objects.all()[:3]
    context = {
        'latest_news': latest_news,
        'upcoming_events': upcoming_events
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def departments(request):
    all_departments = Department.objects.all()
    context = {'departments': all_departments}
    return render(request, 'departments.html', context)

def courses(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'courses.html', context)

def faculty(request):
    all_faculty = Faculty.objects.all()
    context = {'faculty': all_faculty}
    return render(request, 'faculty.html', context)

def admissions(request):
    important_dates = ImportantDate.objects.all()
    context = {'important_dates': important_dates}
    return render(request, 'admissions.html', context)

def events(request):
    all_events = Event.objects.all()
    context = {'events': all_events}
    return render(request, 'events.html', context)

def placements(request):
    placement_stats = PlacementStatistic.objects.all()
    placement_records = PlacementRecord.objects.all()[:20]
    recruiting_companies = RecruitingCompany.objects.all()
    context = {
        'placement_stats': placement_stats,
        'placement_records': placement_records,
        'recruiting_companies': recruiting_companies
    }
    return render(request, 'placements.html', context)

def apply(request):
    from .models import StudentApplication
    if request.method == 'POST':
        try:
            # Create new application
            application = StudentApplication(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                date_of_birth=request.POST.get('date_of_birth'),
                gender=request.POST.get('gender'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                program_type=request.POST.get('program_type'),
                previous_school=request.POST.get('previous_school'),
                percentage=request.POST.get('percentage'),
                parent_name=request.POST.get('parent_name'),
                parent_phone=request.POST.get('parent_phone'),
                parent_email=request.POST.get('parent_email'),
            )
            
            # Handle course (optional)
            course_id = request.POST.get('course')
            if course_id:
                application.course_id = course_id
            
            application.save()
            
            return render(request, 'application_success.html', {'application': application})
        except Exception as e:
            context = {
                'courses': Course.objects.all(),
                'error': str(e)
            }
            return render(request, 'apply.html', context)
    
    # GET request - show form
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'apply.html', context)

def contact(request):
    return render(request, 'contact.html')

# Admin subpages
@staff_member_required
def admin_tables(request):
    import json
    from django.db.models import Count
    
    applications = StudentApplication.objects.all()[:50]
    placements = PlacementRecord.objects.all()[:50]
    total_applications = StudentApplication.objects.count()
    
    # Chart data
    placement_stats_ordered = PlacementStatistic.objects.all().order_by('year')
    placement_years = json.dumps([str(stat.year) for stat in placement_stats_ordered])
    placement_counts = json.dumps([stat.students_placed for stat in placement_stats_ordered])
    total_student_counts = json.dumps([stat.total_students for stat in placement_stats_ordered])
    
    dept_data = PlacementRecord.objects.values('department__name').annotate(count=Count('id')).order_by('-count')[:8]
    department_names = json.dumps([item['department__name'] for item in dept_data])
    department_counts = json.dumps([item['count'] for item in dept_data])
    
    context = {
        'applications': applications,
        'placements': placements,
        'total_applications': total_applications,
        'placement_years': placement_years,
        'placement_counts': placement_counts,
        'total_student_counts': total_student_counts,
        'department_names': department_names,
        'department_counts': department_counts,
    }
    return render(request, 'admin/tables.html', context)

@staff_member_required
def admin_forms(request):
    from django.contrib import messages
    
    if request.method == 'POST':
        # Handle form submissions
        if 'add_department' in request.POST:
            dept = Department(
                name=request.POST.get('name'),
                head=request.POST.get('head'),
                established_year=request.POST.get('established_year'),
                description=request.POST.get('description')
            )
            if request.FILES.get('head_photo'):
                dept.head_photo = request.FILES['head_photo']
            dept.save()
            messages.success(request, 'Department added successfully!')
            
        elif 'add_faculty' in request.POST:
            fac = Faculty(
                name=request.POST.get('faculty_name'),
                designation=request.POST.get('designation'),
                department_id=request.POST.get('department'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                qualifications=request.POST.get('qualifications')
            )
            if request.FILES.get('photo'):
                fac.photo = request.FILES['photo']
            fac.save()
            messages.success(request, 'Faculty added successfully!')
            
        elif 'add_event' in request.POST:
            evt = Event(
                title=request.POST.get('event_title'),
                date=request.POST.get('event_date'),
                time=request.POST.get('event_time'),
                venue=request.POST.get('venue'),
                description=request.POST.get('event_description')
            )
            if request.FILES.get('event_photo'):
                evt.photo = request.FILES['event_photo']
            evt.save()
            messages.success(request, 'Event added successfully!')
            
        elif 'add_placement' in request.POST:
            plc = PlacementRecord(
                student_name=request.POST.get('student_name'),
                company_name=request.POST.get('company_name'),
                package=request.POST.get('package'),
                department_id=request.POST.get('placement_department'),
                year=request.POST.get('year')
            )
            if request.FILES.get('student_photo'):
                plc.photo = request.FILES['student_photo']
            plc.save()
            messages.success(request, 'Placement record added successfully!')
    
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'admin/forms.html', context)

@staff_member_required
def admin_charts(request):
    import json
    from django.db.models import Count
    
    # Chart data
    placement_stats_ordered = PlacementStatistic.objects.all().order_by('year')
    placement_years = json.dumps([str(stat.year) for stat in placement_stats_ordered])
    placement_counts = json.dumps([stat.students_placed for stat in placement_stats_ordered])
    total_student_counts = json.dumps([stat.total_students for stat in placement_stats_ordered])
    
    dept_data = PlacementRecord.objects.values('department__name').annotate(count=Count('id')).order_by('-count')[:8]
    department_names = json.dumps([item['department__name'] for item in dept_data])
    department_counts = json.dumps([item['count'] for item in dept_data])
    
    context = {
        'placement_years': placement_years,
        'placement_counts': placement_counts,
        'total_student_counts': total_student_counts,
        'department_names': department_names,
        'department_counts': department_counts,
    }
    return render(request, 'admin/charts.html', context)

@staff_member_required
def admin_profile(request):
    return render(request, 'admin/profile.html')

@staff_member_required
def admin_settings(request):
    return render(request, 'admin/settings.html')

# Department Management Views
@staff_member_required
def admin_departments_list(request):
    departments = Department.objects.all().order_by('name')
    context = {'departments': departments}
    return render(request, 'admin/departments_list.html', context)

@staff_member_required
def admin_department_add(request):
    if request.method == 'POST':
        dept = Department(
            name=request.POST.get('name'),
            head=request.POST.get('head'),
            established_year=request.POST.get('established_year'),
            description=request.POST.get('description')
        )
        if request.FILES.get('head_photo'):
            dept.head_photo = request.FILES['head_photo']
        dept.save()
        from django.contrib import messages
        messages.success(request, 'Department added successfully!')
        from django.shortcuts import redirect
        return redirect('admin_departments_list')
    
    context = {'action': 'add'}
    return render(request, 'admin/department_form.html', context)

@staff_member_required
def admin_department_edit(request, pk):
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.head = request.POST.get('head')
        department.established_year = request.POST.get('established_year')
        department.description = request.POST.get('description')
        
        if request.FILES.get('head_photo'):
            department.head_photo = request.FILES['head_photo']
        
        department.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('admin_departments_list')
    
    context = {
        'department': department,
        'action': 'edit'
    }
    return render(request, 'admin/department_form.html', context)

@staff_member_required
def admin_department_delete(request, pk):
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Department deleted successfully!')
    return redirect('admin_departments_list')
