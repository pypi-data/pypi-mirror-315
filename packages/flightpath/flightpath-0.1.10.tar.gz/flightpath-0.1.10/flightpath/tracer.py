import abc 
from collections import defaultdict
import dataclasses
import datetime
import functools
import logging
import requests
import time
from typing import Collection, Optional, Mapping

import flightpath.config

@dataclasses.dataclass(frozen=True)
class Task:
    dag_id: str
    task_id: str

@dataclasses.dataclass
class TaskInstance:
    dag_id: str
    task_id: str
    dag_run_id: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    is_wait_task: bool = False
    prev: Optional["TaskInstance"] = None
    next: Optional["TaskInstance"] = None

    _path_index: Optional[int] = None



    @property
    def ready_seconds(self) -> float:
        if not self.prev:
            return 0.0

        if self.is_wait_task:
            return (self.end_date - self.prev.end_date).total_seconds()
        else:
            return (self.start_date - self.prev.end_date).total_seconds()

    @property
    def running_seconds(self) -> float:
        if self.is_wait_task:
            return 0.0
        else:
            return (self.end_date - self.start_date).total_seconds()
    
    @property
    def total_seconds(self) -> float:
        return self.running_seconds + self.ready_seconds

    def __str__(self):
        return f"TaskInstance({self.dag_id}.{self.task_id})"
    
    @property
    def path_index(self):
        if not self._path_index:
            if not self.prev:
                self._path_index = 0
            else:
                self._path_index = self.prev.path_index + 1
            
        return self._path_index
    
    def task(self) -> Task:
        return Task(self.dag_id, self.task_id)



class Client(abc.ABC):
    def get_task_instance(self, dag_id: str, task_id: str, dag_run_id: str) -> TaskInstance:
        pass

    def get_upstream_task_instances(self, ti: TaskInstance) -> Collection[TaskInstance]:
        pass


class AirflowClient(Client):
    def __init__(self, user: str, password: str, base_url: str, verbose: bool = False):
        self.user = user
        self.password = password
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.verbose = verbose

        self._auth = None
    
    @property
    def auth(self) -> requests.auth.HTTPBasicAuth:
        if not self._auth:
            self._auth = requests.auth.HTTPBasicAuth(self.user, self.password)
        return self._auth
    
    def get_task_instance(self, dag_id: str, task_id: str, dag_run_id: str) -> TaskInstance:
        endpoint = f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}"
        logging.debug(f"Fetching task {task_id} in dag {dag_id} for run id {dag_run_id} from: {endpoint}")
        response = requests.get(endpoint, auth=self.auth)

        if response.status_code != 200:
            response.raise_for_status()
            logging.warning(
                "Received error from API. Waiting 120 seconds and retrying."
            )
            time.sleep(120)
            response = requests.get(endpoint, auth=self.auth)
        
            if response.status_code != 200:
                raise Exception(f"Error: Unable to fetch task instances. Status code: {response.status_code}")

        data = response.json()

        is_wait_task = data["operator"] == "ExternalTaskSensor"

        return TaskInstance(
            dag_id=data["dag_id"],
            task_id=data["task_id"],
            dag_run_id=data["dag_run_id"],
            start_date=datetime.datetime.fromisoformat(data["start_date"]),
            end_date=datetime.datetime.fromisoformat(data["end_date"]),
            is_wait_task=is_wait_task,
        )
    
    @functools.lru_cache(maxsize=1000)
    def _get_all_task_dependencies_for_dag(self, dag_id: str, dag_run_id: str) -> Mapping[Task, Collection[Task]]:
        endpoint = f"{self.base_url}/api/v1/dags/{dag_id}/tasks"
        logging.debug(f"Extracting dependencies for dag {dag_id} from endpoint: {endpoint}")

        # Make request for all tasks
        response = requests.get(endpoint, auth=self.auth)

        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response content: {response.text}")
        response.raise_for_status()

        tasks = response.json()["tasks"]
        logging.debug(f"Found {len(tasks)} tasks for dependency analysis")

        dependencies = defaultdict(lambda: set())

        for task in tasks:
            for downstream_task_id in task["downstream_task_ids"]:
                dependencies[Task(dag_id, downstream_task_id)].add(Task(dag_id, task['task_id']))

            if task["class_ref"]["class_name"] == "ExternalTaskSensor":
                task_instance_endpoint = f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task['task_id']}"

                logging.debug(
                    f"Extracting upstream information for ExternalTaskSensor task {task['task_id']} from endpoint: {task_instance_endpoint}"
                )
                response = requests.get(task_instance_endpoint, auth=self.auth)
                task_info = response.json()

                if (
                    "rendered_fields" in task_info
                    and "external_dag_id" in task_info["rendered_fields"]
                    and "external_task_id" in task_info["rendered_fields"]
                ):
                    external_dag_id = task_info["rendered_fields"]["external_dag_id"]
                    external_task_id = task_info["rendered_fields"]["external_task_id"]

                    dependencies[Task(dag_id, task['task_id'])].add(
                        Task(external_dag_id, external_task_id)
                    )
                else:
                    logging.warning(
                        f"Could not find upstream information for ExternalTaskSensor task {task['task_id']} from endpoint: {task_instance_endpoint} for dag_run_id {dag_run_id}"
                    )

        logging.debug("Sleeping to throttle requests...")
        time.sleep(flightpath.config.THROTTLE_DURATION_SECONDS)

        return dict(dependencies)

    def get_upstream_task_instances(self, ti: TaskInstance) -> Collection[TaskInstance]:
        dependencies = self._get_all_task_dependencies_for_dag(
            dag_id=ti.dag_id, 
            dag_run_id=ti.dag_run_id
        )

        if ti.task() in dependencies:
            upstream_tasks = dependencies[Task(ti.dag_id, ti.task_id)]

            upstream_task_instances = [
                self.get_task_instance(dag_id=t.dag_id, task_id=t.task_id, dag_run_id=ti.dag_run_id) 
                for t in upstream_tasks
            ]

            return upstream_task_instances
        else:
            return []


