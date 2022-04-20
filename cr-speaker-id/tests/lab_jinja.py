from jinja2 import Template

template = """
<html>
    <head></head>
    <body>
        <table border=1>
            <tr>
                {%- for column in columns %}
                <th>{{ column -}}</th>{% endfor %}
                <th>DELETE</th>
            </tr>
            {%- for value in values %}
            <tr>
                <td>{{ value.column_1 }}</td>
                <td>{{ value.column_2 }}</td>
                <td>{{ value.column_3 }}</td>
                <td>TRASH_CAN_ICON</td>
            </tr>
            {%- endfor %}
        </table>
    </body>
</html>
"""



data = {
    "columns": ["column-1", "column-2", "column-3"],
    "values": [
        {"column_1": "value-1-1", "column_2": "value-2-1", "column_3": "value-3-1", "column_url"},
        {"column_1": "value-1-2", "column_2": "value-2-2", "column_3": "value-3-2"},
    ]
}

j2_t = Template(template)
print(j2_t.render(data))


# Coding is required
# Troubleshooting
# Core technical skills
# 2 Others with supporting skills
# AI / ML specific experience.
# coding, trouleshooting, 3 other technical areas, Non-tech

# Timelines
# RRK - standard company Base Salary + 15%
# Base will go up.  100 70 / 30 -> 80 / 15 (can scale up to 25)
# Equity stays the same - until refresh, they tend to be larger grants.

# System Design / Cloud 
# Web Tech 
# AI (must cover 3 tech RRK areas.)
# Week 