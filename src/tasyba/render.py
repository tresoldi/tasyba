"""
Module with functions to render database contents to HTML.
"""

# Import Python standard libraries
from pathlib import Path
import datetime
import logging

# Import 3rd-party libraries
from jinja2 import Environment, FileSystemLoader

# TODO: accept Path objects
# TODO: have a default template directory?
def load_template_env(template_path: str) -> Environment:
    """
    Load a Jinja2 template environment.
    """

    logging.debug("Loading Jinja2 template environment")

    # Build template_file and layout path; note that Jinja2 documentation says
    # that template names are not filesystem paths (even though
    # they map to filesystem paths), so that forward slashes should always be used,
    # even under Windows.
    template_path = Path(template_path).resolve()
    template_path = template_path.as_posix().replace("\\", "/")

    template_env = Environment(loader=FileSystemLoader(template_path))

    return template_env


def build_html(template_env, replaces, tables, output_file, config):
    """
    Build and write an HTML file from template and replacements.
    """

    # Load proper template and apply replacements, also setting current date
    logging.info("Applying replacements to generate `%s`...", output_file)
    if output_file == "index.html":
        template = template_env.get_template("index.html")
    elif output_file == "sql.html":
        template = template_env.get_template("sql.html")
    else:
        template = template_env.get_template("datatable.html")

    source = template.render(
        tables=tables,
        file=output_file,
        current_time=datetime.datetime.now().ctime(),
        **replaces,
    )

    # Write
    with open(output_file, "w", encoding="utf-8") as handler:
        handler.write(source)

    logging.info("`%s` wrote with %i bytes.", output_file, len(source))


def render_database(data, replaces, tables, config):
    """
    Render the database to HTML.
    """

    # Set the template path to the default one, if no other is provided
    # TODO: allow to specify a different template path
    template_path = None
    if not template_path:
        template_path = Path(__file__).parent / "templates"

    # Load Jinja HTML template environment
    template_env = load_template_env(template_path)

    # Build and write index.html
    build_html(template_env, replaces, tables, "index.html", config)
