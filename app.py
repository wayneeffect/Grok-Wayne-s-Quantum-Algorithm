from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import quantum_oracle as qo  # Import your core module

app = FastAPI(title="Grok & Wayne's Quantum Oracle")

class Request(BaseModel):
    mode: str  # e.g., "vqe_qaoa"
    params: dict  # Problem-specific (H, p, etc.)
    qpu_mode: str = "hybrid"  # Override env
    provider: str = "ibm"

@app.post("/oracle")
def run_oracle(req: Request):
    try:
        if req.mode == "vqe_qaoa":
            result = qo.hybrid_vqe_qaoa(req.params.get("H_problem"), req.params.get("H_mixer"), req.params.get("p", 1))
        elif req.mode == "vqe_vqf":
            result = qo.hybrid_vqe_vqf(req.params.get("multiplication_circuit"))
        elif req.mode == "vqe_qgans":
            result = qo.hybrid_vqe_qgans(req.params.get("generator"), req.params.get("discriminator"), req.params.get("params_g"), req.params.get("params_d"))
        elif req.mode == "vqe_qsvm":
            result = qo.hybrid_vqe_qsvm(req.params.get("kernel_matrix"), req.params.get("labels"))
        elif req.mode == "vqe_qpe":
            result = qo.hybrid_vqe_qpe(req.params.get("U"), req.params.get("initial_state"))
        elif req.mode == "vqe_krylov":
            result = qo.hybrid_vqe_krylov(req.params.get("H"), req.params.get("subspace_size", 3))
        else:
            raise ValueError("Invalid mode")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
