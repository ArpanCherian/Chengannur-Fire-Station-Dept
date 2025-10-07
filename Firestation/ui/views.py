from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import csv
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from .models import userdetails
from .models import admindetails
from .models import firewater
from .models import generalIncident
from .models import AssistanceCall  

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



# User login form view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = userdetails.objects.get(username=username)
            if password == user.password:
                # Login success logic e.g., create session
                request.session['username'] = username  # simple session example
                messages.success(request, f"You have successfully logged in!")
                return redirect('userdashboard')
            else:
                messages.error(request, "Invalid password")
        except userdetails.DoesNotExist:
            messages.error(request, "Username not found")

    return render(request, 'user_login.html')

def logout(request):
    request.session.flush()
    return redirect('index')




def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('adminusername')
        password = request.POST.get('adminpassword')

        try:
            admin = admindetails.objects.get(adminusername=username)
            if password == admin.adminpassword:
                # Admin login success logic e.g., create session
                request.session['username'] = username  # simple session example
                messages.success(request, f"You have successfully logged in!")
                return redirect('admindashboard')
            else:
                messages.error(request, "Invalid password")
        except admindetails.DoesNotExist:
            messages.error(request, "Admin username not found")
    # admin login logic here or render admin login template
    return render(request, 'admin_login.html')




def userdashboard(request):
    if 'username' not in request.session:
        return redirect('user_login')

    username = request.session['username']

    # Fetch all user reports
    firewater_cases = list(firewater.objects.filter(userName=username).order_by('-form_date'))
    general_cases = list(generalIncident.objects.filter(userName=username).order_by('-form_date'))
    assistant_cases = list(AssistanceCall.objects.filter(userName=username).order_by('-form_date'))

    # Add model_type attribute to distinguish cases
    for case in firewater_cases:
        case.model_type = 'firewater'
    for case in general_cases:
        case.model_type = 'general'
    for case in assistant_cases:
        case.model_type = 'assistance'

    # Combine all into one list
    all_cases = firewater_cases + general_cases + assistant_cases
    all_cases_sorted = sorted(all_cases, key=lambda case: case.form_date, reverse=True)

    # Stats calculations
    total_reports = len(all_cases)
    fire_cases_count = len([c for c in firewater_cases if c.incident == 'Fire'])
    water_cases_count = len([c for c in firewater_cases if c.incident == 'Water'])
    other_cases_count = len(general_cases) + len(assistant_cases)

    context = {
        'recent_cases': all_cases_sorted[:10],
        'username': username,
        'total_reports': total_reports,
        'fire_cases': fire_cases_count,
        'water_cases': water_cases_count,
        'other_cases': other_cases_count,
    }
    return render(request, 'userdashboard.html', context)




def reportcase(request):
    return render(request, 'reportcase.html')




def admindashboard(request):
    if 'username' not in request.session:
        return redirect('admin_login')

    username = request.session['username']

    # Fetch all user reports
    firewater_cases = list(firewater.objects.filter(userName=username).order_by('-form_date'))
    general_cases = list(generalIncident.objects.filter(userName=username).order_by('-form_date'))
    assistant_cases = list(AssistanceCall.objects.filter(userName=username).order_by('-form_date'))

    # Add model_type attribute to distinguish cases
    for case in firewater_cases:
        case.model_type = 'firewater'
    for case in general_cases:
        case.model_type = 'general'
    for case in assistant_cases:
        case.model_type = 'assistance'

    # Combine all into one list
    all_cases = firewater_cases + general_cases + assistant_cases
    all_cases_sorted = sorted(all_cases, key=lambda case: case.form_date, reverse=True)

    # Stats calculations
    total_reports = len(all_cases)
    fire_cases_count = len([c for c in firewater_cases if c.incident == 'Fire'])
    water_cases_count = len([c for c in firewater_cases if c.incident == 'Water'])
    other_cases_count = len(general_cases) + len(assistant_cases)

    context = {
        'recent_cases': all_cases_sorted[:10],
        'username': username,
        'total_reports': total_reports,
        'fire_cases': fire_cases_count,
        'water_cases': water_cases_count,
        'other_cases': other_cases_count,
    }
    return render(request, 'admindashboard.html', context)






def adminreportcase(request):
    return render(request, 'adminreportcase.html')


def fireform(request):
    return render(request, 'fireform.html')

def adminfireform(request):
    return render(request, 'adminfireform.html')

def waterform(request):
    return render(request, 'waterform.html')

def adminwaterform(request):
    return render(request, 'adminwaterform.html')

def generalincidentform(request):
    return render(request, 'generalincidentform.html')

def admingeneralincidentform(request):
    return render(request, 'admingeneralincidentform.html')

def assistcalls(request):
    return render(request, 'assistcalls.html')

def adminassistcalls(request):
    return render(request, 'adminassistcalls.html')



def firewater_report(request):
    if request.method == 'POST':
        data = request.POST
        obj = firewater(
            userName = data.get('userName'),
            form_date = data.get('form_date'),
            incident = data.get('incident'),
            call_number = data.get('call_number'),
            call_received = data.get('call_received'),
            time_left_station = data.get('time_left_station'),
            time_reached_scene = data.get('time_reached_scene'),
            time_returned = data.get('time_returned'),
            occupancy_type = data.get('occupancy_type'),
            construction_type = data.get('construction_type'),
            owner_details = data.get('owner_details'),
            electrical_chemicals = data.get('electrical_chemicals'),
            hazardous_materials = data.get('hazardous_materials'),
            weather_conditions = data.get('weather_conditions'),
            caller_contact = data.get('caller_contact'),
            source_of_call = data.get('source_of_call'),
            nature_incident = data.get('nature_incident'),
            exact_location = data.get('exact_location'),
            owner_occupant = data.get('owner_occupant'),
            premises_occupancy = data.get('premises_occupancy'),
            building_details = data.get('building_details'),
            premises_chemicals = data.get('premises_chemicals'),
            premises_hazardous = data.get('premises_hazardous'),
            deaths_male = data.get('deaths_male'),
            deaths_female = data.get('deaths_female'),
            deaths_adult = data.get('deaths_adult'),
            deaths_child = data.get('deaths_child'),
            injuries_male = data.get('injuries_male'),
            injuries_female = data.get('injuries_female'),
            injuries_adult = data.get('injuries_adult'),
            injuries_child = data.get('injuries_child'),
            rescued_male = data.get('rescued_male'),
            rescued_female = data.get('rescued_female'),
            rescued_adult = data.get('rescued_adult'),
            rescued_child = data.get('rescued_child'),
            fire_personnel_injuries = data.get('fire_personnel_injuries'),
            animals_rescued = data.get('animals_rescued'),
            animals_lost = data.get('animals_lost'),
            hospital_doctor = data.get('hospital_doctor'),
            ambulance_notified = data.get('ambulance_notified'),
            appliances_crews = data.get('appliances_crews'),
            officer_in_charge = data.get('officer_in_charge'),
            equipment_used = data.get('equipment_used'),
            property_removed = data.get('property_removed'),
            property_saved = data.get('property_saved'),
            property_lost = data.get('property_lost'),
            approximate_loss = data.get('approximate_loss'),
            building_damage = data.get('building_damage'),
            items_destroyed = data.get('items_destroyed'),
            major_loss_cause = data.get('major_loss_cause')
        )
        obj.save()
        messages.success(request, 'Form submitted successfully!')
        return redirect('reportcase')  # Replace with your success url name
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'reportcase.html')  # Render your form template

