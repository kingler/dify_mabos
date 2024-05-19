# mabos/process/business_process_manager.py
from mabos.communication.message import DelayedMessageQueue
from datetime import datetime

class BusinessProcessManager:
    def __init__(self, broker):
        self.broker = broker
        self.task_assignments = {}
        # Initialize other attributes and components

    def execute_process(self, process_definition):
        # Parse process definition and identify involved agents
        involved_agents = self._parse_process_definition(process_definition)
        
        # Get tasks from the process definition
        tasks = process_definition.get("tasks", [])
        
        # Assign tasks to agents based on their locations
        self.task_assignments = self._assign_tasks_to_agents(involved_agents)
        
        # Coordinate task execution using the broker
        for agent, tasks in self.task_assignments.items():
            for task in tasks:
                message = {"type": "task_execution", "task": task}
                self.broker.route_message(self, agent, message)

    def monitor_process(self, involved_agents):
        # Monitor the progress of a process instance
        status_updates = {}
        for agent, tasks in self.task_assignments.items():
            agent_location = self.broker.agent_locations.get(agent)
            if agent_location is None:
                raise ValueError(f"Agent {agent} not registered with the broker")
            for task in tasks:
                message = {"type": "status_request", "task": task}
                status = self.broker.route_message(self, agent, message)
                status_updates[(agent, task)] = status

        # Collect status updates from involved agents using location-based addressing
        delayed_updates = []
        for (agent, task), status in status_updates.items():
            if status and not status.get("is_critical", False):
                delayed_updates.append((agent, task, status))
            elif status:
                # Handle critical updates immediately
                self._handle_critical_update(agent, task, status, involved_agents)

        # Apply delayed message passing for non-critical updates  
        delayed_message_queue = DelayedMessageQueue()
        for agent, task, status in delayed_updates:
            message = {"type": "status_update", "task": task, "status": status}
            delayed_message_queue.enqueue_message(message)
        delayed_message_queue.send_batch(self.broker)

    def _parse_process_definition(self, process_definition):
        involved_agents = []
        tasks = process_definition.get("tasks", [])
        for task in tasks:
            agent_id = task.get("agent_id")
            if agent_id:
                involved_agents.append(agent_id)
        return involved_agents

    def _assign_tasks_to_agents(self, involved_agents, tasks):
        task_assignments = {}
        for agent_id in involved_agents:
            agent_location = self.broker.agent_locations.get(agent_id)
            if agent_location is None:
                raise ValueError(f"Agent {agent_id} not registered with the broker")
            
            assigned_tasks = []
            for task in tasks:
                if task.get("location") == agent_location:
                    assigned_tasks.append(task)
            
            if assigned_tasks:
                task_assignments[agent_id] = assigned_tasks
        
        return task_assignments

    def _handle_critical_update(self, agent, task, status, involved_agents):
        # Log the critical update
        self.logger.log_critical_update(agent, task, status)
        
        # Store the critical update in message storage
        message = {"sender": agent, "recipient": self, "content": {"task": task, "status": status}, "timestamp": datetime.now()}
        self.message_storage.store_message(message)
        
        # Notify relevant agents about the critical update
        for agent_id in involved_agents:
            if agent_id != agent:
                notification_message = {"type": "critical_update_notification", "task": task, "status": status}
                self.broker.route_message(self, agent_id, notification_message)
        
        # Trigger any necessary actions based on the critical update
        if status.get("requires_immediate_action", False):
            self._trigger_immediate_action(agent, task, status)
        