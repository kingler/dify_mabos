# mabos/agents/reporting_agent.py
from ...task_management.task import Task

class ReportingAgent:
    def __init__(self, data_store, visualization_manager):
        self.data_store = data_store
        self.visualization_manager = visualization_manager
        # Initialize other attributes and components

    def generate_report(self, report_type, parameters):
        # Retrieve data from the data store based on the report type and parameters
        # Generate the report using the visualization manager
        data = self.data_store.retrieve_data(report_type, parameters)
        report = self.visualization_manager.generate_report(data, report_type)
        return report
        pass

    def schedule_report(self, report_type, parameters, schedule):
        # Schedule a report to be generated periodically
        # Create a task to generate the report periodically
        report_task = Task(
            name=f"Generate {report_type} Report",
            description=f"Generate a {report_type} report with parameters: {parameters}",
            function=self.generate_report,
            args=(report_type, parameters),
            schedule=schedule
        )
        
        # Add the report task to the agent's task queue
        self.agent.add_task(report_task)
