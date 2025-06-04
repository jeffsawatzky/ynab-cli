from uuid import UUID

from ynab_cli.adapters.ynab import models
from ynab_cli.domain.use_cases import categories as use_cases

uuid = UUID("00000000-0000-0000-0000-000000000000")


def test_should_skip_category_or_group__with_category() -> None:
    assert (
        use_cases._should_skip_category_or_group(
            category_or_group=models.Category(
                id=uuid,
                category_group_id=uuid,
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
        use_cases._should_skip_category_or_group(
            category_or_group=models.Category(
                id=uuid,
                category_group_id=uuid,
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
        use_cases._should_skip_category_or_group(
            category_or_group=models.CategoryGroupWithCategories(
                id=uuid,
                name="Category",
                hidden=False,
                categories=[],
                deleted=False,
            )
        )
        is False
    )

    assert (
        use_cases._should_skip_category_or_group(
            category_or_group=models.CategoryGroupWithCategories(
                id=uuid,
                name="Category",
                hidden=False,
                categories=[],
                deleted=True,
            )
        )
        is True
    )
