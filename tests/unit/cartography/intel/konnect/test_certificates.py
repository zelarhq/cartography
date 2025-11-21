import cartography.intel.konnect.certificates
from tests.data.konnect.certificates import KONNECT_CERTIFICATES_RESPONSE


def test_transform_certificates():
    """
    Ensure that transform_certificates() truncates cert data and returns correct fields.
    """
    certificates_data = KONNECT_CERTIFICATES_RESPONSE["data"]
    transformed = cartography.intel.konnect.certificates.transform(
        certificates_data,
        "cp-123",
    )
    
    assert len(transformed) == 2
    
    cert1 = transformed[0]
    assert cert1["id"] == "cert-123"
    assert cert1["control_plane_id"] == "cp-123"
    assert cert1["snis"] == ["api.example.com", "www.example.com"]
    assert cert1["tags"] == ["production", "ssl"]
    
    # Check that cert is truncated
    assert len(cert1["cert"]) <= 103  # 100 chars + "..."
    assert cert1["cert"].endswith("...")


def test_transform_certificates_short_cert():
    """
    Ensure that transform_certificates() doesn't truncate short certs.
    """
    short_cert_data = [
        {
            "id": "cert-short",
            "cert": "short",
            "snis": [],
            "tags": [],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:22:00Z",
        },
    ]
    transformed = cartography.intel.konnect.certificates.transform(
        short_cert_data,
        "cp-123",
    )
    
    assert transformed[0]["cert"] == "short"
    assert not transformed[0]["cert"].endswith("...")

