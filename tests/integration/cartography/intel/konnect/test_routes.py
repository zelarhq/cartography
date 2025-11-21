from unittest.mock import patch

import cartography.intel.konnect.control_planes
import cartography.intel.konnect.routes
import cartography.intel.konnect.services
import tests.data.konnect.control_planes
import tests.data.konnect.routes
import tests.data.konnect.services
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789
TEST_ORG_ID = "org-123"


def _ensure_local_neo4j_has_test_control_planes_and_services(neo4j_session):
    """Helper to ensure control planes and services exist before testing routes."""
    # Load control planes
    cartography.intel.konnect.control_planes.load_control_planes(
        neo4j_session,
        cartography.intel.konnect.control_planes.transform(
            tests.data.konnect.control_planes.KONNECT_CONTROL_PLANES_RESPONSE["data"],
            TEST_ORG_ID,
        ),
        TEST_ORG_ID,
        TEST_UPDATE_TAG,
    )
    # Load services
    cartography.intel.konnect.services.load_services(
        neo4j_session,
        cartography.intel.konnect.services.transform(
            tests.data.konnect.services.KONNECT_SERVICES_RESPONSE["data"],
            "cp-123",
        ),
        "cp-123",
        TEST_UPDATE_TAG,
    )


def _mock_get_routes(api_token, api_url, control_plane_id):
    """Mock get function that only returns data for cp-123."""
    if control_plane_id == "cp-123":
        return tests.data.konnect.routes.KONNECT_ROUTES_RESPONSE["data"]
    return []


@patch.object(
    cartography.intel.konnect.routes,
    "get",
    side_effect=_mock_get_routes,
)
def test_load_routes(mock_api, neo4j_session):
    """
    Ensure that routes actually get loaded with correct relationships to control planes and services.
    """
    # Arrange
    _ensure_local_neo4j_has_test_control_planes_and_services(neo4j_session)
    api_token = "test-token"
    api_url = "https://us.api.konghq.com/v2"
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
    }

    # Act
    cartography.intel.konnect.routes.sync(
        neo4j_session,
        api_token,
        api_url,
        TEST_UPDATE_TAG,
        common_job_parameters,
    )

    # Assert Routes exist
    expected_nodes = {
        ("route-123", "user-api-route"),
        ("route-456", "payment-api-route"),
    }
    assert (
        check_nodes(neo4j_session, "KonnectRoute", ["id", "name"])
        == expected_nodes
    )

    # Assert Routes are connected with Control Planes (ControlPlane -> Route)
    expected_cp_rels = {
        ("cp-123", "route-123"),
        ("cp-123", "route-456"),
    }
    assert (
        check_rels(
            neo4j_session,
            "KonnectControlPlane",
            "id",
            "KonnectRoute",
            "id",
            "RESOURCE",
            rel_direction_right=True,
        )
        == expected_cp_rels
    )

    # Assert Routes are connected with Services (Route -> Service)
    expected_service_rels = {
        ("route-123", "svc-123"),
        ("route-456", "svc-456"),
    }
    assert (
        check_rels(
            neo4j_session,
            "KonnectRoute",
            "id",
            "KonnectService",
            "id",
            "ROUTES_TO",
            rel_direction_right=True,
        )
        == expected_service_rels
    )

