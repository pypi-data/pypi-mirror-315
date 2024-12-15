#!/usr/bin/env python3

import logging

import click

from flightpath.tracer import AirflowClient, CriticalPathTracer


# Updated CLI commands
@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option(
    "-p",
    "--page-length",
    type=int,
    required=False,
    default=100,
    help="Page length for API calls (integer)",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, page_length: int) -> None:
    """Extract information from an Airflow instance."""
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    ctx.obj = {"page_length": page_length}


@cli.command()
@click.option("-u", "--username", required=True, type=str, help="Airflow username")
@click.option("-p", "--password", required=True, type=str, help="Airflow password")
@click.option("--baseurl", required=True, help="Base URL of the Airflow instance")
@click.option("--end-task-id", required=True, help="ID of the end task")
@click.option(
    "--end-dag-id",
    help="ID of the end DAG. If not provided, all DAGs will be extracted.",
)
@click.option("--dag-run-id", required=True, help="ID of the DAG run")
@click.option(
    "--stay-within-dag",
    is_flag=True,
    help="Only trace the critical path within the dag_id specified",
)
@click.option(
    "--print-url",
    is_flag=True,
    help="Print the full URL for each task instance instead of using hyperlinks. Helpful if your terminal does not support OSC8 hyperlinks.",
)

@click.pass_context
def trace(
    ctx: click.Context,
    username: str,
    password: str,
    baseurl: str,
    end_task_id: str,
    end_dag_id: str,
    dag_run_id: str,
    stay_within_dag: bool,
    print_url: bool,
) -> None:
    client = AirflowClient(user=username, password=password, base_url=baseurl)
    tracer = CriticalPathTracer(client)

    root_ti = tracer.trace(
        end_dag_id=end_dag_id, 
        end_task_id=end_task_id, 
        dag_run_id=dag_run_id,
        stay_within_dag=stay_within_dag
    )

    CriticalPathTracer.print_critical_path(
        root_ti=root_ti, 
        print_url=print_url
    )

if __name__ == "__main__":
    cli()

    # cd ~/src/flightpath/tests/airflow_example; astro dev start; cd -

    # poetry run flightpath --verbose trace -u admin -p admin --baseurl http://localhost:8080 --end-task-id end --end-dag-id diamond2 --dag-run-id scheduled__2024-12-13T00:50:00+00:00
