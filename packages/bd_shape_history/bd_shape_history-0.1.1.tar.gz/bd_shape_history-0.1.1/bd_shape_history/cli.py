import sys
import importlib.util
from pathlib import Path

import ocp_vscode as ov

from bd_shape_history import ShapeHistory


def load_part(file_path: Path):
    module_name = '.'.join([*file_path.parent.parts, file_path.stem])

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    shape_module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = shape_module
    spec.loader.exec_module(shape_module)

    return shape_module


def get_shape_var(shape_str: str):
    str_path, variable_name = shape_str.split(':')
    part_module = load_part(Path(str_path))
    return part_module.__dict__[variable_name]


def get_shape_history(this_shape_str: str, that_shape_str: str) -> ShapeHistory:
    return ShapeHistory.from_objects(
        objs={
            this_shape_str: get_shape_var(this_shape_str),
            that_shape_str: get_shape_var(that_shape_str),
        },
        tesselate_hash=True,
    )


def export_diff_png(this_shape_str: str, that_shape_str: str, output_path: str):
    sh = get_shape_history(this_shape_str, that_shape_str)
    ov.set_defaults(render_edges=False)
    ov.show(sh.diff()[-1])
    ov.save_screenshot(output_path)


def run():
    if len(sys.argv) != 4:
        print(f'usage: { sys.argv[0] } <this_file_path>:<this_var_name> <that_file_path>:<that_var_name> <output_image_path>')
        print(f'example: { sys.argv[0] } ./examples/a.py:box ./examples/b.py:box diff.png')
        sys.exit(1)

    export_diff_png(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    run()
