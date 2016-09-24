import modules.options_helper


def main(options):

    options_registry = ["name","command"]
    modules.options_helper.check_options(options, options_registry)



if __name__ == '__main__':
    main(options)
