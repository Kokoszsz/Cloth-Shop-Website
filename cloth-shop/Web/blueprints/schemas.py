from typing import Any

from marshmallow import Schema, fields, validate

MINIMUM_RATING = 1
MAXIMUM_RATING = 5


class StrictNumber(fields.Float):
    def _validated(self, value: Any) -> Any:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise self.make_error('invalid')
        return value


class BasketItemSchema(Schema):
    product_id = fields.Integer(required=True, strict=True)


class RatingSchema(Schema):
    rating = StrictNumber(
        required=True,
        validate=validate.Range(min=MINIMUM_RATING, max=MAXIMUM_RATING),
    )


class ReviewSchema(Schema):
    content = fields.String(required=True)


class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    cost = fields.Float()
    cloth_cathegory = fields.String()
    gender = fields.String()
    image = fields.String()
    url = fields.String()


class ReviewDetailSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    content = fields.String()
    date = fields.String()


class ProductDetailSchema(ProductSchema):
    rating_average = fields.Float()
    reviews = fields.List(fields.Nested(ReviewDetailSchema))


class ProductListSchema(Schema):
    products = fields.List(fields.Nested(ProductSchema))


class BasketSchema(Schema):
    items = fields.List(fields.Nested(ProductSchema))
    total_cost = fields.Float()


class RatingResultSchema(Schema):
    rating = fields.Float()


class ReviewResultSchema(Schema):
    id = fields.Integer()
    content = fields.String()


class ErrorDetailSchema(Schema):
    code = fields.String()
    message = fields.String()


class ApiErrorSchema(Schema):
    error = fields.Nested(ErrorDetailSchema)
