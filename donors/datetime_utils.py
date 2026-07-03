from datetime import datetime, date, timedelta
from donors.exceptions import CampDateError


def parse_camp_date(date_str: str) -> date:
    
    try:
        parsed = datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except (ValueError, AttributeError):
        raise CampDateError(f"'{date_str}' is not a valid date (expected YYYY-MM-DD).")

    if parsed < date.today():
        raise CampDateError(f"Camp date {parsed} cannot be in the past.")

    return parsed


def days_until_camp(camp_date: date) -> int:
    return (camp_date - date.today()).days


def is_camp_upcoming(camp_date: date, within_days: int = 30) -> bool:
    delta = days_until_camp(camp_date)
    return 0 <= delta <= within_days


def format_camp_date(camp_date: date) -> str:
    return camp_date.strftime('%d %b %Y')


def timestamp_now() -> datetime:
    return datetime.utcnow()