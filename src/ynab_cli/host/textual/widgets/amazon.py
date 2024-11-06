import logging
from typing import ClassVar

from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import DataTable, Log, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualWorkerIO
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import amazon as use_cases
from ynab_cli.host.textual.types import ActiveTabId, AmazonListTransactionsTabId, AmazonTabId, CommandParams
from ynab_cli.host.textual.widgets import BaseCommand, CommandRunnableWidget

log = logging.getLogger(__name__)

AMAZON_TAB_ID: AmazonTabId = "amazon"
AMAZON_LIST_TRANSACTIONS_TAB_ID: AmazonListTransactionsTabId = (AMAZON_TAB_ID, "list_transactions")


class AmazonTabs(CommandRunnableWidget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id=AMAZON_LIST_TRANSACTIONS_TAB_ID[1]):
                yield AmazonListTransactionsCommand().data_bind(settings=AmazonTabs.settings)

    @override
    def run_command(self, params: CommandParams) -> None:
        active_tab_id, _ = params
        if active_tab_id == AMAZON_LIST_TRANSACTIONS_TAB_ID:
            self.query_one(TabbedContent).active = AMAZON_LIST_TRANSACTIONS_TAB_ID[1]
            self.query_one(AmazonListTransactionsCommand).run_command(params)


class AmazonListTransactionsCommand(BaseCommand[use_cases.ListTransactionsParams]):
    ACTIVE_TAB_ID: ClassVar[ActiveTabId] = AMAZON_LIST_TRANSACTIONS_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Completed Date",
            "Payment Method",
            "Order Id",
            "Order Link",
            "Seller",
            "Is Refund",
            "Is Gift Card",
            "Grand Total",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.ListTransactionsParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for transaction_group in use_cases.list_transactions(
            self.settings, TextualWorkerIO(self.app, log), use_case_params
        ):
            for transaction in transaction_group.transactions:
                table.add_row(
                    transaction.completed_date.isoformat(),
                    transaction.payment_method,
                    transaction.order_id,
                    transaction.order_link,
                    transaction.seller,
                    str(transaction.is_refund),
                    str(transaction.is_gift_card),
                    str(transaction.grand_total),
                )

                for shipment in transaction.order.shipments:
                    for item in shipment.items:
                        table.add_row(
                            "",
                            "",
                            item.product_id,
                            item.product_link,
                            (item.title[:97] + "...") if len(item.title) > 100 else item.title,
                            ",".join(item.product.categories),
                            str(item.total_price),
                            "",
                        )