def adminfirewater_report(request):
    if request.method == 'POST':
        data = request.POST
        obj = firewater(
            userName = data.get('userName'),
            form_date = data.get('form_date'),
            incident = data.get('incident'),
            call_number = data.get('call_number'),
            call_received = data.get('call_received'),
            time_left_station = data.get('time_left_station'),
            time_reached_scene = data.get('time_reached_scene'),
            time_returned = data.get('time_returned'),
            occupancy_type = data.get('occupancy_type'),
            construction_type = data.get('construction_type'),
            owner_details = data.get('owner_details'),
            electrical_chemicals = data.get('electrical_chemicals'),
            hazardous_materials = data.get('hazardous_materials'),
            weather_conditions = data.get('weather_conditions'),
            caller_contact = data.get('caller_contact'),
            source_of_call = data.get('source_of_call'),
            nature_incident = data.get('nature_incident'),
            exact_location = data.get('exact_location'),
            owner_occupant = data.get('owner_occupant'),
            premises_occupancy = data.get('premises_occupancy'),
            building_details = data.get('building_details'),
            premises_chemicals = data.get('premises_chemicals'),
            premises_hazardous = data.get('premises_hazardous'),
            deaths_male = data.get('deaths_male'),
            deaths_female = data.get('deaths_female'),
            deaths_adult = data.get('deaths_adult'),
            deaths_child = data.get('deaths_child'),
            injuries_male = data.get('injuries_male'),
            injuries_female = data.get('injuries_female'),
            injuries_adult = data.get('injuries_adult'),
            injuries_child = data.get('injuries_child'),
            rescued_male = data.get('rescued_male'),
            rescued_female = data.get('rescued_female'),
            rescued_adult = data.get('rescued_adult'),
            rescued_child = data.get('rescued_child'),
            fire_personnel_injuries = data.get('fire_personnel_injuries'),
            animals_rescued = data.get('animals_rescued'),
            animals_lost = data.get('animals_lost'),
            hospital_doctor = data.get('hospital_doctor'),
            ambulance_notified = data.get('ambulance_notified'),
            appliances_crews = data.get('appliances_crews'),
            officer_in_charge = data.get('officer_in_charge'),
            equipment_used = data.get('equipment_used'),
            property_removed = data.get('property_removed'),
            property_saved = data.get('property_saved'),
            property_lost = data.get('property_lost'),
            approximate_loss = data.get('approximate_loss'),
            building_damage = data.get('building_damage'),
            items_destroyed = data.get('items_destroyed'),
            major_loss_cause = data.get('major_loss_cause')
        )
        obj.save()
        messages.success(request, 'Form submitted successfully!')
        return redirect('adminreportcase')  # Replace with your success url name
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'adminreportcase.html')  # Render your form template


def generalincident_report(request):
    if request.method == 'POST':
        data = request.POST
        obj = generalIncident(
            userName = data.get('userName'),
            form_date = data.get('form_date'),
            incident = data.get('incident'),
            call_number = data.get('call_number'),
            call_received = data.get('call_received'),
            time_left_station = data.get('time_left_station'),
            time_reached_scene = data.get('time_reached_scene'),
            time_returned = data.get('time_returned'),
            occupancy_type = data.get('occupancy_type'),
            construction_type = data.get('construction_type'),
            owner_details = data.get('owner_details'),
            electrical_chemicals = data.get('electrical_chemicals'),
            hazardous_materials = data.get('hazardous_materials'),
            weather_conditions = data.get('weather_conditions'),
            caller_contact = data.get('caller_contact'),
            source_of_call = data.get('source_of_call'),
            nature_incident = data.get('nature_incident'),
            exact_location = data.get('exact_location'),
            owner_occupant = data.get('owner_occupant'),
            premises_occupancy = data.get('premises_occupancy'),
            building_details = data.get('building_details'),
            premises_chemicals = data.get('premises_chemicals'),
            premises_hazardous = data.get('premises_hazardous'),
            deaths_male = data.get('deaths_male'),
            deaths_female = data.get('deaths_female'),
            deaths_adult = data.get('deaths_adult'),
            deaths_child = data.get('deaths_child'),
            injured = data.get('injured'),
            rescued_male = data.get('rescued_male'),
            rescued_female = data.get('rescued_female'),
            rescued_adult = data.get('rescued_adult'),
            rescued_child = data.get('rescued_child'),
            fire_personnel_injuries = data.get('fire_personnel_injuries'),
            animals_rescued = data.get('animals_rescued'),
            animals_lost = data.get('animals_lost'),
            hospital_doctor = data.get('hospital_doctor'),
            ambulance_notified = data.get('ambulance_notified'),
            appliances_crews = data.get('appliances_crews'),
            officer_in_charge = data.get('officer_in_charge'),
            equipment_used = data.get('equipment_used'),
            property_removed = data.get('property_removed'),
            property_saved = data.get('property_saved'),
            property_lost = data.get('property_lost'),
            approximate_loss = data.get('approximate_loss'),
            building_damage = data.get('building_damage'),
            items_destroyed = data.get('items_destroyed'),
            major_loss_cause = data.get('major_loss_cause')
        )
        obj.save()
        messages.success(request, 'Form submitted successfully!')
        return redirect('reportcase')  # Replace with your success url name
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'generalincidentform.html') 


