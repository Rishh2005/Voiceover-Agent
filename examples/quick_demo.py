from voiceover_agent.engine import VoiceRiskEngine
from voiceover_agent.models import FraudContext, VoiceSignalFeatures


def demo() -> None:
    features = VoiceSignalFeatures(
        energy=0.72,
        zero_crossing_rate=0.3,
        pitch_variation=0.84,
        noise_ratio=0.68,
        tempo_stability=0.41,
        spectral_flatness=0.7,
        speech_ratio=0.74,
    )

    context = FraudContext(
        caller_name="Finance Director",
        expected_identity="Alex Morgan",
        requested_action="Wire transfer approval",
        urgency_level=0.86,
        previous_known_behavior=0.36,
        mismatched_profile=True,
        high_risk_channel=True,
        risk_notes=["The caller is requesting immediate fund movement.", "Identity mismatch detected."]
    )

    decision = VoiceRiskEngine().analyze(features, context)
    print({
        "score": decision.score,
        "severity": decision.severity,
        "recommended_action": decision.recommended_action,
        "reasons": decision.reasons,
    })


if __name__ == "__main__":
    demo()
