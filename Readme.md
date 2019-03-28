Chocolate
=========

A __very__ basic static site generator.

Installation
------------

`clone git@github.com:rael9/chocolate.git project_name`

That should be it.

Usage
-----

Create a config.json file. This should have a `navigation` list and a `pages` list.

Each `navigation` item should have a `page` which is the name of the html file this link should navigate to, and a `name`, which is the text for the link. It can also have a `classname` if you want the specific `li` to have a class. The navigation will be returned as an `li` for each nav item, with a `selected` class on the current page.

Each `pages` item should have a `input_file` which is the filename of the content file to pull the HTML from and a `title` which is the title of the page. You can also have an `output_file` if you want it to be something other than the `input_file` name.

Use the config.json.example as a starting point.

Create a template.html file. This should have {navigation} where you want the navigation to be, and {body} where you want the HTML you create to be. Use template.html.example as a starting point.

Create the HTML files you want to be your pages in the 'content' folder.

Run ./chocolate.py.

Your new site will be in 'site'.

You should put any CSS, JS, etc. in the site folder.