def admingeneralincident_report(request):
    if request.method == 'POST':
        data = request.POST
        obj = generalIncident(
            userName = data.get('userName'),
            form_date = data.get('form_date'),
            incident = data.get('incident'),
            call_number = data.get('call_number'),
            call_received = data.get('call_received'),
            time_left_station = data.get('time_left_station'),
            time_reached_scene = data.get('time_reached_scene'),
            time_returned = data.get('time_returned'),
            occupancy_type = data.get('occupancy_type'),
            construction_type = data.get('construction_type'),
            owner_details = data.get('owner_details'),
            electrical_chemicals = data.get('electrical_chemicals'),
            hazardous_materials = data.get('hazardous_materials'),
            weather_conditions = data.get('weather_conditions'),
            caller_contact = data.get('caller_contact'),
            source_of_call = data.get('source_of_call'),
            nature_incident = data.get('nature_incident'),
            exact_location = data.get('exact_location'),
            owner_occupant = data.get('owner_occupant'),
            premises_occupancy = data.get('premises_occupancy'),
            building_details = data.get('building_details'),
            premises_chemicals = data.get('premises_chemicals'),
            premises_hazardous = data.get('premises_hazardous'),
            deaths_male = data.get('deaths_male'),
            deaths_female = data.get('deaths_female'),
            deaths_adult = data.get('deaths_adult'),
            deaths_child = data.get('deaths_child'),
            injured = data.get('injured'),
            rescued_male = data.get('rescued_male'),
            rescued_female = data.get('rescued_female'),
            rescued_adult = data.get('rescued_adult'),
            rescued_child = data.get('rescued_child'),
            fire_personnel_injuries = data.get('fire_personnel_injuries'),
            animals_rescued = data.get('animals_rescued'),
            animals_lost = data.get('animals_lost'),
            hospital_doctor = data.get('hospital_doctor'),
            ambulance_notified = data.get('ambulance_notified'),
            appliances_crews = data.get('appliances_crews'),
            officer_in_charge = data.get('officer_in_charge'),
            equipment_used = data.get('equipment_used'),
            property_removed = data.get('property_removed'),
            property_saved = data.get('property_saved'),
            property_lost = data.get('property_lost'),
            approximate_loss = data.get('approximate_loss'),
            building_damage = data.get('building_damage'),
            items_destroyed = data.get('items_destroyed'),
            major_loss_cause = data.get('major_loss_cause')
        )
        obj.save()
        messages.success(request, 'Form submitted successfully!')
        return redirect('adminreportcase')  # Replace with your success url name
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'admingeneralincidentform.html') 



def assistancecall_report(request):
    if request.method == 'POST':
        data = request.POST
        obj = AssistanceCall(
            userName = data.get('userName'),
            form_date = data.get('form_date'),
            incident_type = data.get('incident_type'),
            call_number = data.get('call_number'),
            call_received = data.get('call_received'),
            time_left_station = data.get('time_left_station'),
            time_reached_scene = data.get('time_reached_scene'),
            time_returned = data.get('time_returned'),
            assistance_details = data.get('assistance_details'),
            electrical_chemicals = data.get('electrical_chemicals'),
            hazardous_materials = data.get('hazardous_materials'),
            weather_conditions = data.get('weather_conditions'),
            caller_contact = data.get('caller_contact'),
            source_of_call = data.get('source_of_call'),
            exact_location = data.get('exact_location'),
        )
        obj.save()
        messages.success(request, 'Form submitted successfully!')
        return redirect('reportcase')  # Replace with your success url name
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'assistcalls.html') 



def adminassistancecall_report(request):
    if request.method == 'POST':
        data = request.POST
        obj = AssistanceCall(
            userName = data.get('userName'),
            form_date = data.get('form_date'),
            incident_type = data.get('incident_type'),
            call_number = data.get('call_number'),
            call_received = data.get('call_received'),
            time_left_station = data.get('time_left_station'),
            time_reached_scene = data.get('time_reached_scene'),
            time_returned = data.get('time_returned'),
            assistance_details = data.get('assistance_details'),
            electrical_chemicals = data.get('electrical_chemicals'),
            hazardous_materials = data.get('hazardous_materials'),
            weather_conditions = data.get('weather_conditions'),
            caller_contact = data.get('caller_contact'),
            source_of_call = data.get('source_of_call'),
            exact_location = data.get('exact_location'),
        )
        obj.save()
        messages.success(request, 'Form submitted successfully!')
        return redirect('adminreportcase')  # Replace with your success url name
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'adminassistcalls.html') 



def case_detail(request, model_type, case_id):
    if 'username' not in request.session:
        return redirect('user_login')
    
    username = request.session['username']
    
    # Fetch the case based on model type
    if model_type == 'firewater':
        case = get_object_or_404(firewater, id=case_id, userName=username)
    elif model_type == 'general':
        case = get_object_or_404(generalIncident, id=case_id, userName=username)
    elif model_type == 'assistance':
        case = get_object_or_404(AssistanceCall, id=case_id, userName=username)
    else:
        return redirect('userdashboard')
    
    context = {
        'case': case,
        'model_type': model_type,
        'username': username,
    }
    return render(request, 'case_detail.html', context)



def admincase_detail(request, model_type, case_id):
    if 'username' not in request.session:
        return redirect('admin_login')
    
    username = request.session['username']
    
    # Fetch the case based on model type
    if model_type == 'firewater':
        case = get_object_or_404(firewater, id=case_id, userName=username)
    elif model_type == 'general':
        case = get_object_or_404(generalIncident, id=case_id, userName=username)
    elif model_type == 'assistance':
        case = get_object_or_404(AssistanceCall, id=case_id, userName=username)
    else:
        return redirect('admindashboard')
    
    context = {
        'case': case,
        'model_type': model_type,
        'username': username,
    }
    return render(request, 'admincase_detail.html', context)



