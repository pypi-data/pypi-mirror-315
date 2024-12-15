from typing import List
from pydantic import BaseModel, Field
from dria_workflows import Workflow, WorkflowBuilder, Operator, Edge, Write, CustomTool
from dria.factory.workflows.template import SingletonTemplate
from dria.models import TaskResult


class SumTool(CustomTool):
    """
    A custom tool to perform summation of two integers.
    """

    name: str = "calculator"
    description: str = "A tool that sums two integers."
    lhs: int = Field(0, description="Left-hand operand for summation")
    rhs: int = Field(0, description="Right-hand operand for summation")

    def execute(self) -> int:
        """
        Execute the summation operation.

        Returns:
            int: The sum of lhs and rhs
        """
        return self.lhs + self.rhs


class SummationOutput(BaseModel):
    """
    Schema for the output of the summation workflow.
    """

    query: str
    result: int = Field(..., description="The result of the summation.")


class Summation(SingletonTemplate):
    """
    Workflow for executing a summation operation and handling function calls.
    """

    # Input fields
    prompt: str = Field(..., description="Input prompt for the workflow")

    # Output schema
    OutputSchema = SummationOutput

    def workflow(self) -> Workflow:
        """
        Creates the summation workflow.

        Returns:
            Workflow: A constructed workflow for summation
        """
        # Set default values for the workflow
        max_tokens = getattr(self.params, "max_tokens", 1000)
        builder = WorkflowBuilder()

        # Add custom summation tool to the workflow
        builder.add_custom_tool(SumTool())
        builder.set_max_tokens(max_tokens)

        # Define the generative step for function calling
        builder.generative_step(
            prompt=self.prompt,
            operator=Operator.FUNCTION_CALLING_RAW,
            outputs=[Write.new("calculation_result")],
        )

        # Define the workflow flow structure
        flow = [Edge(source="0", target="_end")]
        builder.flow(flow)

        # Set the final return value of the workflow
        builder.set_return_value("calculation_result")
        return builder.build()

    def callback(self, result: List[TaskResult]) -> List[SummationOutput]:
        """
        Parses the workflow results into validated output objects.

        Args:
            result: List of TaskResult objects

        Returns:
            List[SummationOutput]: List of validated summation outputs
        """
        outputs = []
        for task_result in result:
            for calculation in task_result.parse():
                outputs.append(
                    SummationOutput(
                        query=task_result.result, result=calculation.execute([SumTool])
                    )
                )
        return outputs
