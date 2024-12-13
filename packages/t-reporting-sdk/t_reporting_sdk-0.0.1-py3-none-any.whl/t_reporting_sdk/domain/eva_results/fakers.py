from random import randint
from typing import Optional

from faker import Faker

from t_reporting_sdk.domain.eva_results.models import EVAResult, EVARecordStatus, EVAExceptionType


class EVAResultFaker:
    @staticmethod
    def provide(
        status: Optional[EVARecordStatus] = None,
        exception_type: Optional[str] = None,
        message: Optional[str] = None,
        customer_id: Optional[str] = None,
        patient_id: Optional[str] = None,
        payer_id: Optional[str] = None,
        portal: Optional[str] = None,
    ) -> EVAResult:
        faker = Faker()
        
        fake_status = EVARecordStatus.SUCCESS
        fake_exception_type = EVAExceptionType.EXCEPTION_PLACEHOLDER
        fake_message = faker.text(max_nb_chars=500)
        fake_customer_id = str(randint(1, 100))
        fake_patient_id = str(randint(1, 100))
        fake_payer_id = str(randint(1, 100))
        fake_portal = faker.company()

        return EVAResult(
            status=fake_status if status is None else status,
            exception_type=fake_exception_type if exception_type is None else exception_type,
            message=fake_message if message is None else message,
            customer_id=fake_customer_id if customer_id is None else customer_id,
            patient_id=fake_patient_id if patient_id is None else patient_id,
            payer_id=fake_payer_id if payer_id is None else payer_id,
            portal=fake_portal if portal is None else portal,
        )
