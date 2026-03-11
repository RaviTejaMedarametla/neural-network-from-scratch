from neural_network_from_scratch.metrics_schema import (
    KEY_DATASET,
    KEY_DATA_SOURCE,
    KEY_TRAIN_TIME,
    KEY_TRAIN_TIME_ALIAS,
    get_dataset_source,
    get_training_time_seconds,
    with_compatibility_aliases,
)


def test_with_compatibility_aliases_populates_missing_pairs():
    payload = {
        KEY_DATA_SOURCE: "fashion-mnist-local-csv",
        KEY_TRAIN_TIME_ALIAS: 12.3,
    }

    out = with_compatibility_aliases(payload)

    assert out[KEY_DATASET] == "fashion-mnist-local-csv"
    assert out[KEY_DATA_SOURCE] == "fashion-mnist-local-csv"
    assert out[KEY_TRAIN_TIME] == 12.3
    assert out[KEY_TRAIN_TIME_ALIAS] == 12.3


def test_get_helpers_accept_both_aliases():
    metrics_new = {KEY_DATASET: "d1", KEY_TRAIN_TIME: 33.0}
    metrics_old = {KEY_DATA_SOURCE: "d2", KEY_TRAIN_TIME_ALIAS: 44.0}

    assert get_dataset_source(metrics_new) == "d1"
    assert get_dataset_source(metrics_old) == "d2"
    assert get_training_time_seconds(metrics_new) == 33.0
    assert get_training_time_seconds(metrics_old) == 44.0
