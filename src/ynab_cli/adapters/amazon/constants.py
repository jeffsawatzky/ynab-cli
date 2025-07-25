from httpx import URL

DEFAULT_AMAZON_HOST = "www.amazon.com"


class Routes:
    SIGN_IN = URL("/gp/sign-in.html")
    SIGN_IN_REFERER = URL("/ap/signin")
    TRANSACTIONS = URL("/cpe/yourpayments/transactions")
    REFUNDS = URL("/spr/returns/cart?orderId=order_id")
