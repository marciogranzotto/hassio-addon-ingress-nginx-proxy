
import json
import os
import contextlib

def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return ui


name = sanitised_input("Enter the desired add-on name: ", str)
slug = sanitised_input("Enter the slug: ", str.lower)
panel_icon = sanitised_input("Enter side pannel icon (like mdi:car): ", str.lower)
panel_admin_str = sanitised_input("Only show at panel for admins? (true/false): ", str.lower, range_=('true', 'false'))
panel_admin = panel_admin_str == "true"


filename = 'config-sample.json'
with open(filename, 'r') as f:
    print("\n\nReading config.json...")
    data = json.load(f)
    print(data)

    print("\n\Editting config.json...")
    data['name'] = name
    data['slug'] = slug
    data['ingress_entry'] = slug
    data['panel_icon'] = panel_icon
    data['panel_admin'] = panel_admin
    print(data)

filename = 'config.json'
with contextlib.suppress(FileNotFoundError):
    os.remove(filename)
with open(filename, 'w') as f:
    print("\n\Saving config.json...")
    json.dump(data, f, indent=4)

print("Done!")
