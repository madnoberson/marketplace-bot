from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncConnection

from marketplace.callbacks import catalog as catalog_callbacks
from marketplace.callbacks import cart as callbacks
from marketplace.keyboards import cart as keyboards
from marketplace.entities.cart_item import CartItem
from marketplace.database.sqlalchemy.mappers import (
    ProductMapper,
    CartItemMapper,
)


cart_router = Router()


@cart_router.callback_query(
    catalog_callbacks.AddProductToCart.filter(),
)
@inject
async def add_product_to_cart(
    callback: CallbackQuery,
    callback_data: catalog_callbacks.AddProductToCart,
    state: FSMContext,
    product_mapper: FromDishka[ProductMapper],
    cart_item_mapper: FromDishka[CartItemMapper],
    db_connection: FromDishka[AsyncConnection],
) -> None:
    product = await product_mapper.with_id(
        product_id=callback_data.product_id,
    )
    if not product:
        await state.clear()
        await callback.message.answer(
            text="<b>Product is out of stock :(</b>"
        )
        await callback.answer()
        return

    cart_item = CartItem(
        id=None,
        user_id=callback.message.chat.id,
        product_id=product.id,
        quantity=callback_data.quantity,
    )
    await cart_item_mapper.save(cart_item)

    await db_connection.commit()

    cart_items_total_number = await cart_item_mapper.count_with_user_id(
        user_id=callback.message.chat.id,
    )

    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Price for a unit: {product.price}\n"
        f"Quantity you chose: {callback_data.quantity}\n\n"
        f"Total price for products: {product.price * callback_data.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=cart_item,
        cart_items_total_number=cart_items_total_number,
        current_number=1,
    )

    await state.clear()
    await callback.message.answer(text="<b>Your cart:</b>")
    await callback.message.answer(
        text=text,
        reply_markup=reply_markup,
    )
    await callback.answer(
        text="Product added to cart",
    )


@cart_router.message(Command("cart"))
@inject
async def get_cart(
    message: Message,
    product_mapper: FromDishka[ProductMapper],
    cart_item_mapper: FromDishka[CartItemMapper],
) -> None:
    cart_item = await cart_item_mapper.with_user_id_and_number(
        user_id=message.chat.id,
        number=1,
    )
    if not cart_item:
        await message.answer(
            text="<b>No products in cart</b>",
        )
        return

    product = await product_mapper.with_id(
        product_id = cart_item.product_id,
    )
    cart_items_total_number = await cart_item_mapper.count_with_user_id(
        user_id=message.chat.id,
    )

    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Price for a unit: {product.price}\n"
        f"Quantity you chose: {cart_item.quantity}\n\n"
        f"Total price for products: {product.price * cart_item.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=cart_item,
        cart_items_total_number=cart_items_total_number,
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
    product_mapper: FromDishka[ProductMapper],
    cart_item_mapper: FromDishka[CartItemMapper],
) -> None:
    cart_item = await cart_item_mapper.with_user_id_and_number(
        user_id=callback.message.chat.id,
        number=callback_data.cart_item_number,
    )
    if not cart_item:
        await callback.message.answer(
            text="<b>No products in cart</b>",
        )
        await callback.answer()
        return

    product = await product_mapper.with_id(
        product_id = cart_item.product_id,
    )
    cart_items_total_number = await cart_item_mapper.count_with_user_id(
        user_id=callback.message.chat.id,
    )

    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Price for a unit: {product.price}\n"
        f"Quantity you chose: {cart_item.quantity}\n\n"
        f"Total price for products: {product.price * cart_item.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=cart_item,
        cart_items_total_number=cart_items_total_number,
        current_number=callback_data.cart_item_number,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )


@cart_router.callback_query(callbacks.DeleteCartItem.filter())
@inject
async def delete_cart_item(
    callback: CallbackQuery,
    callback_data: callbacks.DeleteCartItem,
    product_mapper: FromDishka[ProductMapper],
    cart_item_mapper: FromDishka[CartItemMapper],
    db_connection: FromDishka[AsyncConnection],
) -> None:
    cart_item_number_to_delete = callback_data.cart_item_number

    cart_item = await cart_item_mapper.with_user_id_and_number(
        user_id=callback.message.chat.id,
        number=cart_item_number_to_delete,
    )
    cart_items_total_number_before_deleting = (
        await cart_item_mapper.count_with_user_id(
            user_id=callback.message.chat.id,
        )
    )
    await cart_item_mapper.delete(cart_item)

    await db_connection.commit()

    if cart_items_total_number_before_deleting == 1:
        await callback.message.answer(
            text="<b>No products in cart</b>",
        )
        await callback.answer()
        return

    if cart_item_number_to_delete \
        == cart_items_total_number_before_deleting:
        current_cart_item_number = cart_items_total_number_before_deleting - 1
        current_cart_item = await cart_item_mapper.with_user_id_and_number(
            user_id=callback.message.chat.id,
            number=current_cart_item_number,
        )
    else:
        current_cart_item_number = cart_item_number_to_delete
        current_cart_item = await cart_item_mapper.with_user_id_and_number(
            user_id=callback.message.chat.id,
            number=current_cart_item_number,
        )
    product = await product_mapper.with_id(
        product_id=current_cart_item.product_id,
    )

    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Price for a unit: {product.price}\n"
        f"Quantity you chose: {cart_item.quantity}\n\n"
        f"Total price for products: {product.price * cart_item.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_cart_item(
        cart_item=cart_item,
        cart_items_total_number=cart_items_total_number_before_deleting - 1,
        current_number=current_cart_item_number,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )
    await callback.answer(
        text="Product deleted from cart",
    )