class CriticalPathTracer:
    def __init__(self, client: Client, verbose: bool = False):
        self.client = client
        self.verbose = verbose
    
    def trace(self, end_dag_id: str, end_task_id: str, dag_run_id: str, stay_within_dag: bool = False) -> TaskInstance:
        logging.debug(f"Tracing critical path starting from dag {end_dag_id} task {end_task_id} for run id {dag_run_id}")
        current_ti = self.client.get_task_instance(end_dag_id, end_task_id, dag_run_id)
        logging.info(f"Tracing from {end_dag_id}:{end_task_id}")

        while True:
            previous_ti = self.find_previous(current_ti)

            if stay_within_dag and previous_ti.dag_id != end_dag_id:
                break

            if not previous_ti:
                break

            logging.info(f"Found previous task {previous_ti.dag_id}:{previous_ti.task_id}")

            current_ti.prev = previous_ti
            previous_ti.next = current_ti

            current_ti = previous_ti
        
        return current_ti

    def find_previous(self, ti: TaskInstance) -> TaskInstance:
        upstream_task_instances = self.client.get_upstream_task_instances(ti)

        if not upstream_task_instances:
            return None

        return max(upstream_task_instances, key=lambda t: t.end_date)
    
    @staticmethod
    def print_critical_path(root_ti: TaskInstance):
        results = []

        current_ti = root_ti
        while current_ti:
            results.append(current_ti)
            current_ti = current_ti.next

        # Prepare data for printing
        headers = [
            "DAG ID",
            "Path Index",
            "Task ID",
            "Ready Date",
            "Start Date",
            "End Date",
            "Ready (Seconds)",
            "Running (Seconds)",
            "Total (Seconds)",
        ]
        
        # Convert task instances to rows of data
        data = []
        for ti in results:
            data.append([
                ti.dag_id,
                str(ti.path_index),
                ti.task_id,
                ti.prev.end_date.strftime("%Y-%m-%d %H:%M:%S") if ti.prev else "-",
                ti.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                ti.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                f"{ti.ready_seconds:.1f}" if ti.ready_seconds else "-",
                f"{ti.running_seconds:.1f}" if ti.running_seconds else "-", 
                f"{ti.total_seconds:.1f}" if ti.total_seconds else "-"
            ])

        # Calculate column widths based on data and headers
        all_rows = [headers] + data
        col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(headers))]

        # Create format string for consistent column widths
        format_string = " | ".join("{:<" + str(width) + "}" for width in col_widths)

        # Print table
        print(format_string.format(*headers))
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        for row in data:
            print(format_string.format(*row))

        # Calculate summary statistics
        total_ready = sum(ti.ready_seconds or 0 for ti in results)
        total_running = sum(ti.running_seconds or 0 for ti in results)
        total_time = total_ready + total_running
        
        longest_task = max(results, key=lambda ti: ti.total_seconds or 0)
        longest_time = longest_task.total_seconds
        longest_percent = (longest_time / total_time * 100) if total_time > 0 else 0

        print("\n-- Statistics --")
        print(f"Ready Time:\t{total_ready:.1f} Seconds")
        print(f"Running Time:\t{total_running:.1f} Seconds") 
        print(f"Total Time:\t{total_time:.1f} Seconds")
        print(f"Longest Task:\t{longest_task.dag_id}:{longest_task.task_id} ({longest_time:.1f} Seconds, {longest_percent:.1f}% of total time)")

        print("\n-- Parameters --")
        print(f"Run Id:\t\t{results[-1].dag_run_id}")
        print(f"End Dag:\t{results[-1].dag_id}")
        print(f"End Task:\t{results[-1].task_id}")








    