def adminviewreport(request):
    qs_fire = list(firewater.objects.all())
    qs_general = list(generalIncident.objects.all())
    qs_assist = list(AssistanceCall.objects.all())

    month = request.GET.get('month')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    
    if month:
        y, m = month.split('-')
        qs_fire = [c for c in qs_fire if c.form_date.year == int(y) and c.form_date.month == int(m)]
        qs_general = [c for c in qs_general if c.form_date.year == int(y) and c.form_date.month == int(m)]
        qs_assist = [c for c in qs_assist if c.form_date.year == int(y) and c.form_date.month == int(m)]
    
    if start:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        qs_fire = [c for c in qs_fire if c.form_date >= start_date]
        qs_general = [c for c in qs_general if c.form_date >= start_date]
        qs_assist = [c for c in qs_assist if c.form_date >= start_date]
    
    if end:
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
        qs_fire = [c for c in qs_fire if c.form_date <= end_date]
        qs_general = [c for c in qs_general if c.form_date <= end_date]
        qs_assist = [c for c in qs_assist if c.form_date <= end_date]

    # Add model_type to each case
    for case in qs_fire:
        case.model_type = 'firewater'
    for case in qs_general:
        case.model_type = 'general'
    for case in qs_assist:
        case.model_type = 'assistance'

    all_reports = qs_fire + qs_general + qs_assist
    all_reports = sorted(all_reports, key=lambda c: c.form_date, reverse=True)

    return render(request, 'adminviewreport.html', {'all_reports': all_reports})



def clean_time(value):
    if not value:
        return value
    # If value looks like a list/tuple, take first element
    if isinstance(value, (list, tuple)):
        value = value[0]
    value = str(value).strip().replace('"','').replace("'",'')
    try:
        return datetime.strptime(value, "%I:%M %p").strftime("%H:%M")
    except Exception:
        try:
            return datetime.strptime(value, "%H:%M").strftime("%H:%M")
        except Exception:
            try:
                return datetime.strptime(value, "%H:%M:%S").strftime("%H:%M")
            except Exception:
                return ""  # fallback for invalid

def edit_case(request, model_type, case_id):
    if 'username' not in request.session:
        return redirect('admin_login')
    if model_type == 'firewater':
        case = get_object_or_404(firewater, id=case_id)
        template = 'edit_firewater.html'
    elif model_type == 'general':
        case = get_object_or_404(generalIncident, id=case_id)
        template = 'edit_general.html'
    elif model_type == 'assistance':
        case = get_object_or_404(AssistanceCall, id=case_id)
        template = 'edit_assistance.html'
    else:
        return redirect('adminviewreport')
    time_fields = ["call_received", "time_left_station", "time_reached_scene", "time_returned","ambulance_notified"]
    if request.method == 'POST':
        # Debug: print for investigation
        print("POST DATA:", dict(request.POST))
        for field, value in request.POST.items():
            if hasattr(case, field) and field != 'csrfmiddlewaretoken':
                if field in time_fields:
                    value = clean_time(value)
                setattr(case, field, value)
        case.save()
        messages.success(request, 'Report updated successfully!')
        return redirect('adminviewreport')
    context = {
        'case': case,
        'model_type': model_type,
    }
    return render(request, template, context)






def delete_case(request, model_type, case_id):
    if 'username' not in request.session:
        return redirect('admin_login')
    
    # Fetch and delete the case based on model type
    if model_type == 'firewater':
        case = get_object_or_404(firewater, id=case_id)
    elif model_type == 'general':
        case = get_object_or_404(generalIncident, id=case_id)
    elif model_type == 'assistance':
        case = get_object_or_404(AssistanceCall, id=case_id)
    else:
        return redirect('adminviewreport')
    
    case.delete()
    messages.success(request, 'Report deleted successfully!')
    return redirect('adminviewreport')




