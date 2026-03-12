from neural_network_from_scratch.metrics_schema import normalize_metrics_payload


def test_normalize_metrics_payload_accepts_legacy_aliases():
    payload = {
        "data_source": "fashion-mnist-local-csv",
        "train_time_seconds": 12.34,
        "test_accuracy_percent": 93.2,
    }

    normalized = normalize_metrics_payload(payload)

    assert normalized["dataset"] == "fashion-mnist-local-csv"
    assert normalized["training_time_seconds"] == 12.34
    assert normalized["test_accuracy_percent"] == 93.2


def test_normalize_metrics_payload_prefers_canonical_keys_when_both_provided():
    payload = {
        "dataset": "canonical-dataset",
        "data_source": "legacy-dataset",
        "training_time_seconds": 5.0,
        "train_time_seconds": 9.0,
    }

    normalized = normalize_metrics_payload(payload)

    assert normalized["dataset"] == "canonical-dataset"
    assert normalized["training_time_seconds"] == 5.0
