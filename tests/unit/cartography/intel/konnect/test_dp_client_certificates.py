import cartography.intel.konnect.dp_client_certificates
from tests.data.konnect.dp_client_certificates import KONNECT_DP_CLIENT_CERTIFICATES_RESPONSE


def test_transform_dp_client_certificates():
    """
    Ensure that transform_dp_client_certificates() truncates cert data and returns correct fields.
    """
    certs_data = KONNECT_DP_CLIENT_CERTIFICATES_RESPONSE["data"]
    transformed = cartography.intel.konnect.dp_client_certificates.transform(
        certs_data,
        "cp-123",
    )
    
    assert len(transformed) == 2
    
    cert1 = transformed[0]
    assert cert1["id"] == "dp-client-cert-123"
    assert cert1["control_plane_id"] == "cp-123"
    assert cert1["created_at"] == "2024-01-15T10:30:00Z"
    
    # Check that cert is truncated
    assert len(cert1["cert"]) <= 103  # 100 chars + "..."
    assert cert1["cert"].endswith("...")