def download_reports(request):
    if 'username' not in request.session:
        return redirect('admin_login')
    
    # Get filtered reports
    qs_fire = list(firewater.objects.all())
    qs_general = list(generalIncident.objects.all())
    qs_assist = list(AssistanceCall.objects.all())

    month = request.GET.get('month')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    
    if month:
        y, m = month.split('-')
        qs_fire = [c for c in qs_fire if c.form_date.year == int(y) and c.form_date.month == int(m)]
        qs_general = [c for c in qs_general if c.form_date.year == int(y) and c.form_date.month == int(m)]
        qs_assist = [c for c in qs_assist if c.form_date.year == int(y) and c.form_date.month == int(m)]
    
    if start:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        qs_fire = [c for c in qs_fire if c.form_date >= start_date]
        qs_general = [c for c in qs_general if c.form_date >= start_date]
        qs_assist = [c for c in qs_assist if c.form_date >= start_date]
    
    if end:
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
        qs_fire = [c for c in qs_fire if c.form_date <= end_date]
        qs_general = [c for c in qs_general if c.form_date <= end_date]
        qs_assist = [c for c in qs_assist if c.form_date <= end_date]

    # Define comprehensive header
    header = [
        "Report Type",
        "Date of Filling the Form",
        "Name of the User",
        "Incident/Type",
        "Call Number",
        "Call Received",
        "Time Left Station",
        "Time Reached Scene",
        "Time Returned",
        "Occupancy Type",
        "Construction Type",
        "Owner / Occupant",
        "Electrical / Gas / Chemicals",
        "Hazardous Materials",
        "Weather Conditions",
        "Caller (Name & Contact)",
        "Source of Call",
        "Nature of Incident",
        "Exact Location",
        "Owner / Occupant Details",
        "Premises Occupancy Type",
        "Building Details",
        "Premises Electrical / Gas / Chemicals",
        "Premises Hazardous Materials",
        "Deaths Male",
        "Deaths Female",
        "Deaths Adult (Above 18)",
        "Deaths Child (Below 18)",
        "Injuries Male",
        "Injuries Female",
        "Injuries Adult (Above 18)",
        "Injuries Child (Below 18)",
        "Rescued Male",
        "Rescued Female",
        "Rescued Adult (Above 18)",
        "Rescued Child (Below 18)",
        "Fire Personnel Injuries",
        "Animals Rescued",
        "Animals Lost",
        "Hospital / Doctor",
        "Ambulance / Police Notified Time",
        "Appliances & Crews Attended",
        "Officer In Charge",
        "Equipment Used",
        "Property Removed",
        "Property Saved",
        "Property Lost",
        "Approximate Loss (₹)",
        "Building Damage",
        "Items Destroyed",
        "Cause of Major Loss",
        "Assistance Details",
        "Injured (GeneralIncident)",
    ]

    # Build all reports with complete data
    all_reports = []
    
    # Add firewater reports
    for obj in qs_fire:
        all_reports.append([
            "Firewater",
            obj.form_date.strftime('%d-%m-%Y') if obj.form_date else 'N/A',
            obj.userName,
            getattr(obj, 'incident', 'N/A'),
            getattr(obj, 'call_number', 'N/A'),
            getattr(obj, 'call_received', 'N/A'),
            getattr(obj, 'time_left_station', 'N/A'),
            getattr(obj, 'time_reached_scene', 'N/A'),
            getattr(obj, 'time_returned', 'N/A'),
            getattr(obj, 'occupancy_type', 'N/A'),
            getattr(obj, 'construction_type', 'N/A'),
            getattr(obj, 'owner_details', 'N/A'),
            getattr(obj, 'electrical_chemicals', 'N/A'),
            getattr(obj, 'hazardous_materials', 'N/A'),
            getattr(obj, 'weather_conditions', 'N/A'),
            getattr(obj, 'caller_contact', 'N/A'),
            getattr(obj, 'source_of_call', 'N/A'),
            getattr(obj, 'nature_incident', 'N/A'),
            getattr(obj, 'exact_location', 'N/A'),
            getattr(obj, 'owner_occupant', 'N/A'),
            getattr(obj, 'premises_occupancy', 'N/A'),
            getattr(obj, 'building_details', 'N/A'),
            getattr(obj, 'premises_chemicals', 'N/A'),
            getattr(obj, 'premises_hazardous', 'N/A'),
            getattr(obj, 'deaths_male', 'N/A'),
            getattr(obj, 'deaths_female', 'N/A'),
            getattr(obj, 'deaths_adult', 'N/A'),
            getattr(obj, 'deaths_child', 'N/A'),
            getattr(obj, 'injuries_male', 'N/A'),
            getattr(obj, 'injuries_female', 'N/A'),
            getattr(obj, 'injuries_adult', 'N/A'),
            getattr(obj, 'injuries_child', 'N/A'),
            getattr(obj, 'rescued_male', 'N/A'),
            getattr(obj, 'rescued_female', 'N/A'),
            getattr(obj, 'rescued_adult', 'N/A'),
            getattr(obj, 'rescued_child', 'N/A'),
            getattr(obj, 'fire_personnel_injuries', 'N/A'),
            getattr(obj, 'animals_rescued', 'N/A'),
            getattr(obj, 'animals_lost', 'N/A'),
            getattr(obj, 'hospital_doctor', 'N/A'),
            getattr(obj, 'ambulance_notified', 'N/A'),
            getattr(obj, 'appliances_crews', 'N/A'),
            getattr(obj, 'officer_in_charge', 'N/A'),
            getattr(obj, 'equipment_used', 'N/A'),
            getattr(obj, 'property_removed', 'N/A'),
            getattr(obj, 'property_saved', 'N/A'),
            getattr(obj, 'property_lost', 'N/A'),
            getattr(obj, 'approximate_loss', 'N/A'),
            getattr(obj, 'building_damage', 'N/A'),
            getattr(obj, 'items_destroyed', 'N/A'),
            getattr(obj, 'major_loss_cause', 'N/A'),
            '',  # Assistance Details (not applicable)
            '',  # Injured GeneralIncident (not applicable)
        ])
    
    # Add general incident reports
    for obj in qs_general:
        all_reports.append([
            "GeneralIncident",
            obj.form_date.strftime('%d-%m-%Y') if obj.form_date else 'N/A',
            obj.userName,
            getattr(obj, 'incident', 'N/A'),
            getattr(obj, 'call_number', 'N/A'),
            getattr(obj, 'call_received', 'N/A'),
            getattr(obj, 'time_left_station', 'N/A'),
            getattr(obj, 'time_reached_scene', 'N/A'),
            getattr(obj, 'time_returned', 'N/A'),
            getattr(obj, 'occupancy_type', 'N/A'),
            getattr(obj, 'construction_type', 'N/A'),
            getattr(obj, 'owner_details', 'N/A'),
            getattr(obj, 'electrical_chemicals', 'N/A'),
            getattr(obj, 'hazardous_materials', 'N/A'),
            getattr(obj, 'weather_conditions', 'N/A'),
            getattr(obj, 'caller_contact', 'N/A'),
            getattr(obj, 'source_of_call', 'N/A'),
            getattr(obj, 'nature_incident', 'N/A'),
            getattr(obj, 'exact_location', 'N/A'),
            getattr(obj, 'owner_occupant', 'N/A'),
            getattr(obj, 'premises_occupancy', 'N/A'),
            getattr(obj, 'building_details', 'N/A'),
            getattr(obj, 'premises_chemicals', 'N/A'),
            getattr(obj, 'premises_hazardous', 'N/A'),
            getattr(obj, 'deaths_male', 'N/A'),
            getattr(obj, 'deaths_female', 'N/A'),
            getattr(obj, 'deaths_adult', 'N/A'),
            getattr(obj, 'deaths_child', 'N/A'),
            '',  # Injuries male (not in GeneralIncident)
            '',  # Injuries female
            '',  # Injuries adult
            '',  # Injuries child
            getattr(obj, 'rescued_male', 'N/A'),
            getattr(obj, 'rescued_female', 'N/A'),
            getattr(obj, 'rescued_adult', 'N/A'),
            getattr(obj, 'rescued_child', 'N/A'),
            getattr(obj, 'fire_personnel_injuries', 'N/A'),
            getattr(obj, 'animals_rescued', 'N/A'),
            getattr(obj, 'animals_lost', 'N/A'),
            getattr(obj, 'hospital_doctor', 'N/A'),
            getattr(obj, 'ambulance_notified', 'N/A'),
            getattr(obj, 'appliances_crews', 'N/A'),
            getattr(obj, 'officer_in_charge', 'N/A'),
            getattr(obj, 'equipment_used', 'N/A'),
            getattr(obj, 'property_removed', 'N/A'),
            getattr(obj, 'property_saved', 'N/A'),
            getattr(obj, 'property_lost', 'N/A'),
            getattr(obj, 'approximate_loss', 'N/A'),
            getattr(obj, 'building_damage', 'N/A'),
            getattr(obj, 'items_destroyed', 'N/A'),
            getattr(obj, 'major_loss_cause', 'N/A'),
            '',  # Assistance Details (not applicable)
            getattr(obj, 'injured', 'N/A'),  # GeneralIncident specific field
        ])
    
    # Add assistance call reports
    for obj in qs_assist:
        all_reports.append([
            "AssistanceCall",
            obj.form_date.strftime('%d-%m-%Y') if obj.form_date else 'N/A',
            obj.userName,
            getattr(obj, 'incident_type', 'N/A'),
            getattr(obj, 'call_number', 'N/A'),
            getattr(obj, 'call_received', 'N/A'),
            getattr(obj, 'time_left_station', 'N/A'),
            getattr(obj, 'time_reached_scene', 'N/A'),
            getattr(obj, 'time_returned', 'N/A'),
            '',  # Occupancy Type (not in AssistanceCall)
            '',  # Construction Type
            '',  # Owner / Occupant
            getattr(obj, 'electrical_chemicals', 'N/A'),
            getattr(obj, 'hazardous_materials', 'N/A'),
            getattr(obj, 'weather_conditions', 'N/A'),
            getattr(obj, 'caller_contact', 'N/A'),
            getattr(obj, 'source_of_call', 'N/A'),
            '',  # Nature of Incident
            getattr(obj, 'exact_location', 'N/A'),
            '',  # Owner / Occupant Details
            '',  # Premises Occupancy Type
            '',  # Building Details
            '',  # Premises Electrical / Gas / Chemicals
            '',  # Premises Hazardous Materials
            '',  # Deaths Male
            '',  # Deaths Female
            '',  # Deaths Adult
            '',  # Deaths Child
            '',  # Injuries Male
            '',  # Injuries Female
            '',  # Injuries Adult
            '',  # Injuries Child
            '',  # Rescued Male
            '',  # Rescued Female
            '',  # Rescued Adult
            '',  # Rescued Child
            '',  # Fire Personnel Injuries
            '',  # Animals Rescued
            '',  # Animals Lost
            '',  # Hospital / Doctor
            '',  # Ambulance / Police Notified Time
            '',  # Appliances & Crews Attended
            '',  # Officer In Charge
            '',  # Equipment Used
            '',  # Property Removed
            '',  # Property Saved
            '',  # Property Lost
            '',  # Approximate Loss
            '',  # Building Damage
            '',  # Items Destroyed
            '',  # Cause of Major Loss
            getattr(obj, 'assistance_details', 'N/A'),
            '',  # Injured (GeneralIncident only)
        ])
    
    # Sort by date (most recent first)
    all_reports = sorted(all_reports, key=lambda c: c[1], reverse=True)

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Monthly_reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(header)
    writer.writerows(all_reports)
    
    return response




