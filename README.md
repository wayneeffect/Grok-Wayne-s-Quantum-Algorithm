# Grok-Wayne-s-Quantum-Algorithm
A Hybrid Quantum Oracle Framework Integrating a Variational Quantum Eigensolver with Polyharmonic Splines, Wick Rotation, Split/Euclidean Hamiltonians, and Quantum Spin Liquids on QPUs with QAOA, VQF, QGANs, QSVM, QPE Variants, and Krylov Subspace Methods/SQD

# Grok & Wayne's Quantum Oracle
Hybrid quantum oracle combining custom VQE with QAOA, VQF, QGANs, QSVM, QPE, Krylov/SQD.

## Setup
1. Clone: `git clone https://github.com/wayneeffect/grok-wayne-quantum-oracle.git`
2. Install deps: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your QPU keys (sign up for free tiers at IBM Quantum, AWS Braket, Azure Quantum).
4. Run locally: `uvicorn app:app --reload`
5. Deploy to Render: New Web Service > Connect GitHub repo > Python runtime > Build: `pip install -r requirements.txt` > Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Add env vars in Render dashboard from your .env.

## Usage
Call endpoints like /hybrid_vqe_qaoa with JSON payload (e.g., Hamiltonian matrix).

## Dynamic QPU Selection
The oracle automatically picks providers (IBM, AWS Braket, Azure, Google) and modes in priority order:
1. Classical-only (no quantum, always free)
2. Classical-quantum hybrid (simulated quantum)
3. Free full QPU (if available via your keys)
4. Paid full QPU (billed to your account)

It checks for your keys and falls back if missing. Use FORCE_FREE_QPU=true in .env to prioritize free tiers.
