from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class VoiceSignalFeatures:
    energy: float = 0.0
    zero_crossing_rate: float = 0.0
    pitch_variation: float = 0.0
    noise_ratio: float = 0.0
    tempo_stability: float = 0.0
    spectral_flatness: float = 0.0
    speech_ratio: float = 0.0


@dataclass
class FraudContext:
    caller_name: str = "unknown"
    expected_identity: str = "unknown"
    account_type: str = "general"
    requested_action: str = "general review"
    urgency_level: float = 0.0
    previous_known_behavior: float = 1.0
    mismatched_profile: bool = False
    high_risk_channel: bool = False
    risk_notes: Optional[List[str]] = field(default_factory=list)


@dataclass
class RiskDecision:
    score: float
    severity: str
    reasons: List[str]
    recommended_action: str

    def as_dict(self) -> dict:
        return {
            "score": round(self.score, 2),
            "severity": self.severity,
            "reasons": self.reasons,
            "recommended_action": self.recommended_action,
        }
