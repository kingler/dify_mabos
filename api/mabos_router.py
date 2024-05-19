from fastapi import APIRouter
from typing import List
from ..mabos.agents.agent import Agent
from ..mabos.goal_management.goal import Goal
from ..mabos.planning.plan import Plan   
from ..mabos.task_management.action import Action
from ..mabos.knowledge_base import KnowledgeBase
from ..mabos.knowledge_management.ontology.ontology import Ontology

router = APIRouter()

@router.post("/agents")
def create_agent(agent_id: str, beliefs: dict, desires: List[dict], intentions: List[dict], ontology: dict):
    # Create knowledge base and ontology instances
    ontology_instance = Ontology(concepts=ontology.get("concepts", {}), relationships=ontology.get("relationships", {}))
    knowledge_base = KnowledgeBase(ontology=ontology_instance)

    # Create goal and plan instances from the provided desires and intentions
    goals = [Goal(goal_id=goal.get("goal_id"), description=goal.get("description"), priority=goal.get("priority")) for goal in desires]
    plans = [Plan(plan_id=plan.get("plan_id"), goal_id=plan.get("goal_id"), actions=[]) for plan in intentions]

    # Create the agent instance
    agent = Agent(agent_id=agent_id, beliefs=beliefs, desires=goals, intentions=plans, knowledge_base=knowledge_base)

    return {"agent_id": agent.agent_id}

@router.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    agent = Agent.get_by_id(agent_id)
    if agent is None:
        return {"error": "Agent not found"}, 404
    return {
        "agent_id": agent.agent_id,
        "beliefs": agent.beliefs,
        "desires": [goal.__dict__ for goal in agent.desires],
        "intentions": [plan.__dict__ for plan in agent.intentions],
        "knowledge_base": {
            "ontology": {
                "concepts": agent.knowledge_base.ontology.concepts,
                "relationships": agent.knowledge_base.ontology.relationships
            },
            "facts": agent.knowledge_base.facts
        }
    }
    pass

@router.put("/agents/{agent_id}/beliefs")
def update_agent_beliefs(agent_id: str, beliefs: dict):
    agent = Agent.get_by_id(agent_id)
    if agent is None:
        return {"error": "Agent not found"}, 404

    agent.beliefs.update(beliefs)
    return {"message": "Beliefs updated successfully", "agent_id": agent.agent_id}
    pass

@router.post("/agents/{agent_id}/goals")
def add_agent_goal(agent_id: str, goal: Goal):
    agent = Agent.get_by_id(agent_id)
    if agent is None:
        return {"error": "Agent not found"}, 404

    new_goal = Goal(goal_id=goal.goal_id, description=goal.description, priority=goal.priority)
    agent.desires.append(new_goal)
    
    return {"message": "Goal added successfully", "agent_id": agent.agent_id, "goal_id": new_goal.goal_id}
    pass

@router.post("/agents/{agent_id}/plans")
def add_agent_plan(agent_id: str, plan: Plan):
    agent = Agent.get_by_id(agent_id)
    if agent is None:
        return {"error": "Agent not found"}, 404

    new_plan = Plan(plan_id=plan.plan_id, goal_id=plan.goal_id, actions=plan.actions)
    agent.intentions.append(new_plan)
    
    return {"message": "Plan added successfully", "agent_id": agent.agent_id, "plan_id": new_plan.plan_id}
    pass

@router.delete("/agents/{agent_id}/plans/{plan_id}")
def remove_agent_plan(agent_id: str, plan_id: str):
    # Implement logic to remove a plan from an agent
    agent = Agent.get_by_id(agent_id)
    if agent is None:
        return {"error": "Agent not found"}, 404

    plan_to_remove = next((plan for plan in agent.intentions if plan.plan_id == plan_id), None)
    if plan_to_remove is None:
        return {"error": "Plan not found"}, 404

    agent.intentions.remove(plan_to_remove)
    return {"message": "Plan removed successfully", "agent_id": agent.agent_id, "plan_id": plan_id}
    pass