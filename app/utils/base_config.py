from sqlmodel import SQLModel


class BaseConfigSchema(SQLModel):
    class Config:
        populate_by_name = True
