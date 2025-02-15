
#!/usr/bin/env python3

""" Template experiment application that uses the WEI client to run a workflow."""
from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign


def main() -> None:
    """Runs an example WEI workflow"""
    # *This defines the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="Test_Experiment",
        experiment_description="This a test experiment to demonstrate use of the WEI client",
    )
    # *We can also define a Campaign object to group multiple experiments together
    # *This is useful when you want to run multiple experiments together
    campaign = CampaignDesign(              # This is an advanced feature and can be ignored for now - Lee
        campaign_name="My_First_Campaign",
        campaign_description="This is a campaign, a way of grouping together multiple experiments",
    )
    experiment_client = ExperimentClient(
        server_host="localhost",
        server_port="8000",
        experiment=experiment_design,
        campaign=campaign,
    )

    # *The path to the Workflow definition yaml file
    workflow_dir = (Path(__file__).parent.parent / "workflows").resolve()
    workflow_path = workflow_dir / "cypherlab.workflow.yaml"

    # *This runs the workflow
    wf_run = experiment_client.start_run(
        workflow=workflow_path,
        payload={"wait_time": 5},
        blocking=True,  # *This will block the execution until the workflow is completed
    )

    # *You can use the below to get the image returned by the camera module
    datapoint_id = wf_run.get_datapoint_id_by_label("experiment_result")
    # experiment_client.get_datapoint_value(datapoint_id) # *This will return the image as a bytes object
    experiment_client.save_datapoint_value(
        datapoint_id, "experiment_output.jpg"
    )  # *This will save the image to a file


if __name__ == "__main__":
    main()
