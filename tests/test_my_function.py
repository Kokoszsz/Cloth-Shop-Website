
from Web.send_email import generate_verification_code, account_registration_verification, send_email

def test_generate_verification_code():
    code = generate_verification_code()
    assert len(code) == 6

