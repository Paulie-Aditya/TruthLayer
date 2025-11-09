# { "Depends": "py-genlayer:test" }

from genlayer import *

class TruthLayer(gl.Contract):
    next_id: u256
    claims: TreeMap[u256, str]
    results_json: TreeMap[u256, str]

    def __init__(self):
        self.next_id = u256(0)
        # instantiate TreeMaps
        self.claims = TreeMap[u256, str]()
        self.results_json = TreeMap[u256, str]()
        print(gl.eq_principle.prompt_non_comparative.__code__.co_varnames)


    @gl.public.write
    def submit_claim(self, claim: str) -> u256:
        claim_id = self.next_id
        self.next_id = self.next_id + u256(1)
        self.claims[claim_id] = claim
        
        self.results_json[claim_id] = gl.eq_principle.prompt_non_comparative(
            lambda: claim,
            task=(
                "You are a decentralized validator group. "
                "Research the following governance claim using reliable public web sources. "
                "Return STRICT MINIFIED JSON with keys: decision, confidence, evidence. "
                "decision ∈ {'true','false','uncertain'}. "
                "confidence ∈ [0.0,1.0] float (2 decimals). "
                "evidence = 1-5 https:// URLs supporting your verdict."
            ),
            criteria=(
                "Output MUST be valid minified JSON. "
                "MUST have EXACT keys: decision, confidence, evidence. "
                "decision MUST be 'true','false', or 'uncertain'. "
                "confidence MUST be numeric [0.0,1.0]. "
                "evidence MUST be array (1-5) of unique https:// URLs. "
                "Reject if formatting, types or logic invalid."
            )
        )

        return claim_id

    @gl.public.view
    def get_claim(self, claim_id: u256) -> str:
        return self.claims.get(claim_id, "")

    @gl.public.view
    def get_result_json(self, claim_id: u256) -> str:
        return self.results_json.get(claim_id, "")

    @gl.public.view
    def last_id(self) -> u256:
        return self.next_id
