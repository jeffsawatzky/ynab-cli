from ynab_cli.adapters.ynab import models
from ynab_cli.domain.use_cases import categories as use_cases


def test_should_skip_category_or_group__with_category() -> None:
    assert (
        use_cases.should_skip_category_or_group(
            category_or_group=models.Category(
                id="",
                category_group_id="",
                name="Category",
                activity=0,
                balance=0,
                budgeted=0,
                hidden=False,
                deleted=False,
            )
        )
        is False
    )

    assert (
        use_cases.should_skip_category_or_group(
            category_or_group=models.Category(
                id="",
                category_group_id="",
                name="Category",
                activity=0,
                balance=0,
                budgeted=0,
                hidden=False,
                deleted=True,
            )
        )
        is True
    )


def test_should_skip_category_or_group__with_category_group() -> None:
    assert (
        use_cases.should_skip_category_or_group(
            category_or_group=models.CategoryGroupWithCategories(
                id="",
                name="Category",
                hidden=False,
                categories=[],
                deleted=False,
            )
        )
        is False
    )

    assert (
        use_cases.should_skip_category_or_group(
            category_or_group=models.CategoryGroupWithCategories(
                id="",
                name="Category",
                hidden=False,
                categories=[],
                deleted=True,
            )
        )
        is True
    )
