import sys

# this options helper is usefull for parcing the options, checking string values, etc.
def check_options(input_opt, module_opt):
    if len(input_opt) == 0:
        print "No options passed to the module. Please check module playbook configuration."
    else:
        for option_keys in input_opt.iterkeys():
            try:
                module_opt.index(option_keys)
            except ValueError:
                print "Please check playbook configuration. The option name '" + option_keys + "' is not supported."
                print "Available options in this module are: " + ', '.join(module_opt)
                sys.exit("The option is not supported.")

def is_yes(option_val):
    if option_val == "yes":
        return True
    else:
        return False