class NotFound(Exception):
    pass


class FunctionCallError(Exception):
    errors = list[str]

    def __init__(self, message, errors: list[str]):
        self.errors = errors
        super().__init__(message)

    def __str__(self) -> str:
        return super().__str__() + f"\nErrors: {self.errors}"


# class APIError(Exception):
#     message: str
#     request: httpx.Request

#     body: object | None
#     """The API response body.

#     If the API responded with a valid JSON structure then this property will be the
#     decoded result.

#     If it isn't a valid JSON structure then this will be the raw response.

#     If there was no response associated with this error then it will be `None`.
#     """

#     code: Optional[str] = None
#     param: Optional[str] = None
#     type: Optional[str]

#     def __init__(self, message: str, request: httpx.Request, *, body: object | None) -> None:
#         super().__init__(message)
#         self.request = request
#         self.message = message
#         self.body = body

#         if is_dict(body):
#             self.code = cast(Any, construct_type(type_=Optional[str], value=body.get("code")))
#             self.param = cast(Any, construct_type(type_=Optional[str], value=body.get("param")))
#             self.type = cast(Any, construct_type(type_=str, value=body.get("type")))
#         else:
#             self.code = None
#             self.param = None
#             self.type = None
