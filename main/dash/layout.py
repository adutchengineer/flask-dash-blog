import os
"""Plotly Dash HTML layout override."""
dir_path = os.getcwd()
with open(os.path.join(dir_path, 'main', 'templates', 'base.html'), 'r') as f:
    rows = f.readlines()
rows = [row.strip() for row in rows]
nav_index = rows.index('</nav>')
dash_str = rows[:nav_index+1] + ['{%app_entry%}',
                                 '<footer>'
                                 '{%config%}',
                                 '{%scripts%}',
                                 '{%renderer%}',
                                 '</footer>',
                                 '</body>',
                                 '</html>']

html_layout = "\n".join(dash_str)