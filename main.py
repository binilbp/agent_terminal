from config.settings import Settings


def main():
    # default settings creation
    settings = Settings();

    # Set Run Type
    from llm import set_run_type

    settings = set_run_type(settings)


if __name__ == "__main__":
    main()
