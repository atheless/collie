from marshmallow import Schema, fields, validates, ValidationError
from sqlalchemy.orm import class_mapper

from security.models import User


class BaseModelSerializer(Schema):
    model = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.model:
            raise ValueError("Model class must be specified in the subclass.")

    def validate_unique(self, data):
        """
        Validate uniqueness of fields marked as unique in the model.
        """
        errors = {}
        for field_name, field_value in data.items():
            if hasattr(self.model, field_name) and class_mapper(self.model).get_property(field_name).unique:
                query = self.session.query(self.model).filter(getattr(self.model, field_name) == field_value)
                if self.instance:
                    query = query.filter(self.model.id != self.instance.id)
                if query.count() > 0:
                    errors[field_name] = f"{field_name.capitalize()} must be unique."
        if errors:
            raise ValidationError(errors)

    def load(self, data, instance=None, session=None, *args, **kwargs):
        """
        Deserialize data and optionally bind it to an existing instance.
        """
        self.session = session
        self.instance = instance
        loaded_data, errors = super().load(data, *args, **kwargs)
        if errors:
            raise ValidationError(errors)
        if instance:
            for key, value in loaded_data.items():
                setattr(instance, key, value)
        return instance or self.model(**loaded_data)

    def dump(self, obj, *args, **kwargs):
        """
        Serialize an object to a dictionary.
        """
        return super().dump(obj, *args, **kwargs)



class UserSerializer(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)

    @validates('password')
    def validate_password(self, value):
        if value == '12345':
            raise ValidationError("Password cannot be '12345'.")

    def is_valid(self, data=None):
        if not data:
            raise ValidationError('No data')
        try:
            self.load(data)
        except ValidationError as e:
            return False
        return True

    class Meta:
        model = User
