from random import randint
from typing import Optional
from uuid import uuid4

from faker import Faker

from t_reporting_sdk.domain.agent_runs.models import AgentRun


class AgentRunFaker:
    @staticmethod
    def provide(
        id: Optional[str] = None,
        run_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        organization_name: Optional[str] = None,
    ) -> AgentRun:
        fake_id = str(uuid4())
        fake_run_id = randint(1, 100)
        fake_organization_id = randint(1, 100)
        fake_organization_name = Faker().company()
        return AgentRun(
            id=fake_id if id is None else id,
            run_id=fake_run_id if run_id is None else id,
            organization_id=fake_organization_id if organization_id is None else id,
            organization_name=fake_organization_name if organization_name is None else id,
        )