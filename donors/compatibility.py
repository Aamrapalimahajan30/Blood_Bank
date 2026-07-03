VALID_BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']


COMPATIBILITY_CHART = {
    'A+':  ['A+', 'A-', 'O+', 'O-'],
    'A-':  ['A-', 'O-'],
    'B+':  ['B+', 'B-', 'O+', 'O-'],
    'B-':  ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+':  ['O+', 'O-'],
    'O-':  ['O-'],
}


def compatible_donor_groups(recipient_group: str) -> list:
    recipient_group = recipient_group.strip().upper()
    if recipient_group not in COMPATIBILITY_CHART:
        raise ValueError(f"Unknown blood group: {recipient_group}")
    return COMPATIBILITY_CHART[recipient_group]


def filter_available_donors(donor_list: list, blood_group: str, location: str = None) -> list:
    
    compatible_groups = compatible_donor_groups(blood_group)
    matched = []

    for donor in donor_list:
        if not donor.get('available', True):
            continue
        if donor.get('blood_group') not in compatible_groups:
            continue
        if location and donor.get('location', '').lower() != location.lower():
            continue
        matched.append(donor)

    return matched


def is_universal_donor(blood_group: str) -> bool:
    return blood_group.strip().upper() == 'O-'


def is_universal_recipient(blood_group: str) -> bool:
    return blood_group.strip().upper() == 'AB+'