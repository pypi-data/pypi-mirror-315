from pydantic import BaseModel


class ListResult(BaseModel):
    name: str
    success: bool
    message: list[str]


class Result(BaseModel):
    name: str
    success: bool
    message: str

    def __str__(self):
        messages: list[str] = [line.strip() for line in self.message.split("\n") if line.strip()]

        if messages:
            new = ListResult(name=self.name, success=self.success, message=messages)
            return new.model_dump_json(indent=4)

        return self.model_dump_json(indent=4)

    def __repr__(self):
        return self.__str__()
