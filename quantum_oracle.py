import os
import pennylane as qml
from pennylane import numpy as np
from scipy.interpolate import Rbf  # For polyharmonic splines
from dotenv import load_dotenv

load_dotenv()

# Provider keys/config from .env (users fill their own)
IBMQ_TOKEN = os.getenv("IBMQ_TOKEN")
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
AZURE_RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP")
AZURE_WORKSPACE_NAME = os.getenv("AZURE_WORKSPACE_NAME")
AZURE_LOCATION = os.getenv("AZURE_LOCATION")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FORCE_FREE_QPU = os.getenv("FORCE_FREE_QPU", "true").lower() == "true"

PROVIDERS = ["ibm", "aws-braket", "azure", "google"]

def has_provider_key(provider):
    if provider == "ibm":
        return bool(IBMQ_TOKEN)
    elif provider == "aws-braket":
        return bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_REGION)
    elif provider == "azure":
        return bool(AZURE_SUBSCRIPTION_ID and AZURE_RESOURCE_GROUP and AZURE_WORKSPACE_NAME and AZURE_LOCATION)
    elif provider == "google":
        return bool(GOOGLE_PROJECT_ID and GOOGLE_API_KEY)
    return False

def get_device(wires=4, preferred_provider=None):
    # Prioritize modes: 1. classic, 2. hybrid, 3. free full QPU, 4. paid full QPU
    # Dynamically pick provider with key; prefer free tiers if FORCE_FREE_QPU

    # Mode 1: Classical-only (always available, no quantum)
    try:
        return qml.device("default.qubit", wires=wires)  # Pure classical sim
    except:
        pass  # Should always work

    # Mode 2: Classical-quantum hybrid (simulated quantum + classical opt)
    try:
        return qml.device("default.qubit.tf", wires=wires)  # TF backend for hybrid
    except:
        pass

    # Mode 3 & 4: Full QPU (free first, then paid)
    for provider in [preferred_provider] if preferred_provider else PROVIDERS:
        if has_provider_key(provider):
            if FORCE_FREE_QPU:
                # Prefer free/sim backends (e.g., IBM open simulators or free trials)
                if provider == "ibm":
                    return qml.device("qiskit.ibmq", wires=wires, ibmqx_token=IBMQ_TOKEN, backend="ibmq_qasm_simulator")
                elif provider == "aws-braket":
                    return qml.device("braket.aws.qubit", wires=wires, device_arn=f"arn:aws:braket::{AWS_REGION}:device/quantum-simulator/amazon/sv1")
                elif provider == "azure":
                    return qml.device("azure.quantum", wires=wires, subscription_id=AZURE_SUBSCRIPTION_ID, resource_group=AZURE_RESOURCE_GROUP, name=AZURE_WORKSPACE_NAME, location=AZURE_LOCATION, target="microsoft.estimator")  # Simulator first
                elif provider == "google":
                    return qml.device("cirq.simulator", wires=wires)  # Cirq sim as free fallback
            else:
                # Paid/full QPU
                if provider == "ibm":
                    return qml.device("qiskit.ibmq", wires=wires, ibmqx_token=IBMQ_TOKEN, backend="ibmq_manila")  # Example real QPU
                elif provider == "aws-braket":
                    return qml.device("braket.aws.qubit", wires=wires, device_arn=f"arn:aws:braket::{AWS_REGION}:device/qpu/ionq/Harmony")
                elif provider == "azure":
                    return qml.device("azure.quantum", wires=wires, subscription_id=AZURE_SUBSCRIPTION_ID, resource_group=AZURE_RESOURCE_GROUP, name=AZURE_WORKSPACE_NAME, location=AZURE_LOCATION, target="ionq.qpu.aria-1")
                elif provider == "google":
                    return qml.device("cirq.google", wires=wires, project_id=GOOGLE_PROJECT_ID, processor_id="sycamore")  # Example; requires setup
    # Ultimate fallback
    return qml.device("default.qubit", wires=wires)

# Rest of your core functions (custom_vqe, hybrids like hybrid_vqe_qaoa, etc.) remain the same, using get_device()
# Example: In custom_vqe, dev = get_device(wires=len(wires))
