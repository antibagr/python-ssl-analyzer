import json
import typing as t

import pytest

from app.dto.annotations import TestSSLRecords
from app.dto.entities.fqdn import FQDN
from app.dto.exceptions import TestSSLScanError as ScanError
from app.lib.testssl.parser import TestSSLJsonParser as SSLParser


def get_testssl_scan_data(filename: str) -> TestSSLRecords:
    with open(f"tests/units/test_app/data/{filename}", "r", encoding="utf-8") as f:
        return t.cast(TestSSLRecords, json.loads(f.read()))


@pytest.fixture()
def parser() -> SSLParser:
    return SSLParser()


def test_parser_success(parser: SSLParser) -> None:
    data = get_testssl_scan_data("success.json")
    result = parser.parse(data=data)
    assert isinstance(result, FQDN)

    assert result.fqdn == "google.com"
    assert result.alt_names == {
        "*.2mdn-cn.net",
        "*.admob-cn.com",
        "*.ampproject.net.cn",
        "*.ampproject.org.cn",
        "*.android.com",
        "*.app-measurement-cn.com",
        "*.appengine.google.com",
        "*.bdn.dev",
        "*.cloud.google.com",
        "*.crowdsource.google.com",
        "*.dartsearch-cn.net",
        "*.datacompute.google.com",
        "*.doubleclick-cn.net",
        "*.doubleclick.cn",
        "*.flash.android.com",
        "*.fls.doubleclick-cn.net",
        "*.fls.doubleclick.cn",
        "*.g.cn",
        "*.g.co",
        "*.g.doubleclick-cn.net",
        "*.g.doubleclick.cn",
        "*.gcp.gvt2.com",
        "*.gcpcdn.gvt1.com",
        "*.ggpht.cn",
        "*.gkecnapps.cn",
        "*.google-analytics-cn.com",
        "*.google-analytics.com",
        "*.google.ca",
        "*.google.cl",
        "*.google.co.in",
        "*.google.co.jp",
        "*.google.co.uk",
        "*.google.com",
        "*.google.com.ar",
        "*.google.com.au",
        "*.google.com.br",
        "*.google.com.co",
        "*.google.com.mx",
        "*.google.com.tr",
        "*.google.com.vn",
        "*.google.de",
        "*.google.es",
        "*.google.fr",
        "*.google.hu",
        "*.google.it",
        "*.google.nl",
        "*.google.pl",
        "*.google.pt",
        "*.googleadapis.com",
        "*.googleadservices-cn.com",
        "*.googleapis-cn.com",
        "*.googleapis.cn",
        "*.googleapps-cn.com",
        "*.googlecnapps.cn",
        "*.googlecommerce.com",
        "*.googledownloads.cn",
        "*.googleflights-cn.net",
        "*.googleoptimize-cn.com",
        "*.googlesandbox-cn.com",
        "*.googlesyndication-cn.com",
        "*.googletagmanager-cn.com",
        "*.googletagservices-cn.com",
        "*.googletraveladservices-cn.com",
        "*.googlevads-cn.com",
        "*.googlevideo.com",
        "*.gstatic-cn.com",
        "*.gstatic.cn",
        "*.gstatic.com",
        "*.gvt1-cn.com",
        "*.gvt1.com",
        "*.gvt2-cn.com",
        "*.gvt2.com",
        "*.metric.gstatic.com",
        "*.origin-test.bdn.dev",
        "*.recaptcha-cn.net",
        "*.recaptcha.net.cn",
        "*.safeframe.googlesyndication-cn.com",
        "*.safenup.googlesandbox-cn.com",
        "*.urchin.com",
        "*.url.google.com",
        "*.widevine.cn",
        "*.youtube-nocookie.com",
        "*.youtube.com",
        "*.youtubeeducation.com",
        "*.youtubekids.com",
        "*.yt.be",
        "*.ytimg.com",
        "2mdn-cn.net",
        "admob-cn.com",
        "ampproject.net.cn",
        "ampproject.org.cn",
        "android.clients.google.com",
        "android.com",
        "app-measurement-cn.com",
        "dartsearch-cn.net",
        "developer.android.google.cn",
        "developers.android.google.cn",
        "doubleclick-cn.net",
        "doubleclick.cn",
        "g.cn",
        "g.co",
        "ggpht.cn",
        "gkecnapps.cn",
        "goo.gl",
        "google-analytics-cn.com",
        "google-analytics.com",
        "google.com",
        "googleadservices-cn.com",
        "googleapis-cn.com",
        "googleapps-cn.com",
        "googlecnapps.cn",
        "googlecommerce.com",
        "googledownloads.cn",
        "googleflights-cn.net",
        "googleoptimize-cn.com",
        "googlesandbox-cn.com",
        "googlesyndication-cn.com",
        "googletagmanager-cn.com",
        "googletagservices-cn.com",
        "googletraveladservices-cn.com",
        "googlevads-cn.com",
        "gvt1-cn.com",
        "gvt2-cn.com",
        "recaptcha-cn.net",
        "recaptcha.net.cn",
        "source.android.google.cn",
        "urchin.com",
        "widevine.cn",
        "www.goo.gl",
        "youtu.be",
        "youtube.com",
        "youtubeeducation.com",
        "youtubekids.com",
        "yt.be",
    }
    assert result.supported_protocols == ["TLS1", "TLS1_1", "TLS1_2", "TLS1_3"]


def test_parser_no_cert(parser: SSLParser) -> None:
    data = get_testssl_scan_data("no_cert.json")
    result = parser.parse(data=data)
    assert isinstance(result, FQDN)

    assert result.fqdn == "example.com"
    assert not result.alt_names
    assert result.supported_protocols == ["TLS1", "TLS1_1", "TLS1_2", "TLS1_3"]


def test_parser_error(parser: SSLParser) -> None:
    data = get_testssl_scan_data("error.json")
    with pytest.raises(ScanError) as exc:
        parser.parse(data=data)

    assert str(exc.value) == "No IPv4/IPv6 address(es) for 'does_not_exist' available"
