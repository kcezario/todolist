from drf_spectacular.utils import OpenApiParameter, OpenApiExample

TASK_FILTERS = [
    OpenApiParameter(
        name="status",
        description="Filter by task status (P=Pending, E=In Progress, C=Completed)",
        required=False,
        type=str,
        enum=["P", "E", "C"]
    ),
    OpenApiParameter(
        name="due_date",
        description="Filter by exact due date (format: YYYY-MM-DD)",
        required=False,
        type=str
    ),
    OpenApiParameter(
        name="due_date__gte",
        description="Filter tasks with due date greater than or equal to (YYYY-MM-DD)",
        required=False,
        type=str
    ),
    OpenApiParameter(
        name="due_date__lte",
        description="Filter tasks with due date less than or equal to (YYYY-MM-DD)",
        required=False,
        type=str
    ),
]

CREATE_USER_PARAMS = [
    OpenApiParameter(
        name="username",
        description="Unique username for the new user",
        required=True,
        type=str
    ),
    OpenApiParameter(
        name="password",
        description="Password for the new user",
        required=True,
        type=str
    ),
    OpenApiParameter(
        name="email",
        description="Email address of the new user",
        required=False,
        type=str
    ),
    OpenApiParameter(
        name="group",
        description="Optional: Assign the user to a specific group (e.g., Admin, Manager, User)",
        required=False,
        type=str
    ),
]

CREATE_USER_RESPONSES = {
    201: OpenApiExample(
        name="User Created",
        value={"id": 1, "username": "newuser", "email": "user@example.com", "group": "Manager"},
        response_only=True
    ),
    400: OpenApiExample(
        name="User already exists",
        value={"error": "User with this username already exists."},
        response_only=True
    ),
    403: OpenApiExample(
        name="Permission denied",
        value={"detail": "You do not have permission to perform this action."},
        response_only=True
    ),
}
