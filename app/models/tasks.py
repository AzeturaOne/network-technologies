from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Починить МФУ HP LaserJet Pro MFP M28w",
                "description": "МФУ перестало печатать, хотя сканирует и копирует. Требуется диагностика и ремонт.",
                "status": "В работе",
            }
        }
    )


class TaskList(BaseModel):
    tasks: list[Task]