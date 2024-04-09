from typing import Sequence

import openpyxl


async def update_orders_exel(
    user_id: int,
    product_ids: Sequence[int],
    total_price: int,
) -> None:
    ...
