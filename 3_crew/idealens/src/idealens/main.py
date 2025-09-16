#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from idealens.crew import Idealens

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the Idealens crew with a given topic and print the output.
    """
    inputs = {
        'motion': 'India vs usa',
    }

    try:
        result = Idealens().crew().kickoff(inputs=inputs)
        print(result.raw)  # Print the full raw output
    except Exception as e:
        raise Exception(f"An error occurred while running the Idealens crew: {e}")