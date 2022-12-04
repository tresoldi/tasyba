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

    logging.info("Loading Jinja2 template environment")

    # Build template_file and layout path; note that Jinja2 documentation says
    # that template names are not filesystem paths (even though
    # they map to filesystem paths), so that forward slashes should always be used,
    # even under Windows.
    template_path = Path(template_path).resolve()
    template_path = template_path.as_posix().replace("\\", "/")

    print("----", template_path)

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


# TODO: write properly etc. should load with other templates;
# TODO: also copy images if needed
def build_css(template_env, replaces, config):
    template = template_env.get_template("main.css")

    source = template.render(**replaces)

    # build and write css file
    file_path = Path("main.css")
    with open(file_path.as_posix(), "w") as handler:
        handler.write(source)


def build_tables(data, replaces, tables, template_env, config):
    # TODO: fitting the data to the what is expected by the template
    fields = config["single_table"]

    rows = []
    for row in data["single"]:
        subrow = [{"value": row[field], "url": None} for field in fields]
        rows.append(subrow)

    table_data = {"columns": [{"name": field} for field in fields], "rows": rows}

    for table in data:
        table_replaces = replaces.copy()
        table_replaces["datatable"] = table_data
        build_html(template_env, table_replaces, tables, f"{table}.html", config)


def build_sql_page(data, replaces, template_env, config):
    # Compute inline data replacements
    inline_data = {}
    for table_name in data:
        inline_data[table_name] = []
        for row in data[table_name]["rows"]:
            row_insert = ", ".join(
                ["'%s'" % cell["value"] if cell["value"] else "NULL" for cell in row]
            )
            inline_data[table_name].append(row_insert)

    # Build table schemata
    # TODO: use datatypes
    schemata = {}
    for table_name in data:
        schemata[table_name] = ", ".join(
            ["%s text" % col["name"].lower() for col in data[table_name]["columns"]]
        )

    # Generate page
    sql_replaces = replaces.copy()
    sql_replaces["data"] = inline_data
    sql_replaces["schemata"] = schemata
    build_html(template_env, sql_replaces, "sql.html", config)


def render_database(data, replaces, tables, config):
    """
    Render the database to HTML.
    """

    # Set the template path to the default one, if no other is provided
    # TODO: allow to specify a different template path
    template_path = None
    if not template_path:
        template_path = Path(__file__).parent.parent.parent / "templates" / "default"

    # Load Jinja HTML template environment
    template_env = load_template_env(template_path)

    # Build and write index.html
    build_html(template_env, replaces, tables, "index.html", config)

    # Build CSS files from template
    build_css(template_env, replaces, config)

    # Build tables from CLDF data
    build_tables(data, replaces, tables, template_env, config)

    # Build SQL query page
    # build_sql_page(data, replaces, template_env, config)