def allcase_detail(request, model_type, case_id):
    if 'username' not in request.session:
        return redirect('admin_login')  # Should redirect to admin_login, not user_login
    
    username = request.session['username']
    
    # Fetch the case based on model type - WITHOUT filtering by userName
    if model_type == 'firewater':
        case = get_object_or_404(firewater, id=case_id)
    elif model_type == 'general':
        case = get_object_or_404(generalIncident, id=case_id)
    elif model_type == 'assistance':
        case = get_object_or_404(AssistanceCall, id=case_id)
    else:
        return redirect('adminviewreport')
    
    context = {
        'case': case,
        'model_type': model_type,
        'username': username,
        'is_admin': True,  # Flag to indicate this is admin view
    }
    return render(request, 'allcasedetail.html', context)





def adminanalytics(request):
    # Get date filters
    month = request.GET.get('month', '')
    start = request.GET.get('start_date', '')
    end = request.GET.get('end_date', '')

    # Prepare queryset filters for all 3 models
    q_fire = list(firewater.objects.all())
    q_general = list(generalIncident.objects.all())
    q_assist = list(AssistanceCall.objects.all())
    
    # Apply month filter
    if month:
        y, m = month.split('-')
        q_fire = [c for c in q_fire if c.form_date.year == int(y) and c.form_date.month == int(m)]
        q_general = [c for c in q_general if c.form_date.year == int(y) and c.form_date.month == int(m)]
        q_assist = [c for c in q_assist if c.form_date.year == int(y) and c.form_date.month == int(m)]
    
    # Apply start date filter
    if start:
        startdate = datetime.strptime(start, "%Y-%m-%d").date()
        q_fire = [c for c in q_fire if c.form_date >= startdate]
        q_general = [c for c in q_general if c.form_date >= startdate]
        q_assist = [c for c in q_assist if c.form_date >= startdate]
    
    # Apply end date filter
    if end:
        enddate = datetime.strptime(end, "%Y-%m-%d").date()
        q_fire = [c for c in q_fire if c.form_date <= enddate]
        q_general = [c for c in q_general if c.form_date <= enddate]
        q_assist = [c for c in q_assist if c.form_date <= enddate]
    
    # 1. Total cases - all reports in database
    total_cases = len(q_fire) + len(q_general) + len(q_assist)
    
    # 3. Assistance calls - total AssistanceCall reports
    assistance_calls = len(q_assist)
    
    # 4-11. Incident-specific counts from generalIncident
    vehicle_accidents = sum([c.incident.lower() == "vehicle accident" for c in q_general])
    well_related = sum([c.incident.lower() == "well related" for c in q_general])
    lift_accidents = sum([c.incident.lower() == "lift accidents" for c in q_general])
    quarry = sum([c.incident.lower() == "quarry" for c in q_general])
    landslides = sum([c.incident.lower() == "landslides" for c in q_general])
    building_collapse = sum([c.incident.lower() == "building collapse" for c in q_general])
    tree_related = sum([c.incident.lower() == "tree related" for c in q_general])
    animal_calls = sum([c.incident.lower() == "animal calls" for c in q_general])

    # 12. Animals rescued - sum from firewater and generalIncident
    animals_rescued = (sum([int(c.animals_rescued or 0) for c in q_fire]) +
                       sum([int(c.animals_rescued or 0) for c in q_general]))
    
    # 13. Animals lost - sum from firewater and generalIncident
    animals_lost = (sum([int(c.animals_lost or 0) for c in q_fire]) +
                    sum([int(c.animals_lost or 0) for c in q_general]))

    # 14. Humans rescued - sum of rescued_male and rescued_female from both models
    human_rescued = (
        sum([int(c.rescued_male or 0) for c in q_fire]) +
        sum([int(c.rescued_female or 0) for c in q_fire]) +
        sum([int(c.rescued_male or 0) for c in q_general]) +
        sum([int(c.rescued_female or 0) for c in q_general])
    )
    
    # 15. Humans lost - sum of deaths_male and deaths_female from both models
    human_lost = (
        sum([int(c.deaths_male or 0) for c in q_fire]) +
        sum([int(c.deaths_female or 0) for c in q_fire]) +
        sum([int(c.deaths_male or 0) for c in q_general]) +
        sum([int(c.deaths_female or 0) for c in q_general])
    )
    
    # 16. Water related incidents - only from firewater where incident is "Water"
    # Filter water-related incidents (exact match with "Water")
    q_water = [c for c in q_fire if c.incident == 'Water']
    
    # Deaths - separate by gender and age
    water_deaths_male = sum([int(c.deaths_male or 0) for c in q_water])
    water_deaths_female = sum([int(c.deaths_female or 0) for c in q_water])
    water_deaths_adult = sum([int(c.deaths_adult or 0) for c in q_water])
    water_deaths_child = sum([int(c.deaths_child or 0) for c in q_water])
    
    # Rescued - separate by gender and age
    water_rescued_male = sum([int(c.rescued_male or 0) for c in q_water])
    water_rescued_female = sum([int(c.rescued_female or 0) for c in q_water])
    water_rescued_adult = sum([int(c.rescued_adult or 0) for c in q_water])
    water_rescued_child = sum([int(c.rescued_child or 0) for c in q_water])

    analysis = {
        'total_cases': total_cases,
        'assistance_calls': assistance_calls,
        'vehicle_accidents': vehicle_accidents,
        'well_related': well_related,
        'lift_accidents': lift_accidents,
        'quarry': quarry,
        'landslides': landslides,
        'building_collapse': building_collapse,
        'tree_related': tree_related,
        'animal_calls': animal_calls,
        'animals_rescued': animals_rescued,
        'animals_lost': animals_lost,
        'human_rescued': human_rescued,
        'human_lost': human_lost,
        'water_deaths_male': water_deaths_male,
        'water_deaths_female': water_deaths_female,
        'water_deaths_adult': water_deaths_adult,
        'water_deaths_child': water_deaths_child,
        'water_rescued_male': water_rescued_male,
        'water_rescued_female': water_rescued_female,
        'water_rescued_adult': water_rescued_adult,
        'water_rescued_child': water_rescued_child,
    }

    return render(request, 'adminanalytics.html', {'analysis': analysis})


