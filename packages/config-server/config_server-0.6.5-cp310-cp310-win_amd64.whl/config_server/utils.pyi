from pydantic import BaseModel
from pydantic.json_schema import JsonSchemaValue as JsonSchemaValue
from typing import Any

class ValidationResult(BaseModel):
    result: bool
    detail: list
    @classmethod
    def __get_pydantic_json_schema__(cls, *args, **kwargs) -> JsonSchemaValue: ...

def convert_text_to_comment(comment_text: str, indent: int, indent_level: int = 0): ...
def remove_intent_of_text(text: str) -> str: ...
def get_blank_repr_for_field(field_value: Any): ...

class YamlResponse(BaseModel):
    data: dict
    yaml: str
