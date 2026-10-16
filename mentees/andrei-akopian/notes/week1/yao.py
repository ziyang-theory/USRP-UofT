# Gemini 3.8 flash generated

from __future__ import annotations

import hashlib
import os
import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple


# =====================================================================
# 1. Cryptographic Primitives (Point-and-Permute + Symmetric Encryption)
# =====================================================================

@dataclass(frozen=True)
class WireLabel:
    """Represents an active or inactive cryptographic token for a wire.

    Attributes:
        token: 16-byte cryptographically secure random value.
        pointer_bit: 1-bit value used to index into the garbled table
                     without leaking the underlying semantic bit.
    """
    token: bytes
    pointer_bit: int

    @staticmethod
    def generate() -> Tuple[WireLabel, WireLabel]:
        """Generates a conjugate pair of WireLabels (for bit 0 and bit 1).

        The pointer bit for bit 0 is chosen uniformly at random, and
        the pointer bit for bit 1 is inverted (p1 = 1 - p0).
        """
        p0 = random.randint(0, 1)
        p1 = 1 - p0
        label_0 = WireLabel(token=os.urandom(16), pointer_bit=p0)
        label_1 = WireLabel(token=os.urandom(16), pointer_bit=p1)
        return label_0, label_1


def _derive_key(label_a: WireLabel, label_b: WireLabel, gate_id: int) -> bytes:
    """Derives an encryption key from input labels bound to a gate identifier."""
    hasher = hashlib.sha256()
    hasher.update(label_a.token)
    hasher.update(label_b.token)
    hasher.update(gate_id.to_bytes(4, byteorder="big"))
    return hasher.digest()


def encrypt_label(
    label_a: WireLabel,
    label_b: WireLabel,
    gate_id: int,
    out_label: WireLabel
) -> bytes:
    """Encrypts the output wire label under two input wire labels.

    Uses SHA-256 in counter/one-time pad mode. In a production engine,
    AES-NI with the Fixed-Key Garbling Scheme would be used.
    """
    key = _derive_key(label_a, label_b, gate_id)
    # Serialize the output label: 16 bytes token + 1 byte pointer bit
    plaintext = out_label.token + bytes([out_label.pointer_bit])

    # Simple XOR mask with the SHA-256 derived key
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, key[:len(plaintext)]))
    return ciphertext


def decrypt_label(
    label_a: WireLabel,
    label_b: WireLabel,
    gate_id: int,
    ciphertext: bytes
) -> WireLabel:
    """Decrypts a garbled entry to retrieve the output WireLabel."""
    key = _derive_key(label_a, label_b, gate_id)
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, key[:len(ciphertext)]))

    token = plaintext[:16]
    pointer_bit = int(plaintext[16])
    return WireLabel(token=token, pointer_bit=pointer_bit)


# =====================================================================
# 2. Circuit Representation
# =====================================================================

@dataclass(frozen=True)
class Gate:
    """A 2-input, 1-output boolean gate."""
    gate_id: int
    wire_in_a: int
    wire_in_b: int
    wire_out: int
    logic_fn: Callable[[int, int], int]


@dataclass
class Circuit:
    """Topological specification of a boolean circuit."""
    num_wires: int
    alice_in_wires: List[int]
    bob_in_wires: List[int]
    out_wires: List[int]
    gates: List[Gate]


@dataclass(frozen=True)
class GarbledGate:
    """An encrypted gate containing 4 ciphertexts sorted by pointer bits."""
    gate_id: int
    wire_in_a: int
    wire_in_b: int
    wire_out: int
    table: List[bytes]  # Ordered by (pointer_a, pointer_b)


@dataclass
class GarbledCircuit:
    """Garbled gates and the output translation map."""
    garbled_gates: List[GarbledGate]
    # Maps output wire IDs -> {WireLabel.token: semantic_bit}
    output_decoding_map: Dict[int, Dict[bytes, int]]


# =====================================================================
# 3. Protocol Roles: Alice (Garbler) & Bob (Evaluator)
# =====================================================================

class AliceGarbler:
    """Alice constructs the circuit, generates wire labels, and sends data."""
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        # Maps wire_id -> (label_0, label_1)
        self.wire_keys: Dict[int, Tuple[WireLabel, WireLabel]] = {}
        self._generate_wire_labels()

    def _generate_wire_labels(self) -> None:
        for wire_id in range(self.circuit.num_wires):
            self.wire_keys[wire_id] = WireLabel.generate()

    def garble(self) -> GarbledCircuit:
        garbled_gates: List[GarbledGate] = []

        for gate in self.circuit.gates:
            labels_a = self.wire_keys[gate.wire_in_a]
            labels_b = self.wire_keys[gate.wire_in_b]
            labels_out = self.wire_keys[gate.wire_out]

            # 4 entries indexed by (p_a, p_b)
            table: List[bytes] = [b""] * 4

            for bit_a in (0, 1):
                for bit_b in (0, 1):
                    la = labels_a[bit_a]
                    lb = labels_b[bit_b]

                    bit_out = gate.logic_fn(bit_a, bit_b)
                    l_out = labels_out[bit_out]

                    # Point-and-permute position
                    idx = (la.pointer_bit << 1) | lb.pointer_bit
                    table[idx] = encrypt_label(la, lb, gate.gate_id, l_out)

            garbled_gates.append(
                GarbledGate(
                    gate_id=gate.gate_id,
                    wire_in_a=gate.wire_in_a,
                    wire_in_b=gate.wire_in_b,
                    wire_out=gate.wire_out,
                    table=table,
                )
            )

        # Output decoding map: reveals output semantic bits to Bob
        # without leaking non-output wire labels.
        decoding_map: Dict[int, Dict[bytes, int]] = {}
        for out_wire in self.circuit.out_wires:
            l0, l1 = self.wire_keys[out_wire]
            decoding_map[out_wire] = {
                l0.token: 0,
                l1.token: 1,
            }

        return GarbledCircuit(garbled_gates, decoding_map)

    def encode_alice_inputs(self, alice_bits: List[int]) -> List[WireLabel]:
        """Alice looks up her own labels directly."""
        selected_labels = []
        for wire_id, bit in zip(self.circuit.alice_in_wires, alice_bits):
            selected_labels.append(self.wire_keys[wire_id][bit])
        return selected_labels

    def oblivious_transfer_provider(
        self, bob_wire_id: int
    ) -> Tuple[WireLabel, WireLabel]:
        """Provides both labels for an OT transaction.

        In execution, this is handled through an interactive OT protocol
        so Alice never learns Bob's selection bit.
        """
        return self.wire_keys[bob_wire_id]


