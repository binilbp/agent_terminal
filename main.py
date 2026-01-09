from config.settings import Settings, set_run_type


def main():
    # default settings creation
    settings = Settings();

    # Set Run Type
    settings = set_run_type(settings)


if __name__ == "__main__":
    main()
