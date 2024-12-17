import json
import os.path
import tempfile
import shutil
import subprocess

from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .const import TEMPLATES_PATH
from sphinx_helm.utils import flatten

yaml = YAML()


def load_chart(chartdir, root=None):
    """Load the yaml information from a Helm chart directory.

    Load in the `Chart.yaml` and `values.yaml` files from a Helm
    chart.

    Args:
        chartdir (str): Path to the Helm chart.
        root (list, optional): The root of the namespace we are currently at. Used for recursion.

    Returns:
        chart (dict): Contents of `Chart.yaml` loaded into a dict.
        values (dict): Contents of `values.yaml` loaded into a dict.

    """
    with open(os.path.join(chartdir, "values.yaml"), "r") as fh:
        values = yaml.load(fh.read())
    with open(os.path.join(chartdir, "Chart.yaml"), "r") as fh:
        chart = yaml.load(fh.read())
    return chart, list(traverse(values, root=root))


def load_chart_with_dependencies(chartdir, root=None):
    """
    Load and return dictionaries representing Chart.yaml and values.yaml from
    the Helm chart. If Chart.yaml declares dependencies, recursively merge in
    their values as well.

    Args:
        chartdir (str): Path to the Helm chart.
        root (list, optional): The root of the namespace we are currently at. Used for recursion.

    Returns:
        chart (dict): Contents of `Chart.yaml` loaded into a dict.
        values (dict): Contents of `values.yaml` loaded into a dict.
    """
    if root is None:
        root = []
    chart, values = load_chart(chartdir, root=root)
    if "dependencies" in chart:
        # update the helm chart's charts/ folder
        update_chart_dependencies(chartdir)

        # recursively update values by unpacking the helm charts in the charts/ folder
        for dependency in chart["dependencies"]:
            dependency_name = dependency["name"]
            dependency_path = os.path.join(
                chartdir, "charts", f"{dependency_name}-{dependency['version']}.tgz",
            )
            with tempfile.TemporaryDirectory() as tmpdirname:
                shutil.unpack_archive(dependency_path, tmpdirname)
                dependency_dir = os.path.join(tmpdirname, dependency_name)

                _, dependency_values = load_chart_with_dependencies(
                    dependency_dir, root + [dependency_name]
                )
                values = squash_duplicate_values(values + dependency_values)

    return chart, values


def squash_duplicate_values(values):
    """Remove duplicates from values.

    If a value has already been defined remove future values.

    Args:
        values (list): List of value tuples.

    Returns:
        values (list): List of value tuples with duplicated removed.

    """
    tmp = {}
    for item in values:
        if item[0] not in tmp:
            tmp[item[0]] = (item[1], item[2])
    return [(key, tmp[key][0], tmp[key][1]) for key in tmp]


def update_chart_dependencies(chart_path):
    """Update a helm charts local cache of dependencies.

    In order to generate a values table including dependencies we need
    all dependencies to be checked out locally. For each chart we are generating
    values for we will call ``helm dep update <chart>``.

    Args:
        chart_path (string): Path to the directory containing the helm chart
                             with dependencies to update to its charts/ folder.

    """
    if shutil.which("helm") is None:
        raise RuntimeError(
            "Unable to locate `helm` command which is needed for updating dependencies. "
            "Please ensure `helm` is installed and available on the path. "
            "Alternatively run sphinx-helm again with the `--no-deps` flag to skip generating "
            "value table entried for dependencies."
        )
    subprocess.check_call(
        ["helm", "dep", "update", "."],
        cwd=chart_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return None


def get_comment(tree, key):
    """Extract the in-line comment from a ruamel.yaml.comments.Comment list.

    When ruamel.yaml parses a YAML file it also extracts a ruamel.yaml.comments.Comment
    object for each item. This is a list of CommentToken objects which represent comments
    adjacent to the item.

    This function attempts to extract the comment which is on the same line as the item.

    Examples:
        Extract a comment

        >>> from ruamel.yaml import YAML
        >>> yaml = YAML()
        >>> tree = yaml.load("hello: world  # this is the comment")
        >>> get_comment(tree, "hello")
        "This is the comment"

    Args:
        comments (list): List of CommentToken objects (potentially nested)

    Returns:
        str: Comment

    """
    comments = tree.ca.items[key]
    linecol = tree.lc.data[key]
    for comment in flatten(comments):
        if isinstance(comment, str):
            return clean_comment(comment)
        if comment is not None and comment.start_mark.line == linecol[0]:
            first_line = comment.value.strip().split("\n")[0]
            return clean_comment(first_line)
    return ""


def clean_comment(comment):
    """Remove comment formatting.

    Strip a comment.

    Examples:
        Strip down a comment

        >>> clean_comment("# hello world")
        "hello world"

    Args:
        comment (str): Comment to clean

    Returns:
        str: Cleaned sentence

    """
    return comment.strip("# ")


def traverse(tree, root=None):
    """Iterate over a tree of configuration and extract all information.

    Iterate over nested configuration and extract parameters, comments and values.

    Parameters will be fully namespaced. Descriptions will be extracted from the inline
    comment. Values will be taken as the default value.

    Examples:
        Traversing the following YAML config would yield this list.

        my:
          config:
            hello: world  # comment to describe the option

        >>> traverse(tree)
        ['my.config.hello', 'Comment to describe the option', 'world']

    Args:
        comment (ruamel.yaml.comments.CommentedMap): Tree of config to traverse.
        root (list, optional): The root of the namespace we are currently at. Used for recursion.

    Yields:
        list(param, comment, value): Each namespaced parameter (str), the comment (str) and value (obj).

    """
    if root is None:
        root = []
    for key in tree:
        default = tree[key]
        if isinstance(default, dict) and default != {}:
            newroot = root + [key]
            for value in traverse(default, root=newroot):
                yield value
        else:
            if isinstance(default, list):
                default = [
                    (dict(item) if isinstance(item, CommentedMap) else item)
                    for item in default
                ]
            if isinstance(default, CommentedMap):
                default = dict(default)
            comment = ""
            if key in tree.ca.items:
                comment = get_comment(tree, key)
            param = ".".join(root + [key])
            yield [param, comment, json.dumps(default)]


def gen(chartdir, output_format, credits=True, deps=True):
    """Generate documentation for a Helm chart.

    Generate documentation for a Helm chart given the path to a chart and a
    format to write out in.

    Args:
        chartdir (str): Path to Helm chart
        output_format (str): Output format (maps to jinja templates in sphinx-helm)
        credits (bool): Show sphinx-helm credits in documentation
        deps (bool): Read values from chart dependencies and include them in the config table

    Returns:
        str: Rendered documentation for the Helm chart

    """
    chart, values = (
        load_chart_with_dependencies(chartdir) if deps else load_chart(chartdir)
    )

    templates = Environment(loader=FileSystemLoader([chartdir, TEMPLATES_PATH]))
    template = templates.get_template(f"{output_format}.jinja2")

    return template.render(**chart, values=values, credits=credits)
