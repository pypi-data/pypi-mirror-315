import re
import subprocess
import os
import shutil
from functools import partial
import random
import string

def tex_to_svg(source, options):
    dirPath = ".latexTmp"
    os.makedirs(f"{dirPath}", exist_ok=True)
    with open(f"{dirPath}/latex.tex", "w", encoding="utf-8") as f:
        f.write(source)
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                "-output-directory", dirPath, f"{dirPath}/latex.tex"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e.output)
        shutil.rmtree(dirPath)
        return f"<pre>{e.output}</pre><pre>{source}</pre>"

    subprocess.run(
        ["pdfcrop", f"{dirPath}/latex.pdf", f"{dirPath}/latex_crop.pdf"],
        capture_output=True,
        text=True,
        check=True
    )
    subprocess.run(
        ["pdf2svg", f"{dirPath}/latex_crop.pdf", f"{dirPath}/latex.svg"],
        capture_output=True,
        text=True,
        check=True
    )
    with open(f"{dirPath}/latex.svg", "rb") as f:
        svg = f.read().decode("UTF8")
    blackfill = options.get('blackfill')
    if blackfill:
        svg = svg.replace("fill:rgb(0%,0%,0%)", f"fill:{blackfill}")
        svg = svg.replace("fill=\"rgb(0%, 0%, 0%)\"", f"fill=\"{blackfill}\"")
    blackstroke = options.get('blackstroke')
    if blackstroke:
        svg = svg.replace("stroke:rgb(0%,0%,0%)", f"stroke:{blackstroke}")
        svg = svg.replace("stroke=\"rgb(0%, 0%, 0%)\"", f"stroke=\"{blackstroke}\"")
    whitefill = options.get('whitefill')
    if whitefill:
        svg = svg.replace("fill:rgb(100%,100%,100%)", f"fill:{whitefill}")
        svg = svg.replace("fill=\"rgb(100%, 100%, 100%)\"", f"fill=\"{whitefill}\"")
    whitestroke = options.get('whitestroke')
    if whitestroke:
        svg = svg.replace("stroke:rgb(100%,100%,100%)", f"stroke:{whitestroke}")
        svg = svg.replace("stroke=\"rgb(100%, 100%, 100%)\"", f"stroke=\"{whitestroke}\"")    
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    svg = svg.replace("id=\"glyph", f"id=\"glyph{random_string}")
    svg = svg.replace("href=\"#glyph", f"href=\"#glyph{random_string}")
    shutil.rmtree(dirPath)
    return svg


def formatter(**kwargs):
    blackfill = kwargs.get('blackfill')
    blackstroke = kwargs.get('blackstroke')
    whitefill = kwargs.get('whitefill')
    whitestroke = kwargs.get('whitestroke')
    return partial(_fence_latex_format, blackfill=blackfill, blackstroke=blackstroke, whitefill=whitefill, whitestroke=whitestroke)


def _fence_latex_format(
    source, language='latex', class_name='latex', options={}, md=None, preview=False, blackfill=None, blackstroke=None, whitefill=None, whitestroke=None, **kwargs
):
    options['blackfill'] = options.get('blackfill', blackfill)
    options['blackstroke'] = options.get('blackstroke', blackstroke)
    options['whitefill'] = options.get('whitefill', whitefill)
    options['whitestroke'] = options.get('whitestroke', whitestroke)
    pattern = r'^\s*:\w+:\s*\w+.*$'
    source = re.sub(pattern, '', source, flags=re.MULTILINE)
    svg = tex_to_svg(source, options)
    template = f"<p align=center>{svg}</p>"
    return template


def validator(language, inputs, options, attrs, md):
    okay = True
    print(inputs)
    for k, v in inputs.items():
        options[k] = v
    return okay
