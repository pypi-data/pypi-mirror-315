from t_reporting_sdk.domain.eva_results.models import EVAResult
from t_reporting_sdk.repositories.eva_results.repository import EVAResultsRepository
import logging


class EvaReporter:
    def __init__(self, eva_repository: EVAResultsRepository):
        self._eva_repository = eva_repository
    
    def report_eligibility_verification_result(self, eligibility_verification_result: EVAResult):
        try:
            self._eva_repository.store_eva_result(
                eligibility_verification_result=eligibility_verification_result)
        except Exception as e:
            # Handle failures - reporting failures should be logged but not cause the client to fail
            logging.error(f"Unable to report eligibility verification result: {e}")
