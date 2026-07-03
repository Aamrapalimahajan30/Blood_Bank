from donors.validators import validate_phone, validate_email, validate_blood_group
from donors.compatibility import compatible_donor_groups
from donors.exceptions import NoMatchingDonorError
from donors.datetime_utils import timestamp_now

class Donor:

    def __init__(self, name, blood_group, phone, email, location, available=True):
        self.name = name.strip()
        self.blood_group = validate_blood_group(blood_group)
        self.phone = validate_phone(phone)
        self.email = validate_email(email)
        self.location = location.strip()
        self.available = available
        self.registered_at = timestamp_now()

    def to_dict(self):
        return {
            'name': self.name,
            'blood_group': self.blood_group,
            'phone': self.phone,
            'email': self.email,
            'location': self.location,
            'available': self.available,
        }

    def __repr__(self):
        return f"<Donor {self.name} ({self.blood_group}) @ {self.location}>"


class BloodRequest:

    def __init__(self, hospital, blood_group, location, units_needed=1, urgency='normal'):
        self.hospital = hospital.strip()
        self.blood_group = validate_blood_group(blood_group)
        self.location = location.strip()
        self.units_needed = int(units_needed)
        self.urgency = urgency  # 'low' | 'normal' | 'high' | 'critical'
        self.created_at = timestamp_now()
        self.fulfilled = False

    def to_dict(self):
        return {
            'hospital': self.hospital,
            'blood_group': self.blood_group,
            'location': self.location,
            'units_needed': self.units_needed,
            'urgency': self.urgency,
            'fulfilled': self.fulfilled,
        }

    def __repr__(self):
        return f"<BloodRequest {self.hospital} needs {self.units_needed}x {self.blood_group}>"


class MatchEngine:
    
    def __init__(self, donor_pool):
        self.donor_pool = donor_pool

    def _as_dict(self, donor):
        return donor.to_dict() if isinstance(donor, Donor) else donor

    def find_matches(self, request: BloodRequest, same_location_only=True):
        compatible_groups = compatible_donor_groups(request.blood_group)
        matches = []

        for donor in self.donor_pool:
            d = self._as_dict(donor)
            if not d.get('available', True):
                continue
            if d.get('blood_group') not in compatible_groups:
                continue
            if same_location_only and d.get('location', '').lower() != request.location.lower():
                continue
            matches.append(d)

        if not matches:
            raise NoMatchingDonorError(
                f"No available donor found for {request.blood_group} in {request.location}"
            )

        return matches

    def best_match(self, request: BloodRequest):
        matches = self.find_matches(request)
        exact = [m for m in matches if m['blood_group'] == request.blood_group]
        return exact[0] if exact else matches[0]