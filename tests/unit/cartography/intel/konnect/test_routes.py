import json

import cartography.intel.konnect.routes
from tests.data.konnect.routes import KONNECT_ROUTES_RESPONSE


def test_transform_routes():
    """
    Ensure that transform_routes() returns a list of routes with correct fields and converts lists/dicts to JSON.
    """
    routes_data = KONNECT_ROUTES_RESPONSE["data"]
    transformed = cartography.intel.konnect.routes.transform(
        routes_data,
        "cp-123",
    )
    
    assert len(transformed) == 2
    
    route1 = transformed[0]
    assert route1["id"] == "route-123"
    assert route1["name"] == "user-api-route"
    assert route1["control_plane_id"] == "cp-123"
    assert route1["service_id"] == "svc-123"
    
    # Check that lists are converted to JSON strings
    assert isinstance(route1["protocols"], str)
    protocols = json.loads(route1["protocols"])
    assert protocols == ["https", "http"]
    
    assert isinstance(route1["methods"], str)
    methods = json.loads(route1["methods"])
    assert methods == ["GET", "POST"]
    
    # Check that headers dict is converted to JSON string
    assert isinstance(route1["headers"], str)
    headers = json.loads(route1["headers"])
    assert headers == {"X-Custom-Header": "value"}


def test_transform_routes_with_none_headers():
    """
    Ensure that transform_routes() handles None headers correctly.
    """
    routes_data = KONNECT_ROUTES_RESPONSE["data"]
    transformed = cartography.intel.konnect.routes.transform(
        routes_data,
        "cp-123",
    )
    
    route2 = transformed[1]
    assert route2["id"] == "route-456"
    # None headers should remain None
    assert route2["headers"] is None