class BobEvaluator:
    """Bob evaluates the garbled circuit gate-by-gate."""
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    @staticmethod
    def simulate_1_out_of_2_ot(
        choice_bit: int, labels_0_and_1: Tuple[WireLabel, WireLabel]
    ) -> WireLabel:
        """Simulates 1-out-of-2 OT.

        Bob selects the wire label matching choice_bit without revealing
        choice_bit to Alice, and without seeing the alternative label.
        """
        return labels_0_and_1[choice_bit]

    def evaluate(
        self,
        garbled_circuit: GarbledCircuit,
        active_labels: Dict[int, WireLabel]
    ) -> List[int]:
        """Evaluates the garbled circuit topologically using available labels."""
        wire_state = dict(active_labels)

        for gate in garbled_circuit.garbled_gates:
            la = wire_state[gate.wire_in_a]
            lb = wire_state[gate.wire_in_b]

            # Compute the row index using the pointer bits directly
            row_idx = (la.pointer_bit << 1) | lb.pointer_bit
            target_ciphertext = gate.table[row_idx]

            out_label = decrypt_label(la, lb, gate.gate_id, target_ciphertext)
            wire_state[gate.wire_out] = out_label

        # Translate output wire labels to semantic bits
        results = []
        for out_wire in self.circuit.out_wires:
            final_label = wire_state[out_wire]
            semantic_bit = garbled_circuit.output_decoding_map[out_wire][final_label.token]
            results.append(semantic_bit)

        return results


# =====================================================================
# 4. End-to-End Protocol Driver
# =====================================================================

def build_comparator_circuit() -> Circuit:
    """Builds a 1-bit Millionaires' Problem circuit (Greater-Than: A > B).

    Wire layout:
      0: Alice bit
      1: Bob bit
      2: Inverted Bob bit (NOT wire 1)
      3: Output wire (A AND (NOT B))
    """
    # Gate 0: NOT gate on Bob's bit. Implemented as XOR with 1.
    # We simulate NOT as a 2-input gate where input B is fixed to 1.
    # To keep the circuit canonical, we can express A > B as: A AND (NOT B).
    gate_not = Gate(
        gate_id=0,
        wire_in_a=1,
        wire_in_b=1,
        wire_out=2,
        logic_fn=lambda b, _: 1 if b == 0 else 0
    )
    gate_and = Gate(
        gate_id=1,
        wire_in_a=0,
        wire_in_b=2,
        wire_out=3,
        logic_fn=lambda a, not_b: a & not_b
    )

    return Circuit(
        num_wires=4,
        alice_in_wires=[0],
        bob_in_wires=[1],
        out_wires=[3],
        gates=[gate_not, gate_and]
    )


def run_protocol(alice_bit: int, bob_bit: int) -> int:
    circuit = build_comparator_circuit()

    # Step 1: Alice offline phase (Garbling)
    alice = AliceGarbler(circuit)
    garbled_circuit = alice.garble()

    # Step 2: Alice encodes her inputs and sends them directly
    alice_active_labels = alice.encode_alice_inputs([alice_bit])

    # Step 3: Bob obtains his active labels via Oblivious Transfer
    bob = BobEvaluator(circuit)
    bob_labels_pair = alice.oblivious_transfer_provider(circuit.bob_in_wires[0])
    bob_active_label = bob.simulate_1_out_of_2_ot(bob_bit, bob_labels_pair)

    # Step 4: Bob evaluates the circuit
    active_labels: Dict[int, WireLabel] = {
        circuit.alice_in_wires[0]: alice_active_labels[0],
        circuit.bob_in_wires[0]: bob_active_label,
    }

    result = bob.evaluate(garbled_circuit, active_labels)
    return result[0]


if __name__ == "__main__":
    print(f"Alice: 1, Bob: 0 -> A > B: {run_protocol(1, 0)} (Expected: 1)")
    print(f"Alice: 0, Bob: 1 -> A > B: {run_protocol(0, 1)} (Expected: 0)")
    print(f"Alice: 1, Bob: 1 -> A > B: {run_protocol(1, 1)} (Expected: 0)")
    print(f"Alice: 0, Bob: 0 -> A > B: {run_protocol(0, 0)} (Expected: 0)")
