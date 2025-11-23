from unittest.mock import patch

import cartography.intel.konnect.control_planes
import tests.data.konnect.control_planes
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789
TEST_ORG_ID = "org-123"


@patch.object(
    cartography.intel.konnect.control_planes,
    "get",
    return_value=tests.data.konnect.control_planes.KONNECT_CONTROL_PLANES_RESPONSE[
        "data"
    ],
)
def test_load_control_planes(mock_api, neo4j_session):
    """
    Ensure that control planes and organization actually get loaded with correct relationships.
    """
    # Arrange
    api_token = "test-token"
    api_url = "https://us.api.konghq.com/v2"
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
    }

    # Act
    cartography.intel.konnect.control_planes.sync(
        neo4j_session,
        api_token,
        api_url,
        TEST_ORG_ID,
        TEST_UPDATE_TAG,
        common_job_parameters,
    )

    # Assert Organization exists
    expected_org_nodes = {
        (TEST_ORG_ID, TEST_ORG_ID),
    }
    assert (
        check_nodes(neo4j_session, "KonnectOrganization", ["id", "name"])
        == expected_org_nodes
    )

    # Assert Control Planes exist
    expected_cp_nodes = {
        ("cp-123", "production-cp"),
        ("cp-456", "staging-cp"),
    }
    assert (
        check_nodes(neo4j_session, "KonnectControlPlane", ["id", "name"])
        == expected_cp_nodes
    )

    # Assert Control Planes are connected with Organization (Organization -> ControlPlane)
    expected_rels = {
        (TEST_ORG_ID, "cp-123"),
        (TEST_ORG_ID, "cp-456"),
    }
    assert (
        check_rels(
            neo4j_session,
            "KonnectOrganization",
            "id",
            "KonnectControlPlane",
            "id",
            "RESOURCE",
            rel_direction_right=True,
        )
        == expected_rels
    )
