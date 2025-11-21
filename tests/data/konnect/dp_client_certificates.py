# Mock data for Kong Konnect DP Client Certificates API responses

KONNECT_DP_CLIENT_CERTIFICATES_RESPONSE = {
    "data": [
        {
            "id": "dp-client-cert-123",
            "cert": (
                "-----BEGIN CERTIFICATE-----\n"
                "MIIFclientcertificatepayloadthatshouldbetruncatedAAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJ"
                "KKKKLLLLMMMMNNNNOOOOPPPPQQQQ\n"
                "-----END CERTIFICATE-----\n"
            ),
            "created_at": "2024-01-15T10:30:00Z",
        },
        {
            "id": "dp-client-cert-456",
            "cert": (
                "-----BEGIN CERTIFICATE-----\n"
                "MIIFanotherclientcertificatepayloadfortruncationBBBB1111CCCC2222DDDD3333EEEE4444FFFF5555"
                "GGGG6666HHHH7777IIII8888\n"
                "-----END CERTIFICATE-----\n"
            ),
            "created_at": "2024-02-01T08:15:00Z",
        },
    ],
    "next": None,
}

