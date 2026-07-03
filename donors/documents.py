from mongoengine import (
    Document, StringField, IntField, BooleanField, DateTimeField,
    DateField, ReferenceField, ListField, EmailField
)
from datetime import datetime


class DonorDocument(Document):
    name = StringField(required=True, max_length=100)
    blood_group = StringField(required=True, max_length=3)
    phone = StringField(required=True, max_length=15)
    email = EmailField(required=True)
    location = StringField(required=True, max_length=100)
    available = BooleanField(default=True)
    registered_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'donors',
        'indexes': ['blood_group', 'location'],
        'ordering': ['-registered_at'],
    }

    def __str__(self):
        return f"{self.name} ({self.blood_group}) - {self.location}"


class CampDocument(Document):
    name = StringField(required=True, max_length=150)
    venue = StringField(required=True, max_length=200)
    organizer = StringField(required=True, max_length=150)
    camp_date = DateField(required=True)
    location = StringField(required=True, max_length=100)
    created_at = DateTimeField(default=datetime.utcnow)
    registered_donors = ListField(ReferenceField(DonorDocument), default=list)

    meta = {
        'collection': 'camps',
        'indexes': ['camp_date', 'location'],
        'ordering': ['camp_date'],
    }

    def __str__(self):
        return f"{self.name} @ {self.venue} on {self.camp_date}"


class BloodRequestDocument(Document):
    hospital = StringField(required=True, max_length=150)
    blood_group = StringField(required=True, max_length=3)
    location = StringField(required=True, max_length=100)
    units_needed = IntField(default=1)
    urgency = StringField(
        choices=('low', 'normal', 'high', 'critical'), default='normal'
    )
    fulfilled = BooleanField(default=False)
    matched_donors = ListField(ReferenceField(DonorDocument), default=list)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'blood_requests',
        'indexes': ['blood_group', 'location', 'urgency'],
        'ordering': ['-created_at'],
    }

    def __str__(self):
        return f"{self.hospital} needs {self.units_needed}x {self.blood_group}"


def create_donor(**kwargs) -> DonorDocument:
    donor = DonorDocument(**kwargs)
    donor.save()
    return donor


def get_donors_by_blood_group(blood_group: str):
    return DonorDocument.objects(blood_group=blood_group, available=True)


def get_donors_by_location(location: str):
    return DonorDocument.objects(location__iexact=location)


def get_donors_by_group_and_location(blood_group: str, location: str):
    return DonorDocument.objects(
        blood_group=blood_group, location__iexact=location, available=True
    )


def update_donor_availability(donor_id, available: bool):
    donor = DonorDocument.objects(id=donor_id).first()
    if donor:
        donor.available = available
        donor.save()
    return donor


def delete_donor(donor_id):
    donor = DonorDocument.objects(id=donor_id).first()
    if donor:
        donor.delete()
        return True
    return False


def camp_donor_count_report():
    
    report = []
    for camp in CampDocument.objects:
        report.append({
            'camp_name': camp.name,
            'venue': camp.venue,
            'camp_date': camp.camp_date,
            'location': camp.location,
            'donor_count': len(camp.registered_donors),
        })
    return report