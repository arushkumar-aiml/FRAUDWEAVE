import hmac

def verify(authorization, expected):
    """Return None if authorized, else (status_code, message). Pure function so it is unit-testable."""
    if not expected:
        return 503, "Reviewer access is not configured on this server."
    if not authorization or not authorization.startswith("Bearer "):
        return 401, "Reviewer token required."
    if not hmac.compare_digest(authorization[7:].encode(), expected.encode()):
        return 403, "Invalid reviewer token."
    return None
