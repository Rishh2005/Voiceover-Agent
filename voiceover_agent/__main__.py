from voiceover_agent import VoiceRiskEngine
from voiceover_agent.models import FraudContext, VoiceSignalFeatures


def main() -> None:
    engine = VoiceRiskEngine()
    features = VoiceSignalFeatures(
        energy=0.68,
        zero_crossing_rate=0.29,
        pitch_variation=0.82,
        noise_ratio=0.71,
        tempo_stability=0.44,
        spectral_flatness=0.67,
        speech_ratio=0.75,
    )

    context = FraudContext(
        caller_name="Chief Financial Officer",
        expected_identity="Harper Lee",
        requested_action="Payment approval",
        urgency_level=0.9,
        previous_known_behavior=0.3,
        mismatched_profile=True,
        high_risk_channel=True,
        risk_notes=["Urgent request for payment approval", "Mismatch with expected identity"],
    )

    decision = engine.analyze(features, context)
    print(f"Risk score: {decision.score}")
    print(f"Severity: {decision.severity}")
    print(f"Recommended action: {decision.recommended_action}")
    for reason in decision.reasons:
        print("-", reason)


if __name__ == "__main__":
    main()
