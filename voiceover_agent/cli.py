import argparse
import json

from .engine import VoiceRiskEngine
from .models import FraudContext, VoiceSignalFeatures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect suspicious voice impersonation patterns and assign a security risk score.")
    parser.add_argument("--caller-name", default="unknown", help="Name or identity claimed by the caller.")
    parser.add_argument("--expected-identity", default="unknown", help="The expected or trusted identity for this interaction.")
    parser.add_argument("--requested-action", default="general review", help="Action being requested by the caller.")
    parser.add_argument("--urgency", type=float, default=0.0, help="Urgency level from 0.0 to 1.0.")
    parser.add_argument("--previous-known-behavior", type=float, default=1.0, help="Trust score for previous known behavior, from 0.0 to 1.0.")
    parser.add_argument("--mismatched-profile", action="store_true", help="Flag if the caller identity does not match the expected profile.")
    parser.add_argument("--high-risk-channel", action="store_true", help="Flag if the interaction occurs on a high-risk channel.")
    parser.add_argument("--energy", type=float, default=0.55, help="Energy metric from 0.0 to 1.0.")
    parser.add_argument("--zero-crossing-rate", type=float, default=0.2, help="Zero crossing rate from 0.0 to 1.0.")
    parser.add_argument("--pitch-variation", type=float, default=0.35, help="Pitch variation from 0.0 to 1.0.")
    parser.add_argument("--noise-ratio", type=float, default=0.3, help="Noise ratio from 0.0 to 1.0.")
    parser.add_argument("--tempo-stability", type=float, default=0.7, help="Tempo stability from 0.0 to 1.0.")
    parser.add_argument("--spectral-flatness", type=float, default=0.4, help="Spectral flatness from 0.0 to 1.0.")
    parser.add_argument("--speech-ratio", type=float, default=0.8, help="Speech ratio from 0.0 to 1.0.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    features = VoiceSignalFeatures(
        energy=args.energy,
        zero_crossing_rate=args.zero_crossing_rate,
        pitch_variation=args.pitch_variation,
        noise_ratio=args.noise_ratio,
        tempo_stability=args.tempo_stability,
        spectral_flatness=args.spectral_flatness,
        speech_ratio=args.speech_ratio,
    )

    context = FraudContext(
        caller_name=args.caller_name,
        expected_identity=args.expected_identity,
        requested_action=args.requested_action,
        urgency_level=max(0.0, min(1.0, args.urgency)),
        previous_known_behavior=max(0.0, min(1.0, args.previous_known_behavior)),
        mismatched_profile=args.mismatched_profile,
        high_risk_channel=args.high_risk_channel,
    )

    result = VoiceRiskEngine().analyze(features, context)
    print(json.dumps({
        "caller": context.caller_name,
        "expected_identity": context.expected_identity,
        "requested_action": context.requested_action,
        "decision": result.as_dict(),
    }, indent=2))


if __name__ == "__main__":
    main()
