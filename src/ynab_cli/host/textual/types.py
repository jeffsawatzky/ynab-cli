from typing import Literal

from ynab_cli.domain.use_cases import amazon as amazon_use_cases
from ynab_cli.domain.use_cases import categories as categories_use_cases
from ynab_cli.domain.use_cases import payees as payees_use_cases
from ynab_cli.domain.use_cases import transactions as transactions_use_cases

AmazonTabId = Literal["amazon"]
AmazonListTransactionsTabId = tuple[AmazonTabId, Literal["list_transactions"]]
AmazonListTransactionsCommandParams = tuple[AmazonListTransactionsTabId, amazon_use_cases.ListTransactionsParams]

CategoriesTabId = Literal["categories"]
CategoriesListUnusedTabId = tuple[CategoriesTabId, Literal["list_unused"]]
CategoriesListAllTabId = tuple[CategoriesTabId, Literal["list_all"]]
CategoriesListUnusedCommandParams = tuple[CategoriesListUnusedTabId, categories_use_cases.ListUnusedParams]
CategoriesListAllCommandParams = tuple[CategoriesListAllTabId, categories_use_cases.ListAllParams]

PayeesTabId = Literal["payees"]
PayeesNormalizeNamesTabId = tuple[PayeesTabId, Literal["normalize_names"]]
PayeesListDuplicatesTabId = tuple[PayeesTabId, Literal["list_duplicates"]]
PayeesListUnusedTabId = tuple[PayeesTabId, Literal["list_unused"]]
PayeesNormalizeNamesCommandParams = tuple[PayeesNormalizeNamesTabId, payees_use_cases.NormalizeNamesParams]
PayeesListDuplicatesCommandParams = tuple[PayeesListDuplicatesTabId, payees_use_cases.ListDuplicatesParams]
PayeesListUnusedCommandParams = tuple[PayeesListUnusedTabId, payees_use_cases.ListUnusedParams]

TransactionsTabId = Literal["transactions"]
TransactionsApplyRulesTabId = tuple[TransactionsTabId, Literal["apply_rules"]]
TransactionsApplyRulesCommandParams = tuple[TransactionsApplyRulesTabId, transactions_use_cases.ApplyRulesParams]

ActiveTabId = (
    AmazonListTransactionsTabId
    | CategoriesListUnusedTabId
    | CategoriesListAllTabId
    | PayeesNormalizeNamesTabId
    | PayeesListDuplicatesTabId
    | PayeesListUnusedTabId
    | TransactionsApplyRulesTabId
)

CommandParams = (
    AmazonListTransactionsCommandParams
    | CategoriesListUnusedCommandParams
    | CategoriesListAllCommandParams
    | PayeesNormalizeNamesCommandParams
    | PayeesListDuplicatesCommandParams
    | PayeesListUnusedCommandParams
    | TransactionsApplyRulesCommandParams
)
