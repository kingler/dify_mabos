from ast import Dict
from typing import Any
from .performance_metrics_collector import PerformanceMetricsCollector
from .anomaly_detection_engine import AnomalyDetectionEngine
from .predictive_analytics_engine import PredictiveAnalyticsEngine
import matplotlib.pyplot as plt
import networkx as nx

class MonitoringManager:
    def __init__(self, agents):
        self.agents = agents
        self.communication_graph = nx.DiGraph()
        self.metrics_collector = PerformanceMetricsCollector()
        self.anomaly_detection_engine = AnomalyDetectionEngine(self.metrics_collector)
        self.predictive_analytics_engine = PredictiveAnalyticsEngine(self.metrics_collector)

    def track_communication(self):
        for agent in self.agents:
            self.communication_graph.add_node(agent.agent_id)
            for recipient, message in agent.communication.sent_messages.items():
                self.communication_graph.add_edge(agent.agent_id, recipient, message=message)

    def visualize_communication_patterns(self):
        pos = nx.spring_layout(self.communication_graph)
        nx.draw(self.communication_graph, pos, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.communication_graph, 'message')
        nx.draw_networkx_edge_labels(self.communication_graph, pos, edge_labels=edge_labels)
        plt.show()

    def monitor_performance_metrics(self):
        for agent in self.agents:
            self.metrics_collector.collect_metrics('core', agent)
            self.metrics_collector.collect_metrics('knowledge_management', agent)
            self.metrics_collector.collect_metrics('reasoning', agent)
            self.metrics_collector.collect_metrics('planning', agent)
            self.metrics_collector.collect_metrics('execution', agent)

    def detect_anomalies(self):
        for component in self.metrics_collector.supported_components:
            self.anomaly_detection_engine.detect_anomalies(component, 'threshold')
            self.anomaly_detection_engine.detect_anomalies(component, 'statistical')
            self.anomaly_detection_engine.detect_anomalies(component, 'machine_learning')

    def predict_performance(self):
        for component in self.metrics_collector.supported_components:
            self.predictive_analytics_engine.train_prediction_model(component)
            predictions = self.predictive_analytics_engine.generate_predictions(component)
            self.predictive_analytics_engine.evaluate_prediction_model(component)
            self.predictive_analytics_engine.visualize_predictions(component, predictions)

    def log_communication(self, sender_id: str, recipient_id: str,      message: Dict[str, Any]):
            self.communication_logs.append((sender_id, recipient_id, message))
            
    def analyze_performance_metrics(self):
        # Perform analysis on performance metrics
        # Analyze performance metrics for each component
        for component in self.metrics_collector.supported_components:
            metrics = self.metrics_collector.retrieve_metrics(component, time_range='last_hour')
            
            # Calculate average response time
            avg_response_time = self.metrics_collector.aggregate_metrics(component, 'avg')
            print(f"Average response time for {component}: {avg_response_time} ms")
            
            # Identify performance bottlenecks
            bottlenecks = self.identify_bottlenecks(component, metrics)
            if bottlenecks:
                print(f"Performance bottlenecks identified for {component}:")
                for bottleneck in bottlenecks:
                    print(f"- {bottleneck}")
            
            # Generate performance report
            report = self.generate_performance_report(component, metrics)
            print(f"Performance report generated for {component}:")
            print(report)
            
            # Provide optimization recommendations
            recommendations = self.provide_optimization_recommendations(component, metrics)
            if recommendations:
                print(f"Optimization recommendations for {component}:")
                for recommendation in recommendations:
                    print(f"- {recommendation}")

    def update_performance_metric(self, component: str, metric: str, value: float):
        self.metrics_collector.update_metric(component, metric, value)

    def log_communication(self, sender_id: str, recipient_id: str, message: Dict[str, Any]):
        self.communication_logs.append((sender_id, recipient_id, message))
        self.update_performance_metric('communication', 'total_messages', 1)