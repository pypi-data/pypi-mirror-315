from enum import Enum

from pydantic import BaseModel


class EVARecordStatus(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    EXCEPTION = 'exception'


class EVAExceptionType(Enum):
    """
    Exception type specified determined by the Agent
    """
    EXCEPTION_PLACEHOLDER = 'exception_placeholder'


class EVAResult(BaseModel):
    status: EVARecordStatus
    exception_type: EVAExceptionType
    message: str  # Additional context about the exception provided by the Agent.
    customer_id: str  # ID of the Thoughtful customer

    # EVA records typically refer to a patient/payer combo run on a specific portal
    patient_id: str  # ID of the patient eligibility verification is being performed on
    payer_id: str  # ID of the Payer that eligibility verification is being checked against
    portal: str  # Name of the portal being interacted with

