import enum
import ssl
import typing as t


@t.final
@enum.unique
class ProtocolVersion(enum.IntEnum):
    # SSLv2 = ssl.PROTOCOL_SSLv23
    # SSLv3 = ssl.PROTOCOL_SSLv23
    TLSv1 = ssl.PROTOCOL_TLSv1
    TLSv1_1 = ssl.PROTOCOL_TLSv1_1
    TLSv1_2 = ssl.PROTOCOL_TLSv1_2
    TLSv1_3 = ssl.PROTOCOL_TLS