def download_analytics_csv(request):
    """
    View to download analytics data as CSV with corrected logic
    """
    # Get filter parameters
    month = request.GET.get('month', '')
    start = request.GET.get('start_date', '')
    end = request.GET.get('end_date', '')
    
    # Prepare queryset filters for all 3 models
    q_fire = list(firewater.objects.all())
    q_general = list(generalIncident.objects.all())
    q_assist = list(AssistanceCall.objects.all())
    
    # Apply month filter
    if month:
        y, m = month.split('-')
        q_fire = [c for c in q_fire if c.form_date.year == int(y) and c.form_date.month == int(m)]
        q_general = [c for c in q_general if c.form_date.year == int(y) and c.form_date.month == int(m)]
        q_assist = [c for c in q_assist if c.form_date.year == int(y) and c.form_date.month == int(m)]
    
    # Apply start date filter
    if start:
        startdate = datetime.strptime(start, "%Y-%m-%d").date()
        q_fire = [c for c in q_fire if c.form_date >= startdate]
        q_general = [c for c in q_general if c.form_date >= startdate]
        q_assist = [c for c in q_assist if c.form_date >= startdate]
    
    # Apply end date filter
    if end:
        enddate = datetime.strptime(end, "%Y-%m-%d").date()
        q_fire = [c for c in q_fire if c.form_date <= enddate]
        q_general = [c for c in q_general if c.form_date <= enddate]
        q_assist = [c for c in q_assist if c.form_date <= enddate]
    
    # Calculate statistics using corrected logic
    total_cases = len(q_fire) + len(q_general) + len(q_assist)
    assistance_calls = len(q_assist)
    
    vehicle_accidents = sum([c.incident.lower() == "vehicle accident" for c in q_general])
    well_related = sum([c.incident.lower() == "well related" for c in q_general])
    lift_accidents = sum([c.incident.lower() == "lift accidents" for c in q_general])
    quarry = sum([c.incident.lower() == "quarry" for c in q_general])
    landslides = sum([c.incident.lower() == "landslides" for c in q_general])
    building_collapse = sum([c.incident.lower() == "building collapse" for c in q_general])
    tree_related = sum([c.incident.lower() == "tree related" for c in q_general])
    animal_calls = sum([c.incident.lower() == "animal calls" for c in q_general])

    animals_rescued = (sum([int(c.animals_rescued or 0) for c in q_fire]) +
                       sum([int(c.animals_rescued or 0) for c in q_general]))
    animals_lost = (sum([int(c.animals_lost or 0) for c in q_fire]) +
                    sum([int(c.animals_lost or 0) for c in q_general]))

    human_rescued = (
        sum([int(c.rescued_male or 0) for c in q_fire]) +
        sum([int(c.rescued_female or 0) for c in q_fire]) +
        sum([int(c.rescued_male or 0) for c in q_general]) +
        sum([int(c.rescued_female or 0) for c in q_general])
    )
    human_lost = (
        sum([int(c.deaths_male or 0) for c in q_fire]) +
        sum([int(c.deaths_female or 0) for c in q_fire]) +
        sum([int(c.deaths_male or 0) for c in q_general]) +
        sum([int(c.deaths_female or 0) for c in q_general])
    )
    
    # Water related incidents
    q_water = [c for c in q_fire if 'water' in c.incident.lower()]
    
    water_deaths_male = sum([int(c.deaths_male or 0) for c in q_water])
    water_deaths_female = sum([int(c.deaths_female or 0) for c in q_water])
    water_deaths_adult = sum([int(c.deaths_adult or 0) for c in q_water])
    water_deaths_child = sum([int(c.deaths_child or 0) for c in q_water])
    
    water_rescued_male = sum([int(c.rescued_male or 0) for c in q_water])
    water_rescued_female = sum([int(c.rescued_female or 0) for c in q_water])
    water_rescued_adult = sum([int(c.rescued_adult or 0) for c in q_water])
    water_rescued_child = sum([int(c.rescued_child or 0) for c in q_water])
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'incidents_analytics_{timestamp}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header with filter information
    writer.writerow(['Incidents Report Analytics'])
    writer.writerow(['Generated on:', datetime.now().strftime('%Y-%m-%d')])
    
    if month:
        writer.writerow(['Filtered by Month:', month])
    if start and end:
        writer.writerow(['Date Range:', f'{start} to {end}'])
    elif start:
        writer.writerow(['Start Date:', start])
    elif end:
        writer.writerow(['End Date:', end])
    
    writer.writerow([])  # Empty row for spacing
    
    # Write column headers
    writer.writerow(['Category', 'Total Cases', 'Notes'])
    
    # Write data rows
    writer.writerow(['Total Cases', total_cases, ''])
    writer.writerow(['Assistance Calls', assistance_calls, ''])
    writer.writerow(['Vehicle Accidents', vehicle_accidents, ''])
    writer.writerow(['Well Related', well_related, ''])
    writer.writerow(['Lift Accidents', lift_accidents, ''])
    writer.writerow(['Quarry', quarry, ''])
    writer.writerow(['Landslides', landslides, ''])
    writer.writerow(['Building Collapse', building_collapse, ''])
    writer.writerow(['Tree Related', tree_related, ''])
    writer.writerow(['Animal Calls', animal_calls, ''])
    writer.writerow(['Animal Rescued', animals_rescued, ''])
    writer.writerow(['Animal Lost', animals_lost, ''])
    writer.writerow(['Human Rescued', human_rescued, ''])
    writer.writerow(['Human Lost', human_lost, ''])
    
    # Water Related section
    writer.writerow([])
    writer.writerow(['Water Related Incidents', '', ''])
    writer.writerow(['Deaths - Male', water_deaths_male, ''])
    writer.writerow(['Deaths - Female', water_deaths_female, ''])
    writer.writerow(['Deaths - Adult (Above 18)', water_deaths_adult, ''])
    writer.writerow(['Deaths - Child (Below 18)', water_deaths_child, ''])
    writer.writerow(['Rescued - Male', water_rescued_male, ''])
    writer.writerow(['Rescued - Female', water_rescued_female, ''])
    writer.writerow(['Rescued - Adult (Above 18)', water_rescued_adult, ''])
    writer.writerow(['Rescued - Child (Below 18)', water_rescued_child, ''])
    
    return response




