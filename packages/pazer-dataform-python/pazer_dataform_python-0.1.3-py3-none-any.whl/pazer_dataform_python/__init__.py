import time
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class DataFormModel(BaseModel):
    class Config:
        validate_assignment = True

class DataSubForm(DataFormModel):
    items: list | None = None
    rows: int | None = None
    ids: int | None = None

    def toData(self) -> dict:
        return {k: v for k, v in {
            "status": self.items is not None or self.rows is not None or self.ids is not None,
            "items": self.items,
            "count": len(self.items) if self.items else None,
            "rows": self.rows,
            "ids": self.ids
        }.items() if v is not None}

class DataTimeForm(DataFormModel):
    start: float = time.time()
    end: float = 0.0
    run: float = 0.0

    def timeEnd(self) -> None:
        self.end = time.time()
        self.run = round(self.end - self.start, 3)

class DataForm(DataFormModel):
    status: bool = False
    message: str = ""
    execute: bool = False
    timer: bool = False
    data: DataSubForm = DataSubForm()
    time: DataTimeForm = DataTimeForm()

class ResponseForm(DataFormModel):
    status: bool = False
    message: str | None = None
    timer: bool = False
    statusCode: int = 500
    data: DataSubForm = DataSubForm()
    time: DataTimeForm = DataTimeForm()

    def toResponseJSON(self) -> JSONResponse:
        if self.timer:
            self.time.timeEnd()
        form = {
            "status": self.status,
            "message": self.message,
            "data": self.data.toData() if self.status else None,
            "time": self.time.__dict__ if self.timer else None
        }
        return JSONResponse(
            status_code=self.statusCode,
            content={k: v for k, v in form.items() if v is not None}
        )