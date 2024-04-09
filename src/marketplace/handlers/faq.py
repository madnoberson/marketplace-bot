from typing import Sequence

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from dishka.integrations.aiogram import FromDishka, inject

from marketplace.entities.faq import FAQ


faq_router = Router()


@faq_router.inline_query()
@inject
async def get_faq(
    inline_query: InlineQuery,
    faq_seq: FromDishka[Sequence[FAQ]],
) -> None:
    def is_fit(faq: FAQ) -> bool:
        return (
            inline_query.query in faq.question
            or inline_query.query in faq.answer
        )

    results = [
        InlineQueryResultArticle(
            id=str(faq.id),
            title=faq.question,
            description=faq.answer,
            input_message_content=InputTextMessageContent(
                message_text=(
                    f"<b>Question:</b> {faq.question}\n\n"
                    f"<b>Answer:</b> {faq.answer}"
                ),
            )
        )
        for faq in filter(is_fit, faq_seq)
    ]

    await inline_query.answer(results=results)
