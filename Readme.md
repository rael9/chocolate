Chocolate
=========

A __very__ basic static site generator.


Usage
-----

Create a config.json file. This should have a 'navigation' list and a 'pages' list. Use the config.json.example as a starting point.

Create a template.html file. This should have {navigation} where you want the navigation to be, and {body} where you want the HTML you create to be. Use template.html.example as a starting point.

Create the HTML files you want to be your pages in the 'content' folder.

Run ./chocolate.py.

Your new site will be in 'site'.

You should put any CSS, JS, etc. in the site folder.