from __future__ import annotations

from typing import Iterable, Optional

from fastapi import Body, FastAPI, HTTPException, status
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel

from render import Render, config

render_engines = {size: Render(size) for size in config.SIZES}


class Board(BaseModel):
    field: list[list[str]] = [
        ["R", "H", "B", "Q", "K", "B", "H", "R"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["r", "h", "b", "q", "k", "b", "h", "r"]
    ]
    white: bool = True
    picked: Optional[list[Iterable[int]]]
    move: Optional[list[Iterable[int]]]
    beat: Optional[list[Iterable[int]]]
    check: Optional[list[Iterable[int]]]


app = FastAPI(title="ChessRenderAPI")


@app.get("/sizes", response_model=list[int])
async def sizes():
    return JSONResponse(content=config.SIZES, headers={
        "Access-Control-Allow-Origin": "*"
    })


@app.get("/render")
@app.post("/render", response_class=Response, responses={
    200: {"content": {"image/png": {}}}
})
async def convert(size: int = config.SIZES[0], board: Board = Body(default=Board())):
    if size not in config.SIZES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid size")
    image = render_engines[size].render(**board.dict())
    return Response(image, media_type="image/png", headers={
        "Access-Control-Allow-Origin": "*"
    })
