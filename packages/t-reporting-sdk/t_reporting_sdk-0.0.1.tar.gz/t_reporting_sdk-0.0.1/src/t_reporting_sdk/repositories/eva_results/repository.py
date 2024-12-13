from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.eva_results.models import EVAResult
from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClient


class EVAResultsRepository:
    def __init__(self, fabric_client: FabricClient):
        self._fabric_api = fabric_client

    def store_eva_result(
            self,
            agent_run: AgentRun,  # AgentRun to associate the EVAResult with
            eva_result: EVAResult,
    ) -> None:
        record = {
            "agent_run_id": agent_run.run_id,
            "status": eva_result.status,
            "exception_type": eva_result.exception_type,
            "message": eva_result.message,
            "customer_id": eva_result.customer_id,
            "patient_id": eva_result.patient_id,
            "payer_id": eva_result.payer_id,
            "portal": eva_result.portal,
        }
        self._fabric_api.send_report(record)
