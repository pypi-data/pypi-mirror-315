import re
import subprocess
from functools import partial

svg_colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']

# Get the list of SVG color names
def dot_to_svg(source, config):
    # Could use -Tsvg:cairo for centering and polices problems : https://forum.graphviz.org/t/text-in-table-in-svg-output-not-completly-centered/2199
    # But messed up color replacements, and ids/hrefs would need to be updated too (see latex-superfence)
    args = ['dot', '-Tsvg']
    replacements = {}
    for k, v in config.items():
        if k in svg_colors:
            replacements[k] = v
        else:
            args += [f"-{k}={v}"]
    with subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        result, err = proc.communicate(input=source.encode())
        if err:
            return f"<pre>{err.decode()}</pre><pre>{source}</pre>"
        else:
            res = result.decode()
            # Replace color names with their config values
            for name, value in replacements.items():
                res = res.replace(f'fill="{name}"', f'fill="{value}"')
                res = res.replace(f'stroke="{name}"', f'stroke="{value}"')
            return res
def formatter(**kwargs):
    # Get config from mkdocs.yml
    return partial(_fence_dot_format, config=kwargs)


def _fence_dot_format(
    source, language='dot', class_name='dot', options={}, md=None, preview=False, config={}, **kwargs
):
    # Prioritize inline options over config file
    for k, v in options.items():
        config[k] = v
    pattern = r'^\s*:\w+:\s*\w+.*$'
    source = re.sub(pattern, '', source, flags=re.MULTILINE)

    svg = dot_to_svg(source, config)
    template = f"<p align=center>{svg}</p>"
    return template


def validator(language, inputs, options, attrs, md):
    okay = True
    # Get inline options from ```dot ...
    for k, v in inputs.items():
        options[k] = v
    print(options)
    return okay

