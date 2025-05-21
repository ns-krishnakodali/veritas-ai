from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Request

router = APIRouter()


@router.post("/ask")
async def rag_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        query = data.get("query", "")
        print(query)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Server up and running",
            },
        )
    except Exception as _:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
