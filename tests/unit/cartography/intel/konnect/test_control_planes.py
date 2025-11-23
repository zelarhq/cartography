import cartography.intel.konnect.control_planes
from tests.data.konnect.control_planes import KONNECT_CONTROL_PLANES_RESPONSE


def test_transform_control_planes():
    """
    Ensure that transform_control_planes() returns a list of control planes with correct fields.
    """
    control_planes_data = KONNECT_CONTROL_PLANES_RESPONSE["data"]
    transformed = cartography.intel.konnect.control_planes.transform(
        control_planes_data,
        "org-123",
    )

    assert len(transformed) == 2

    cp1 = transformed[0]
    assert cp1["id"] == "cp-123"
    assert cp1["name"] == "production-cp"
    assert cp1["description"] == "Production control plane"
    assert cp1["created_at"] == "2024-01-15T10:30:00Z"
    assert cp1["updated_at"] == "2024-01-20T14:22:00Z"


def test_transform_control_planes_without_org_id():
    """
    Ensure that transform_control_planes() works when org_id is None.
    """
    control_planes_data = KONNECT_CONTROL_PLANES_RESPONSE["data"]
    transformed = cartography.intel.konnect.control_planes.transform(
        control_planes_data,
        None,
    )

    assert len(transformed) == 2
    assert transformed[0]["id"] == "cp-123"
