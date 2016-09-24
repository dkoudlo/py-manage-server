import modules.options_helper as opt_helper


def main(options):

    options_registry = ["path","line","content"]
    opt_helper.check_options(options, options_registry)


if __name__ == '__main__':
    main(options)
