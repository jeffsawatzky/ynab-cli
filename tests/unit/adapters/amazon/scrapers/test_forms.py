from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup
from callee import StartsWith
from yarl import URL

from tests import fixture_exists, load_fixture
from ynab_cli.adapters.amazon.browser import Browser, BrowserResponse
from ynab_cli.adapters.amazon.models.form import Form
from ynab_cli.adapters.amazon.scrapers.forms import (
    CfvRequestCaptchaFormScraper,
    PpwWidgetNextPageFormScraper,
    SignInCaptchaFormScraper,
    SignInFormScraper,
)
from ynab_cli.domain.ports.io import IO


@pytest.mark.asyncio
async def test_signin_form_scraper__failed() -> None:
    # Given
    mock_browser = MagicMock(spec=Browser)
    mock_io = MagicMock(spec=IO)

    fixture = """<html />"""
    html = BeautifulSoup(fixture, "html.parser")

    # When
    sut = SignInFormScraper("username", "password", mock_browser, mock_io)
    form = await sut.scrape(URL("https://www.amazon.com"), html)

    # Then
    assert form is None


@pytest.mark.skipif(
    not fixture_exists("adapters/amazon/pages/amazon_ap_signin.html"),
    reason="Skipped, to debug the signin page, place it at tests/fixtures/adapters/amazon/pages/amazon_ap_signin.html",
)
@pytest.mark.asyncio
async def test_signin_form_scraper__success() -> None:
    # Given
    mock_browser = MagicMock(spec=Browser)
    mock_io = MagicMock(spec=IO)

    fixture = load_fixture("adapters/amazon/pages/amazon_ap_signin.html")
    html = BeautifulSoup(fixture, "html.parser")

    # When
    sut = SignInFormScraper("username", "password", mock_browser, mock_io)
    form = await sut.scrape(URL("https://www.amazon.com"), html)

    # Then
    assert form is not None
    assert form.action == StartsWith(
        "https://www.amazon.com/ax/claim/validate?policy_handle=Retail-Checkout&openid.return_to=https%3A%2F%2Fwww.amazon.ca%2Fcpe%2Fyourpayments%2Ftransactions%3F3705366964747893%3D3705366964747893&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&arb=e3fa1ccd-86cd-4345-ba29-37c66f80f4ba&openid.assoc_handle=caflex&openid.mode=checkid_setup"
    )
    assert form.method == "post"
    assert form.data == {
        "aaToken": "aa-token",
        "anti-csrftoken-a2z": "hDNR1iauRHKX4IroEq8o4yiJNmKd+W6Jc4qiRkAh+gcLAAAAAGedcGcAAAAB",
        "appAction": "SIGNIN_CLAIM_COLLECT",
        "claimCollectionWorkflow": "unified",
        "claimType": "",
        "countryCode": "",
        "email": "username",
        "isServerSideRouting": "",
        "metadata1": "true",
        "password": "password",
        "subPageType": "FullPageUnifiedClaimCollect",
        "unifiedAuthTreatment": "T3",
    }


@pytest.mark.skipif(
    not fixture_exists("adapters/amazon/pages/amazon_ap_signin__captcha.html"),
    reason="Skipped, to debug the signin captcha page, place it at tests/fixtures/adapters/amazon/pages/amazon_ap_signin__captcha.html",
)
@pytest.mark.asyncio
async def test_signin_captcha_form_scraper__success() -> None:
    # Given
    mock_io = MagicMock(spec=IO)
    mock_io.prompt.return_value = "captcha"

    mock_image_response = MagicMock(spec=BrowserResponse)
    mock_image_response.read.return_value = b"image"

    mock_request_ctxmngr = MagicMock()
    mock_request_ctxmngr.__aenter__.return_value = mock_image_response

    mock_browser = MagicMock(spec=Browser)
    mock_browser.request.return_value = mock_request_ctxmngr

    fixture = load_fixture("adapters/amazon/pages/amazon_ap_signin__captcha.html")
    html = BeautifulSoup(fixture, "html.parser")

    # When
    sut = SignInCaptchaFormScraper(mock_browser, mock_io)
    form = await sut.scrape(URL("https://www.amazon.com"), html)

    # Then
    mock_io.display_image.assert_awaited()
    mock_browser.request.assert_called_once_with(
        URL("https://images-na.ssl-images-amazon.com/captcha/bcxmjlko/Captcha_dygxpkgbov.jpg")
    )
    assert form is not None
    assert form == Form(
        action="https://www.amazon.com/errors/validateCaptcha",
        method="get",
        data={
            "amzn": "/fpDYTJx7Erpw3yVzPkWJw==",
            "amzn-r": "/ap/signin?openid.pape.max_auth_age=3600&openid.return_to=https://www.amazon.com/cpe/yourpayments/transactions&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&language=EN_US&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.ns=http://specs.openid.net/auth/2.0",
            "amzn-pt": "AuthenticationPortal",
            "field-keywords": "captcha",
        },
    )


