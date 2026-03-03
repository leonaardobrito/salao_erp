from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

class DomainException(Exception):
    """Base exception for domain errors."""
    def __init__(self, message, code='domain_error'):
        self.message = message
        self.code = code
        super().__init__(message)


class BusinessRuleViolation(DomainException):
    """Exception for business rule violations."""
    def __init__(self, message):
        super().__init__(message, code='business_rule_violation')


class EntityNotFoundException(DomainException):
    """Exception when entity is not found."""
    def __init__(self, message):
        super().__init__(message, code='entity_not_found')


class DuplicateEntityException(DomainException):
    """Exception when trying to create duplicate entity."""
    def __init__(self, message):
        super().__init__(message, code='duplicate_entity')


class InvalidStateException(DomainException):
    """Exception when entity is in invalid state for operation."""
    def __init__(self, message):
        super().__init__(message, code='invalid_state')


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
    
    # Handle custom domain exceptions
    if isinstance(exc, DomainException):
        return Response(
            {'detail': exc.message, 'code': exc.code},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return response
