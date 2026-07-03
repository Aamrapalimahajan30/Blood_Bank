class BloodBankError(Exception):
    pass


class InvalidBloodGroupError(BloodBankError):
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid blood group format: '{value}'. "f"Expected one of A+, A-, B+, B-, AB+, AB-, O+, O-")


class InvalidPhoneError(BloodBankError):
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid phone number: '{value}'. Expected a 10-digit Indian mobile number.")


class InvalidEmailError(BloodBankError):
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid email address: '{value}'.")


class CampDateError(BloodBankError):
    pass


class NoMatchingDonorError(BloodBankError):
    pass