@pytest.mark.skipif(
    not fixture_exists("adapters/amazon/pages/amazon_ap_cvf_request__captcha.html"),
    reason="Skipped, to debug the request captcha page, place it at tests/fixtures/adapters/amazon/pages/amazon_ap_cvf_request__captcha.html",
)
@pytest.mark.asyncio
async def test_cfv_request_captcha_form_scraper__success() -> None:
    # Given
    mock_io = MagicMock(spec=IO)
    mock_io.prompt.return_value = "captcha"

    mock_image_response = MagicMock(spec=BrowserResponse)
    mock_image_response.read.return_value = b"image"

    mock_request_ctxmngr = MagicMock()
    mock_request_ctxmngr.__aenter__.return_value = mock_image_response

    mock_browser = MagicMock(spec=Browser)
    mock_browser.request.return_value = mock_request_ctxmngr

    fixture = load_fixture("adapters/amazon/pages/amazon_ap_cvf_request__captcha.html")
    html = BeautifulSoup(fixture, "html.parser")

    # When
    sut = CfvRequestCaptchaFormScraper(mock_browser, mock_io)
    form = await sut.scrape(URL("https://www.amazon.ca/ap/cvf/request"), html)

    # Then
    mock_io.display_image.assert_awaited()
    mock_browser.request.assert_called_once_with(
        URL(
            "https://opfcaptcha-prod.s3.amazonaws.com/e815ee3c77c544d196106002395d403a.jpg?AWSAccessKeyId=AKIA5WBBRBBB27TDSHCK&Expires=1729748642&Signature=6td2IvXhOATZawmYqC6sygfysx4%3D"
        ),
    )
    assert form is not None
    assert form == Form(
        action="https://www.amazon.ca/ap/cvf/verify",
        method="post",
        data={
            "cvf_captcha_captcha_token": "LZG+bu8Bpm8xWVaTf39/fwAAAAAAAAAB/Zcl2YCxk/QUqJ4Br6HE1/BVGoR9rmtfu45vdgqCXKjB4br3bHyCpHA/OqwulwFask2ifu2Pw2KWFYmpNqChEOctLALzOa2eiLG+r00pFXbYV9PDpYxrvtyPmANbCMEX8rau87fSWN/hyd4C0d/RpoY3EyWRHhk4TyzT9hRDVBDtTguiF0barMhVXVu/2bf489w8AkEK28VCBxE5/ECJsaZuvyC6wbMAjCPp3/gfQcevkVPCyROPK0nl3GqYFCAP1e12qW4VVleecPHmFaGD/+LJ/D7u1TI9oEGdSxQYScc3iEMyDGHeID/JOdYGMR16iPmSqS8XOexb",
            "cvf_captcha_captcha_type": "imageCaptcha",
            "cvf_captcha_js_enabled_metric": "0",
            "clientContext": "135-9390495-3588138",
            "openid.pape.max_auth_age": "3600",
            "openid.return_to": "https://www.amazon.com/cpe/yourpayments/transactions",
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.assoc_handle": "usflex",
            "openid.mode": "checkid_setup",
            "marketPlaceId": "ATVPDKIKX0DER",
            "isSHuMAAuthenticable": "false",
            "language": "en_CA",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
            "pageId": "usflex",
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "verifyToken": "s|576c1df8-8653-3115-bc4f-df7ec8d163af",
            "cvf_captcha_input": "captcha",
            "cvf_captcha_captcha_action": "verifyCaptcha",
        },
    )


@pytest.mark.skipif(
    not fixture_exists("adapters/amazon/pages/amazon_cpe_yourpayments_transactions.html"),
    reason="Skipped, to debug the transactions next page form, place it at tests/fixtures/adapters/amazon/pages/amazon_cpe_yourpayments_transactions.html",
)
@pytest.mark.asyncio
async def test_ppw_widget_next_page_form_scraper__success() -> None:
    # Given
    mock_browser = MagicMock(spec=Browser)
    mock_io = MagicMock(spec=IO)

    fixture = load_fixture("adapters/amazon/pages/amazon_cpe_yourpayments_transactions.html")
    html = BeautifulSoup(fixture, "html.parser")

    # When
    sut = PpwWidgetNextPageFormScraper(mock_browser, mock_io)
    form = await sut.scrape(URL("https://www.amazon.com"), html)

    # Then
    assert form is not None
    assert form == Form(
        action="https://www.amazon.ca/cpe/yourpayments/transactions",
        method="post",
        data={
            "ppw-widgetState": "dsfgefwc2938r793nyr49cybn",
            "ie": "UTF-8",
            'ppw-widgetEvent:DefaultNextPageNavigationEvent:{"nextPageKey":"skjdfh"}': "",
        },
    )
