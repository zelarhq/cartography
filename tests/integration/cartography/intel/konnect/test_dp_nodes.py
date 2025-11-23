from unittest.mock import patch

import cartography.intel.konnect.control_planes
import cartography.intel.konnect.dp_nodes
import tests.data.konnect.control_planes
import tests.data.konnect.dp_nodes
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789
TEST_ORG_ID = "org-123"


def _ensure_local_neo4j_has_test_control_planes(neo4j_session):
    """Helper to ensure control planes exist before testing DP nodes."""
    cartography.intel.konnect.control_planes.load_control_planes(
        neo4j_session,
        cartography.intel.konnect.control_planes.transform(
            tests.data.konnect.control_planes.KONNECT_CONTROL_PLANES_RESPONSE["data"],
            TEST_ORG_ID,
        ),
        TEST_ORG_ID,
        TEST_UPDATE_TAG,
    )


def _mock_get_dp_nodes(api_token, api_url, control_plane_id):
    """Mock get function that only returns data for cp-123."""
    if control_plane_id == "cp-123":
        return tests.data.konnect.dp_nodes.KONNECT_DP_NODES_RESPONSE["data"]
    return []


@patch.object(
    cartography.intel.konnect.dp_nodes,
    "get",
    side_effect=_mock_get_dp_nodes,
)
def test_load_dp_nodes(mock_api, neo4j_session):
    """
    Ensure that DP nodes actually get loaded with correct relationships to control planes.
    """
    # Arrange
    _ensure_local_neo4j_has_test_control_planes(neo4j_session)
    api_token = "test-token"
    api_url = "https://us.api.konghq.com/v2"
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
    }

    # Act
    cartography.intel.konnect.dp_nodes.sync(
        neo4j_session,
        api_token,
        api_url,
        TEST_UPDATE_TAG,
        common_job_parameters,
    )

    # Assert DP Nodes exist
    expected_nodes = {
        ("dp-node-123", "dp-node-1.example.com"),
        ("dp-node-456", "dp-node-2.example.com"),
    }
    assert (
        check_nodes(neo4j_session, "KonnectDPNode", ["id", "hostname"])
        == expected_nodes
    )

    # Assert DP Nodes are connected with Control Planes (ControlPlane -> DPNode)
    expected_rels = {
        ("cp-123", "dp-node-123"),
        ("cp-123", "dp-node-456"),
    }
    assert (
        check_rels(
            neo4j_session,
            "KonnectControlPlane",
            "id",
            "KonnectDPNode",
            "id",
            "RESOURCE",
            rel_direction_right=True,
        )
        == expected_rels
    )
