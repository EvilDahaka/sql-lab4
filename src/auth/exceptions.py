class UserServiceError(Exception):
    """Base exception for user service errors."""

    pass


class UserNotFoundError(UserServiceError):
    """Exception raised when a user is not found."""

    pass


class UserRegistrationError(UserServiceError):
    """Exception raised during user registration errors."""

    pass


class UserAuthenticationError(UserServiceError):
    """Exception raised during user authentication errors."""

    pass