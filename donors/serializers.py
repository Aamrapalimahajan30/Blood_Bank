from rest_framework import serializers
from donors.validators import validate_phone, validate_email, validate_blood_group
from donors.exceptions import BloodBankError


class DonorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    blood_group = serializers.CharField(max_length=3)
    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    location = serializers.CharField(max_length=100)
    available = serializers.BooleanField(default=True)
    registered_at = serializers.DateTimeField(read_only=True)

    def validate_phone(self, value):
        try:
            return validate_phone(value)
        except BloodBankError as e:
            raise serializers.ValidationError(str(e))

    def validate_email(self, value):
        try:
            return validate_email(value)
        except BloodBankError as e:
            raise serializers.ValidationError(str(e))

    def validate_blood_group(self, value):
        try:
            return validate_blood_group(value)
        except BloodBankError as e:
            raise serializers.ValidationError(str(e))


class CampSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=150)
    venue = serializers.CharField(max_length=200)
    organizer = serializers.CharField(max_length=150)
    camp_date = serializers.DateField()
    location = serializers.CharField(max_length=100)
    donor_count = serializers.IntegerField(read_only=True, required=False)


class BloodRequestSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    hospital = serializers.CharField(max_length=150)
    blood_group = serializers.CharField(max_length=3)
    location = serializers.CharField(max_length=100)
    units_needed = serializers.IntegerField(min_value=1, default=1)
    urgency = serializers.ChoiceField(choices=['low', 'normal', 'high', 'critical'], default='normal')
    fulfilled = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate_blood_group(self, value):
        try:
            return validate_blood_group(value)
        except BloodBankError as e:
            raise serializers.ValidationError(str(e))