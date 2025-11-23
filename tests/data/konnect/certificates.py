# Mock data for Kong Konnect Certificates API responses

KONNECT_CERTIFICATES_RESPONSE = {
    "data": [
        {
            "id": "cert-123",
            "cert": (
                "-----BEGIN CERTIFICATE-----\n"
                "MIIFverylongcertdatathatislongenoughfortruncationcheckAAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH"
                "IIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSS\n"
                "-----END CERTIFICATE-----\n"
            ),
            "snis": ["api.example.com", "www.example.com"],
            "tags": ["production", "ssl"],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:22:00Z",
        },
        {
            "id": "cert-456",
            "cert": (
                "-----BEGIN CERTIFICATE-----\n"
                "MIIFanothertestcertificatepayloadthatshouldtriggertruncationAAAA1111BBBB2222CCCC3333DDDD"
                "4444EEEE5555FFFF6666GGGG7777HHHH\n"
                "-----END CERTIFICATE-----\n"
            ),
            "snis": ["payments.example.com"],
            "tags": ["production"],
            "created_at": "2024-02-01T08:15:00Z",
            "updated_at": "2024-02-05T16:45:00Z",
        },
    ],
    "next": None,
}
