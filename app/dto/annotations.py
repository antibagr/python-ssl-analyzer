import typing as t

TestSSLRecord = t.TypedDict(
    "Record",
    {
        "id": str,
        "ip": str,
        "port": str,
        "severity": str,
        "finding": str,
    },
)

TestSSLRecords = list[TestSSLRecord]
Domain = t.NewType("Domain", str)
