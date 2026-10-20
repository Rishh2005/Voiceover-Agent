from __future__ import annotations

from typing import List

from .models import FraudContext, RiskDecision, VoiceSignalFeatures


class VoiceRiskEngine:
    """Calculates a risk score for suspicious voice-based impersonation scenarios."""

    RISKY_ACTIONS = {
        "wire transfer",
        "payment approval",
        "account reset",
        "password change",
        "fund withdrawal",
        "security override",
        "sensitive verification",
    }

    def analyze(self, features: VoiceSignalFeatures, context: FraudContext) -> RiskDecision:
        score = self._score(features, context)
        severity = self._severity(score)
        reasons = self._reasons(features, context)
        recommended_action = self._recommendation(score)
        return RiskDecision(score=score, severity=severity, reasons=reasons, recommended_action=recommended_action)

    def _score(self, features: VoiceSignalFeatures, context: FraudContext) -> float:
        score = 0.0

        score += max(0.0, features.noise_ratio - 0.35) * 45
        score += max(0.0, features.pitch_variation - 0.6) * 30
        score += max(0.0, features.spectral_flatness - 0.5) * 28
        score += max(0.0, 0.7 - features.tempo_stability) * 26
        score += max(0.0, 0.72 - features.speech_ratio) * 20
        score += max(0.0, features.zero_crossing_rate - 0.25) * 18

        if context.mismatched_profile:
            score += 18
        if context.high_risk_channel:
            score += 12
        if context.urgency_level > 0.7:
            score += context.urgency_level * 24
        if context.previous_known_behavior < 0.5:
            score += (0.5 - context.previous_known_behavior) * 30

        requested_action = context.requested_action.lower()
        if any(keyword in requested_action for keyword in self.RISKY_ACTIONS):
            score += 14

        if context.expected_identity.lower() != "unknown" and context.caller_name.lower() != context.expected_identity.lower():
            score += 16

        if context.risk_notes:
            score += min(len(context.risk_notes), 8) * 2.5

        score = min(100.0, max(0.0, score))
        return round(score, 2)

    def _severity(self, score: float) -> str:
        if score >= 80:
            return "critical"
        if score >= 60:
            return "high"
        if score >= 35:
            return "medium"
        return "low"

    def _reasons(self, features: VoiceSignalFeatures, context: FraudContext) -> List[str]:
        reasons: List[str] = []

        if features.noise_ratio > 0.55:
            reasons.append("Elevated signal noise suggests possible synthetic or degraded audio capture.")
        if features.pitch_variation > 0.7:
            reasons.append("Pitch variance exceeds expected human voice stability patterns.")
        if features.spectral_flatness > 0.6:
            reasons.append("Spectral characteristics show signs of unnatural synthesis or manipulation.")
        if features.tempo_stability < 0.5:
            reasons.append("Temporal consistency is inconsistent with a natural human speaking cadence.")
        if context.urgency_level > 0.75:
            reasons.append("The caller is applying high-pressure urgency associated with social engineering attempts.")
        if context.mismatched_profile:
            reasons.append("The claimed identity does not align with the observed caller profile.")
        if context.high_risk_channel:
            reasons.append("The interaction is occurring through a channel known to be high risk for impersonation fraud.")
        if context.requested_action.lower() in {"wire transfer", "payment approval", "account reset", "security override"}:
            reasons.append("The requested action is sensitive and consistent with common fraud execution patterns.")

        if not reasons:
            reasons.append("Baseline checks are within a normal range; risk remains low but should still be monitored.")

        return reasons

    def _recommendation(self, score: float) -> str:
        if score >= 80:
            return "Block the call, trigger identity verification, and escalate to a human analyst immediately."
        if score >= 60:
            return "Request additional identity confirmation and place the call under manual review."
        if score >= 35:
            return "Continue with monitoring and require a secondary verification step."
        return "Allow the interaction with standard monitoring and routine logging."
