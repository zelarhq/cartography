import json

import cartography.intel.konnect.services
from tests.data.konnect.services import KONNECT_SERVICES_RESPONSE


def test_transform_services():
    """
    Ensure that transform_services() returns a list of services with correct fields and converts lists to JSON.
    """
    services_data = KONNECT_SERVICES_RESPONSE["data"]
    transformed = cartography.intel.konnect.services.transform(
        services_data,
        "cp-123",
    )
    
    assert len(transformed) == 2
    
    svc1 = transformed[0]
    assert svc1["id"] == "svc-123"
    assert svc1["name"] == "user-service"
    assert svc1["host"] == "api.example.com"
    assert svc1["port"] == 443
    assert svc1["protocol"] == "https"
    assert svc1["control_plane_id"] == "cp-123"
    
    # Check that lists are converted to JSON strings
    assert isinstance(svc1["ca_certificates"], str)
    ca_certs = json.loads(svc1["ca_certificates"])
    assert ca_certs == ["cert-1", "cert-2"]
    
    assert isinstance(svc1["tags"], str)
    tags = json.loads(svc1["tags"])
    assert tags == ["production", "api"]


def test_transform_services_with_empty_lists():
    """
    Ensure that transform_services() handles empty lists correctly.
    """
    services_data = [
        {
            "id": "svc-empty",
            "name": "empty-service",
            "host": "example.com",
            "port": 443,
            "protocol": "https",
            "path": "/",
            "enabled": True,
            "connect_timeout": 60000,
            "read_timeout": 60000,
            "write_timeout": 60000,
            "retries": 5,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:22:00Z",
            "ca_certificates": [],
            "tags": [],
        },
    ]
    transformed = cartography.intel.konnect.services.transform(
        services_data,
        "cp-123",
    )
    
    svc = transformed[0]
    assert svc["id"] == "svc-empty"
    # Empty lists should remain as empty lists (not converted to JSON)
    assert svc["ca_certificates"] == []
    assert svc["tags"] == []

