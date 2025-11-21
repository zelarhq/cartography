import cartography.intel.konnect.dp_nodes
from tests.data.konnect.dp_nodes import KONNECT_DP_NODES_RESPONSE


def test_transform_dp_nodes():
    """
    Ensure that transform_dp_nodes() returns a list of DP nodes with correct fields.
    """
    dp_nodes_data = KONNECT_DP_NODES_RESPONSE["data"]
    transformed = cartography.intel.konnect.dp_nodes.transform(
        dp_nodes_data,
        "cp-123",
    )
    
    assert len(transformed) == 2
    
    node1 = transformed[0]
    assert node1["id"] == "dp-node-123"
    assert node1["hostname"] == "dp-node-1.example.com"
    assert node1["version"] == "3.4.0"
    assert node1["status"] == "connected"
    assert node1["last_ping"] == "2024-01-20T14:22:00Z"
    assert node1["config_hash"] == "abc123def456"
    assert node1["control_plane_id"] == "cp-123"