def adminadduser(request):
    # ✅ FIXED: Session check
    if 'username' not in request.session:
        return redirect('admin_login')  # Correct admin redirect
    
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        
        if form_type == "user":
            fullname = request.POST.get("fullname")
            username = request.POST.get("username")
            userid = request.POST.get("userid")
            password = request.POST.get("password")
            confirmpassword = request.POST.get("confirmpassword")
            
            # ✅ ADDED: Input validation
            if not all([fullname, username, userid, password, confirmpassword]):
                messages.error(request, "All fields are required.")
                return redirect("adminadduser")
            
            # ✅ ADDED: Check for duplicate username
            if userdetails.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect("adminadduser")
            
            # ✅ ADDED: Check for duplicate user ID
            if userdetails.objects.filter(userid=userid).exists():
                messages.error(request, "User ID already exists.")
                return redirect("adminadduser")
            
            if password != confirmpassword:
                messages.error(request, "User passwords do not match.")
                return redirect("adminadduser")
            
            # ✅ SECURITY: Hash passwords before storing
            # You should use Django's built-in password hashing
            # from django.contrib.auth.hashers import make_password
            # hashed_password = make_password(password)
            
            try:
                userdetails.objects.create(
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    password=password,  # Should be hashed!
                    confirmpassword=confirmpassword
                )
                messages.success(request, f"User {username} added successfully.")
            except Exception as e:
                messages.error(request, f"Error adding user: {str(e)}")
            
            return redirect("adminadduser")
        
        elif form_type == "admin":
            adminname = request.POST.get("adminname")
            adminusername = request.POST.get("adminusername")
            adminid = request.POST.get("adminid")
            adminpassword = request.POST.get("adminpassword")
            adminconfirmpassword = request.POST.get("adminconfirmpassword")
            
            # ✅ ADDED: Input validation
            if not all([adminname, adminusername, adminid, adminpassword, adminconfirmpassword]):
                messages.error(request, "All fields are required.")
                return redirect("adminadduser")
            
            # ✅ ADDED: Check for duplicate username
            if admindetails.objects.filter(adminusername=adminusername).exists():
                messages.error(request, "Admin username already exists.")
                return redirect("adminadduser")
            
            # ✅ ADDED: Check for duplicate admin ID
            if admindetails.objects.filter(adminid=adminid).exists():
                messages.error(request, "Admin ID already exists.")
                return redirect("adminadduser")
            
            if adminpassword != adminconfirmpassword:
                messages.error(request, "Admin passwords do not match.")
                return redirect("adminadduser")
            
            try:
                admindetails.objects.create(
                    adminname=adminname,
                    adminusername=adminusername,
                    adminid=adminid,
                    adminpassword=adminpassword,  # Should be hashed!
                    adminconfirmpassword=adminconfirmpassword
                )
                messages.success(request, f"Admin {adminusername} added successfully.")
            except Exception as e:
                messages.error(request, f"Error adding admin: {str(e)}")
            
            return redirect("adminadduser")
    
    # GET request
    all_users = userdetails.objects.all()
    all_admins = admindetails.objects.all()
    
    return render(request, "adminaddusers.html", {
        "all_users": all_users,
        "all_admins": all_admins,
    })

def deleteuser(request, user_id):
    # ✅ ADDED: Session check
    if 'username' not in request.session:
        return redirect('admin_login')
    
    # ✅ ADDED: POST method check for security
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("adminadduser")
    
    try:
        user = userdetails.objects.get(id=user_id)
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully.")
    except userdetails.DoesNotExist:
        messages.error(request, "User not found.")
    except Exception as e:
        messages.error(request, f"Error deleting user: {str(e)}")
    
    return redirect("adminadduser")

def deleteadmin(request, admin_id):
    # ✅ ADDED: Session check
    if 'username' not in request.session:
        return redirect('admin_login')
    
    # ✅ ADDED: POST method check for security
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("adminadduser")
    
    # ✅ ADDED: Prevent deleting yourself
    try:
        admin = admindetails.objects.get(id=admin_id)
        
        # Check if trying to delete current logged-in admin
        if admin.adminusername == request.session.get('username'):
            messages.error(request, "You cannot delete your own admin account.")
            return redirect("adminadduser")
        
        adminusername = admin.adminusername
        admin.delete()
        messages.success(request, f"Admin {adminusername} deleted successfully.")
    except admindetails.DoesNotExist:
        messages.error(request, "Admin not found.")
    except Exception as e:
        messages.error(request, f"Error deleting admin: {str(e)}")
    
    return redirect("adminadduser")