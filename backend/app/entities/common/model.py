from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    def update(self, **new_data):
        for field, value in new_data.items():
            setattr(self, field, value)
