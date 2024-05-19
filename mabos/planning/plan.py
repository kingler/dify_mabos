from typing import List
from ..task_management.action import Action
from ..agents.agent import Agent

class Plan:
    def __init__(self, plan_id: str, goal_id: str, actions: List[Action], priority: int = 0,
                 preconditions: List[str] = None, postconditions: List[str] = None,
                 constraints: List[str] = None):
        self.plan_id = plan_id
        self.goal_id = goal_id
        self.actions = actions
        self.priority = priority
        self.preconditions = preconditions or []
        self.postconditions = postconditions or []
        self.constraints = constraints or []
        self.status = "pending"

    def execute(self, agents: List['Agent']):
        if self.check_preconditions():
            self.status = "in_progress"
            for action in self.actions:
                agent = self.select_agent(action, agents)
                action.execute(agent)
                # Monitor progress and handle failures
                if not action.status == "completed":
                    self.repair(action)
            self.status = "completed"
            self.evaluate()
        else:
            self.status = "failed"
            # Handle precondition failure
            self.adapt_to_precondition_failure()

    def check_preconditions(self) -> bool:
        # Check if all preconditions are satisfied
        return all(precondition for precondition in self.preconditions)

    def evaluate(self):
        # Evaluate the success or effectiveness of the plan
        actual_outcomes = self.get_actual_outcomes()
        success_rate = self.calculate_success_rate(actual_outcomes)
        effectiveness_score = self.calculate_effectiveness_score(actual_outcomes)
        
        # Compare actual outcomes with postconditions
        for outcome, postcondition in zip(actual_outcomes, self.postconditions):
            if outcome != postcondition:
                print(f"Postcondition mismatch: Expected {postcondition}, got {outcome}")
        
        print(f"Plan success rate: {success_rate}")
        print(f"Plan effectiveness score: {effectiveness_score}")
        # Compare actual outcomes with postconditions
        pass

    def adapt(self, new_goal: str):
        # Adapt the plan based on goal changes
        self.goal_id = new_goal
        new_actions = self.generate_actions_for_goal(new_goal)
        self.actions = self.merge_actions(self.actions, new_actions)
        self.update_preconditions_and_postconditions()

    def generate_actions_for_goal(self, goal: str) -> List[Action]:
        # Generate new actions based on the new goal
        # Implement goal-based action generation logic
        pass

    def merge_actions(self, current_actions: List[Action], new_actions: List[Action]) -> List[Action]:
        # Merge current actions with new actions
        # Resolve conflicts and optimize the merged action sequence
        merged_actions = []
        current_action_index = 0
        new_action_index = 0

        while current_action_index < len(current_actions) and new_action_index < len(new_actions):
            current_action = current_actions[current_action_index]
            new_action = new_actions[new_action_index]

            if current_action.priority > new_action.priority:
                merged_actions.append(current_action)
                current_action_index += 1
            elif current_action.priority < new_action.priority:
                merged_actions.append(new_action)
                new_action_index += 1
            else:
                # Resolve conflicts between actions with the same priority
                if current_action.action_id == new_action.action_id:
                    # Merge actions with the same ID
                    merged_action = self.merge_action_properties(current_action, new_action)
                    merged_actions.append(merged_action)
                    current_action_index += 1
                    new_action_index += 1
                else:
                    # Prioritize actions based on additional criteria (e.g., dependencies, resource usage)
                    if self.is_action_preferred(current_action, new_action):
                        merged_actions.append(current_action)
                        current_action_index += 1
                    else:
                        merged_actions.append(new_action)
                        new_action_index += 1

        # Append remaining actions from either list
        merged_actions.extend(current_actions[current_action_index:])
        merged_actions.extend(new_actions[new_action_index:])

        # Optimize the merged action sequence
        optimized_actions = self.optimize_action_sequence(merged_actions)

        return optimized_actions

    def update_preconditions_and_postconditions(self):
        # Update preconditions and postconditions based on the adapted plan
        for action in self.actions:
            # Update preconditions
            for precondition in action.preconditions:
                if not self.satisfies_condition(precondition):
                    # Find actions that can satisfy the precondition
                    satisfying_actions = self.find_satisfying_actions(precondition)
                    if satisfying_actions:
                        # Insert satisfying actions before the current action
                        index = self.actions.index(action)
                        self.actions[index:index] = satisfying_actions
                    else:
                        # Remove the action if its preconditions cannot be satisfied
                        self.actions.remove(action)
                        break
            
            # Update postconditions
            for postcondition in action.postconditions:
                if self.satisfies_condition(postcondition):
                    # Remove redundant postconditions
                    action.postconditions.remove(postcondition)
        
        # Update overall plan preconditions and postconditions
        self.preconditions = [precondition for action in self.actions for precondition in action.preconditions]
        self.postconditions = [postcondition for action in self.actions for postcondition in action.postconditions]

    def adapt_to_precondition_failure(self):
        # Adapt the plan when preconditions are not satisfied
        # Modify actions or find alternative paths to satisfy preconditions
        unsatisfied_preconditions = [precondition for action in self.actions for precondition in action.preconditions if not self.satisfies_condition(precondition)]
        
        for precondition in unsatisfied_preconditions:
            # Find actions that can satisfy the precondition
            satisfying_actions = self.find_satisfying_actions(precondition)
            
            if satisfying_actions:
                # Insert satisfying actions before the action with the unsatisfied precondition
                action_index = next(i for i, action in enumerate(self.actions) if precondition in action.preconditions)
                self.actions[action_index:action_index] = satisfying_actions
            else:
                # Remove the action if its preconditions cannot be satisfied
                action_to_remove = next(action for action in self.actions if precondition in action.preconditions)
                self.actions.remove(action_to_remove)
        
        # Optimize the modified plan
        self.actions = self.optimize_action_sequence(self.actions)

    def merge(self, other_plan: 'Plan') -> 'Plan':
        # Merge the current plan with another plan
        merged_actions = self.actions + other_plan.actions
        # Resolve conflicts and optimize the merged plan
        merged_plan = Plan(plan_id=f"{self.plan_id}_{other_plan.plan_id}",
                           goal_id=self.goal_id,
                           actions=merged_actions,
                           priority=max(self.priority, other_plan.priority),
                           preconditions=self.preconditions + other_plan.preconditions,
                           postconditions=self.postconditions + other_plan.postconditions,
                           constraints=self.constraints + other_plan.constraints)
        return merged_plan

    def select_agent(self, action: Action, agents: List['Agent']) -> 'Agent':
        best_agent = None
        max_suitability_score = -1

        for agent in agents:
            if not agent.available:
                continue

            suitability_score = 0
            
            # Check if the agent has the required capabilities for the action
            if set(action.required_capabilities).issubset(agent.capabilities):
                suitability_score += 1

            # Consider agent's experience level for similar actions
            if action.name in agent.experience:
                suitability_score += agent.experience[action.name]

            # Check agent's current workload
            if agent.current_workload < agent.max_workload:
                suitability_score += 1

            # Update the best agent if the current agent has a higher suitability score
            if suitability_score > max_suitability_score:
                max_suitability_score = suitability_score
                best_agent = agent

        if best_agent is None:
            raise Exception("No suitable agent found for the action.")
        # Consider agent capabilities, availability, and other criteria
        return agents[0]  # Placeholder implementation

    def repair(self, failed_action: Action):
        # Repair the plan by replacing the failed action with an alternative
        alternative_action = self.find_alternative_action(failed_action)
        if alternative_action:
            self.actions[self.actions.index(failed_action)] = alternative_action
        else:
            # If no alternative action found, replan from the failed action
            self.replan(failed_action)

    def find_alternative_action(self, failed_action: Action) -> Action:
        # Find an alternative action to replace the failed action
        # Consider action preconditions, effects, and constraints
        alternative_actions = []
        for action in self.available_actions:
            if action.effects == failed_action.effects:
                if all(precondition in self.current_state for precondition in action.preconditions):
                    if all(constraint.satisfied(action) for constraint in self.constraints):
                        alternative_actions.append(action)
        
        if alternative_actions:
            # Select the best alternative action based on a heuristic or cost function
            best_alternative = min(alternative_actions, key=lambda a: a.cost)
            return best_alternative
        else:
            return None

    def replan(self, failed_action: Action):
        # Replan the actions from the failed action
        # Generate a new plan starting from the current state
        current_state = self.get_current_state()
        new_plan = self.generate_plan(current_state, self.goal_id)
        self.actions = self.actions[:self.actions.index(failed_action)] + new_plan.actions

    def generate_plan(self, current_state: List[str], goal: str) -> 'Plan':
        # Generate a new plan from the current state to achieve the goal
        # Implement planning algorithms like A*, forward search, or backward search
        pass

    def get_current_state(self) -> List[str]:
        # Get the current state of the environment
        # Implement state retrieval logic based on the environment
        pass

    def decompose(self) -> List['Plan']:
        # Decompose the high-level plan into more detailed sub-plans
        sub_plans = []
        for action in self.actions:
            sub_plan = self.create_sub_plan(action)
            if sub_plan:
                sub_plans.append(sub_plan)
        return sub_plans

    def create_sub_plan(self, action: Action) -> 'Plan':
        sub_plan = Plan(name=f"Sub-plan for {action.name}")
        sub_actions = []
        
        # Define sub-actions based on the specific action
        if action.name == "Market Research":
            sub_actions.append(Action(name="Conduct Surveys"))
            sub_actions.append(Action(name="Analyze Competitors"))
            sub_actions.append(Action(name="Identify Target Customers"))
        elif action.name == "Product Development":
            sub_actions.append(Action(name="Design Product"))
            sub_actions.append(Action(name="Prototype Creation"))
            sub_actions.append(Action(name="User Testing"))
        # Add more conditions for other specific actions
        
        # Set dependencies between sub-actions
        sub_actions[1].add_precondition(sub_actions[0])
        sub_actions[2].add_precondition(sub_actions[1])
        
        sub_plan.actions = sub_actions
        sub_plan.preconditions = action.preconditions
        sub_plan.postconditions = action.postconditions
        sub_plan.constraints = action.constraints
        
        return sub_plan
