from app.openai.openai_client import OpenAIClient
from app.scripts.prompt import build_prompt

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from typing import Iterator

router = APIRouter()


@router.post("/ask")
async def rag_endpoint(request: Request) -> StreamingResponse:
    data = await request.json()
    query = data.get("query", "")

    openai_client = OpenAIClient()

    if openai_client.count_tokens(query) > 512:

        def error_stream():
            yield "event: error\ndata: Query exceeds token limit.\n\n"

        return StreamingResponse(error_stream(), media_type="text/event-stream")

    prompt = build_prompt(query)

    def event_generator() -> Iterator[str]:
        try:
            for chunk in openai_client.chat_completion_stream(prompt):
                if chunk:
                    yield chunk
            yield "event: done\ndata: [DONE]\n\n"
        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
