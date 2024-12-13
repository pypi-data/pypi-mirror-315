from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClient


class AgentRunsRepository:
    def __init__(self, fabric_client: FabricClient):
        self._fabric_api = fabric_client

    def store_agent_run(
            self,
            agent_run: AgentRun,
    ) -> AgentRun:
        record = {
            "run_id": agent_run.run_id,
            "organization_id": agent_run.organization_id,
            "organization_name": agent_run.organization_name,
        }
        result = self._fabric_api.send_report(record)

        return AgentRun(
            run_id=result.run_id,
            organization_id=result.organization_id,
            organization_name=result.organization_name,
            id=result.id,
        )
