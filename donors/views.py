from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from donors.forms import DonorRegistrationForm, CampForm, BloodRequestForm, CampRegistrationForm
from donors.documents import (
    DonorDocument, CampDocument, BloodRequestDocument,
    camp_donor_count_report,
)
from donors.core import BloodRequest, MatchEngine
from donors.notifications import notify_matched_donors
from donors.exceptions import NoMatchingDonorError, BloodBankError


def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            # Duplicate prevention: same phone OR same email already registered
            existing = DonorDocument.objects(phone=phone).first() or \
                    DonorDocument.objects(email=email).first()
            if existing:
                messages.error(
                    request,
                    f'A donor with this phone or email is already registered '
                    f'(name: {existing.name}). Please contact support if this is a mistake.'
                )
            else:
                DonorDocument(
                    name=form.cleaned_data['name'],
                    blood_group=form.cleaned_data['blood_group'],
                    phone=phone,
                    email=email,
                    location=form.cleaned_data['location'],
                ).save()
                messages.success(request, 'Donor registered successfully!')
                return redirect('register_donor')
    else:
        form = DonorRegistrationForm()

    donors = DonorDocument.objects.order_by('-registered_at')[:20]
    return render(request, 'donors/register_donor.html', {'form': form, 'donors': donors})


def camp_listing(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login as a hospital/organizer to create a camp.')
            return redirect('login')

        form = CampForm(request.POST)
        if form.is_valid():
            CampDocument(**form.cleaned_data).save()
            messages.success(request, 'Camp created successfully!')
            return redirect('camp_listing')
    else:
        form = CampForm()

    camps = CampDocument.objects.order_by('camp_date')
    return render(request, 'donors/camp_listing.html', {'form': form, 'camps': camps})


def camp_register_donor(request):
    if request.method == 'POST':
        form = CampRegistrationForm(request.POST)
        if form.is_valid():
            camp = CampDocument.objects(id=form.cleaned_data['camp_id']).first()
            donor = DonorDocument.objects(id=form.cleaned_data['donor_id']).first()
            if not camp or not donor:
                messages.error(request, 'Camp or donor not found.')
            elif donor in camp.registered_donors:
                messages.info(request, f'{donor.name} is already registered for {camp.name}.')
            else:
                camp.registered_donors.append(donor)
                camp.save()
                messages.success(request, f'{donor.name} registered for camp "{camp.name}".')
            return redirect('camp_listing')

    camps = CampDocument.objects.order_by('camp_date')
    donors = DonorDocument.objects.order_by('name')
    return render(request, 'donors/camp_register_donor.html', {'camps': camps, 'donors': donors})


@login_required
def request_board(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            BloodRequestDocument(**form.cleaned_data).save()
            messages.success(request, 'Blood request posted!')
            return redirect('request_board')
    else:
        form = BloodRequestForm()

    requests_qs = BloodRequestDocument.objects.order_by('-created_at')
    return render(request, 'donors/request_board.html', {'form': form, 'requests': requests_qs})


@login_required
def match_donors_view(request, request_id):
    
    blood_req_doc = BloodRequestDocument.objects(id=request_id).first()
    if not blood_req_doc:
        messages.error(request, 'Request not found.')
        return redirect('request_board')

    pool = [
        {
            'name': d.name, 'blood_group': d.blood_group,
            'phone': d.phone, 'email': d.email,
            'location': d.location, 'available': d.available,
        }
        for d in DonorDocument.objects(location__iexact=blood_req_doc.location, available=True)
    ]

    req_obj = BloodRequest(
        hospital=blood_req_doc.hospital,
        blood_group=blood_req_doc.blood_group,
        location=blood_req_doc.location,
        units_needed=blood_req_doc.units_needed,
        urgency=blood_req_doc.urgency,
    )

    engine = MatchEngine(pool)

    try:
        matches = engine.find_matches(req_obj, same_location_only=True)
    except NoMatchingDonorError as e:
        messages.warning(request, str(e))
        return redirect('request_board')

    sent = notify_matched_donors(matches, {
        'hospital': blood_req_doc.hospital,
        'location': blood_req_doc.location,
    })

    blood_req_doc.fulfilled = True
    blood_req_doc.save()

    messages.success(
        request,
        f'Matched {len(matches)} donor(s) and sent {len(sent)} notification(s).'
    )
    return render(request, 'donors/match_results.html', {
        'request_obj': blood_req_doc, 'matches': matches, 'notifications': sent,
    })


def camp_report(request):
    report = camp_donor_count_report()
    return render(request, 'donors/camp_report.html', {'report': report})