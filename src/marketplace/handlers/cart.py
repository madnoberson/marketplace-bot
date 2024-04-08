from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka, inject

from marketplace.callbacks import catalog as catalog_callbacks
from marketplace.callbacks import cart as callbacks
from marketplace.keyboards import cart as keyboards
from marketplace.services.get_product_with_id import GetProductWithId
from marketplace.services.add_product_to_cart import AddProductToCart
from marketplace.services.get_cart_item import GetCartItem


cart_router = Router()


@cart_router.callback_query(
    catalog_callbacks.AddProductToCart.filter(),
)
@inject
async def add_product_to_cart(
    callback: CallbackQuery,
    callback_data: catalog_callbacks.AddProductToCart,
    state: FSMContext,
    get_product_with_id: FromDishka[GetProductWithId],
    add_product_to_cart: FromDishka[AddProductToCart],
    get_cart_item: FromDishka[GetCartItem],
) -> None:
    product = await get_product_with_id(
        product_id=callback_data.product_id,
    )
    await add_product_to_cart(
        product=product,
        quantity=callback_data.quantity,
        user_id=callback.message.chat.id,
    )
    get_cart_item_result = await get_cart_item(
        user_id=callback.message.chat.id,
        number=1,
    )
    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Quantity you chose: {callback_data.quantity}\n\n"
        f"Total price for product: {product.price * callback_data.quantity}"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=get_cart_item_result.cart_item,
        cart_items_total_number=get_cart_item_result.total_number,
        current_number=1,
    )

    await state.clear()
    await callback.message.answer(text="<b>Your cart:</b>")
    await callback.message.answer(
        text=text,
        reply_markup=reply_markup,
    )
    await callback.answer()


@cart_router.message(Command("cart"))
@inject
async def get_cart(
    message: Message,
    get_cart_item: FromDishka[GetCartItem],
    get_product_with_id: FromDishka[GetProductWithId],
) -> None:
    get_cart_item_result = await get_cart_item(
        user_id=message.chat.id,
        number=1,
    )
    if not get_cart_item_result.cart_item:
        await message.answer(
            text="<b>No products in cart</b>",
        )
        return

    product = await get_product_with_id(
        product_id=get_cart_item_result.cart_item.product_id,
    )
    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Quantity you chose: {get_cart_item_result.cart_item.quantity}\n\n"
        "Total price for product: "
        f"{product.price * get_cart_item_result.cart_item.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=get_cart_item_result.cart_item,
        cart_items_total_number=get_cart_item_result.total_number,
        current_number=1,
    )

    await message.answer(text="<b>Your cart:</b>")
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@cart_router.callback_query(callbacks.GetCartItem.filter())
@inject
async def get_cart_item(
    callback: CallbackQuery,
    callback_data: callbacks.GetCartItem,
    get_cart_item: FromDishka[GetCartItem],
    get_product_with_id: FromDishka[GetProductWithId],
) -> None:
    get_cart_item_result = await get_cart_item(
        user_id=callback.message.chat.id,
        number=callback_data.cart_item_number,
    )
    product = await get_product_with_id(
        product_id=get_cart_item_result.cart_item.product_id,
    )
    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Quantity you chose: {get_cart_item_result.cart_item.quantity}\n\n"
        "Total price for product: "
        f"{product.price * get_cart_item_result.cart_item.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=get_cart_item_result.cart_item,
        cart_items_total_number=get_cart_item_result.total_number,
        current_number=callback_data.cart_item_number,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )
