import csv
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from benchmark import run_benchmarks


class BenchmarkModuleTests(unittest.TestCase):
    def test_benchmark_generates_csv_with_expected_columns(self):
        output_name = 'test_benchmark_results.csv'
        output_path, rows = run_benchmarks(
            batch_sizes=[8],
            precision_modes=['float32', 'int8'],
            model_sizes=[[8, 16, 3]],
            output_csv=output_name,
            n_samples=64,
            epochs=1,
            seed=123,
        )

        self.assertTrue(output_path.exists())
        self.assertEqual(len(rows), 2)

        with output_path.open('r', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            cols = reader.fieldnames

        self.assertIn('train_time_per_epoch_s', cols)
        self.assertIn('inference_latency_per_sample_s', cols)
        self.assertIn('batch_throughput_samples_per_s', cols)
        self.assertIn('peak_memory_mb', cols)
        self.assertIn('cpu_utilization_percent', cols)

        output_path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
