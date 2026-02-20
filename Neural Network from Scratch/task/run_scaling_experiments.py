from scaling_study import default_scaling_config, run_scaling_study


def main():
    config = default_scaling_config()
    rows = run_scaling_study(config)
    print(f"Completed scaling study with {len(rows)} experiments.")


if __name__ == "__main__":
    main()
