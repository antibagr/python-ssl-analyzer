import typing as t

TestSSLRecord = t.TypedDict(
    "TestSSLRecord",
    {
        "id": str,
        "ip": str,
        "port": str,
        "severity": str,
        "finding": str,
    },
)

TestSSLRecords: t.TypeAlias = list[TestSSLRecord]
Domain = t.NewType("Domain", str)
