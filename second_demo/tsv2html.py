import csv

def tsv2html(tsvfile, rows=None):
    """
    Convert the table in a tsvfile to a string with an HTML table.

    The function takes care of appropriately setting the HTML table
    header with <th> tags and the table body with <td> tags.
    """

    # Load the content of the tsv file as a dictionary of lists
    with open(tsvfile, 'r') as f:
        reader = csv.DictReader(f, dialect='excel-tab')
        data = list(reader)
        if rows is not None:
            data = data[:rows]

    # Build a buffer with the HTML table, first filling the header
    # and then all the rows
    headers = data[0].keys()
    html = ['<table>', '<thead>']
    html.append('<tr>')
    html.append("\n".join(['<th>%s</th>' % h for h in headers]))
    html.append('</tr>')
    html.append('</thead>')
    html.append('<tbody>')
    for row in data:
        html.append('<tr>')
        html.append("\n".join(['<td>%s</td>' % row[h] for h in headers]))
        html.append('</tr>')
    html.append('</tbody>')
    html.append('<tfoot>')
    html.append('<tr>')
    html.append("\n".join(['<th>%s</th>' % h for h in headers]))
    html.append('</tr>')
    html.append('</tfoot>')
    html.append('</table>')

    return "\n".join(html)

html = tsv2html('carib.tsv', 100)
with open("carib.html", "w") as f:
    f.write(html)