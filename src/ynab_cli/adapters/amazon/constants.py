from yarl import URL


class Routes:
    SIGN_IN = URL("/gp/sign-in.html", encoded=True)
    SIGN_IN_REFERER = URL("/ap/signin", encoded=True)
    TRANSACTIONS = URL("/cpe/yourpayments/transactions", encoded=True)
    REFUNDS = URL("/spr/returns/cart?orderId={order_id}", encoded=True)


DEFAULT_AMAZON_SCHEME = "https"
DEFAULT_AMAZON_HOST = "www.amazon.com"

DEFAULT_HEADERS: dict[str, str] = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cache-Control": "max-age=0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Viewport-Width": "1393",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Viewport-Width": "1393",
}
