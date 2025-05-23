from app.openai.openai_client import OpenAIClient
from app.scripts.prompt import build_prompt

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from typing import Iterator

router = APIRouter()


@router.post("/conversation")
async def conversation_endpoint(request: Request) -> StreamingResponse:
    data = await request.json()
    query = data.get("query", "")
    query = query.strip()

    try:
        openai_client = OpenAIClient()
    except Exception as e:

        def error_stream():
            yield "event: error\ndata: Something went wrong internally, please try again later.\n\n"

        return StreamingResponse(error_stream(), media_type="text/event-stream")

    token_count = openai_client.count_tokens(query)
    if token_count == 0 or token_count > 512:

        def error_stream():
            yield "event: error\ndata: Query must be between 1 and 512 tokens.\n\n"

        return StreamingResponse(error_stream(), media_type="text/event-stream")

    prompt = build_prompt(query, openai_client)

    def event_generator() -> Iterator[str]:
        try:
            for chunk in openai_client.chat_completion_stream(prompt):
                if chunk:
                    yield chunk
            yield "event: done\ndata: [DONE]\n\n"
        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
