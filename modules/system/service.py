import modules.options_helper


def main(options):

    options_registry = ["name","status"]
    modules.options_helper.check_options(options, options_registry)

    name = options.get("name", False)
    status = options.get("status", False)


if __name__ == '__main__':
    main(options)
