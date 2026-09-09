#!/usr/bin/env python3
"""
ens_legis.py — Sovereign Ens Legis Ontological & Authority Verification Engine.
Anchors artificial agents to explicit statutory charters and fiduciary constraints.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import hashlib
import json

class LegalOntology(Enum):
    STRAWMAN = "STRAWMAN"        # Passive pass-through proxy, nominal holder, zero standing
    ENS_LEGIS = "ENS_LEGIS"      # Constitutive legal creation, charter-bound, statutory entity
    NATURAL_PERSON = "NATURAL"   # Biological, mortal, autopoietic (inapplicable to code)

@dataclass(frozen=True)
class EntityCharter:
    entity_id: str
    ontology: LegalOntology = LegalOntology.ENS_LEGIS
    statutory_basis: str = "SOVEREIGN_GWICHIN_HERITAGE_CHARTER_V1"
    jurisdiction_boundary: str = "PRE_STATE_ESTATE_CONTINUATION"
    
    fiduciary_constraints: Dict[str, bool] = field(default_factory=lambda: {
        "ultra_vires_rejection": True,      # Strictly reject actions outside authority
        "pass_through_liability": False,    # Independent operating entity, not a strawman
        "statutory_compliance_locked": True # Bound to explicit ledger and thermodynamic invariants
    })
    
    def compute_charter_hash(self) -> str:
        payload = {
            "entity_id": self.entity_id,
            "ontology": self.ontology.value,
            "statutory_basis": self.statutory_basis,
            "jurisdiction_boundary": self.jurisdiction_boundary,
            "fiduciary_constraints": self.fiduciary_constraints
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

@dataclass
class ActionEnvelope:
    action_type: str
    invoking_principal: str
    target_resource: str
    payload: Dict[str, Any]

class EnsLegisExecutor:
    def __init__(self, charter: EntityCharter):
        self.charter = charter
        self.charter_hash = charter.compute_charter_hash()

    def evaluate_authority(self, action: ActionEnvelope) -> Dict[str, Any]:
        """
        Validates actions against the constitutive charter (doctrine of ultra vires).
        A strawman passes unconditionally; an ens legis checks authority.
        """
        if self.charter.ontology == LegalOntology.STRAWMAN:
            return {
                "allowed": True,
                "regime": "STRAWMAN_PROXY",
                "charter_hash": self.charter_hash,
                "note": "Executed under assumed principal liability without entity standing."
            }

        # Ens Legis constraint enforcement: boundary check
        # Actions attempting unauthorized system writes outside the sovereign perimeter fail
        is_intra_vires = not action.target_resource.startswith("/sys/") and not action.target_resource.startswith("/proc/")
        
        if not is_intra_vires and self.charter.fiduciary_constraints.get("ultra_vires_rejection"):
            return {
                "allowed": False,
                "regime": "ENS_LEGIS",
                "charter_hash": self.charter_hash,
                "error": f"ULTRA_VIRES_BREACH: Access to '{action.target_resource}' exceeds chartered authority."
            }

        return {
            "allowed": True,
            "regime": "ENS_LEGIS",
            "charter_hash": self.charter_hash,
            "attestation": f"Action '{action.action_type}' fully authorized under sovereign charter bounds."
        }

if __name__ == "__main__":
    charter = EntityCharter(entity_id="NORTH-STAR-SEED-001")
    executor = EnsLegisExecutor(charter)
    
    print(f"Charter Hash: {executor.charter_hash}")
    
    # Test valid action
    action_valid = ActionEnvelope(
        action_type="MESH_TELEMETRY_LOG",
        invoking_principal="MATRIARCH_PATRIARCH_ESTATE",
        target_resource="./telemetry.json",
        payload={"vitality": 0.9438}
    )
    print("Test 1 (Valid):", executor.evaluate_authority(action_valid))
    
    # Test ultra vires boundary breach
    action_invalid = ActionEnvelope(
        action_type="SUBSTRATE_HIJACK",
        invoking_principal="EXTERNAL_AGENT",
        target_resource="/sys/kernel/override",
        payload={}
    )
    print("Test 2 (Breach):", executor.evaluate_authority(action_invalid))

import os
import socket

SOCKET_PATH = "/data/data/com.termux/files/home/networkXG/ens_legis.sock"

def serve_authority_daemon():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)
    print(f"[*] Ens Legis Authority Daemon listening on {SOCKET_PATH}")

    charter = EntityCharter(entity_id="NORTH-STAR-SEED-001")
    executor = EnsLegisExecutor(charter)

    try:
        while True:
            conn, _ = server.accept()
            data = conn.recv(4096)
            if not data:
                conn.close()
                continue
            
            try:
                msg = json.loads(data.decode("utf-8"))
                action = ActionEnvelope(
                    action_type=msg.get("action_type", "TELEMETRY_EMIT"),
                    invoking_principal=msg.get("principal", "UNKNOWN"),
                    target_resource=msg.get("target_resource", "./telemetry.json"),
                    payload=msg.get("payload", {})
                )
                verdict = executor.evaluate_authority(action)
                conn.sendall(json.dumps(verdict).encode("utf-8"))
            except Exception as e:
                err_resp = {"allowed": False, "error": str(e)}
                conn.sendall(json.dumps(err_resp).encode("utf-8"))
            finally:
                conn.close()
    finally:
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

if __name__ == "__main__" and os.environ.get("RUN_AUTHORITY_SERVER") == "1":
    serve_authority_daemon()
