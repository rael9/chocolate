Chocolate
=========

A __very__ basic static site generator.

Installation
------------

`clone git@github.com:rael9/chocolate.git project_name`

That should be it.

NOTICE
------

Version 2 has changed the format of the `config.json`. If you don't need the new features, you can continue to use your current config with version 1.

Usage
-----

Create a `config.json` file. This should have at least a `pages` array, and optionally a `settings` object.

Each `pages` entry should be an object with the following properties:

 - `input_file` (required) which is the filename of the content file to pull the HTML from
 - `output_file` (optional) if you want the output file to be something other than the `input_file` name.
 - `title` (required) which is the title of the page.
 - `name` (required) which is the text that will be used for the navigation link for this page.
 - `classname` (optional) to add a class to the navigation link.
 - `nav_exclude` (optional) if this is set to `true`, it will exclude this page from the navigation.

The `settings` object has the following possible properties:

 - `auto_index` which if set to `true` will tell the script to generate an index with the specifications set in the other properties.
 - `index_length` which is the number of previews of pages to put on the index.
 - `preview_length` which is the number of paragraphs to use for each preview.
 - `nav_inc_index` which is whether or not to include the index in the navigation.
 - `slug_class` which is the class to get the slug (preview title) from.

You can use the `config.json.example` as a starting point.

Create a `template.html` file. This should have `{navigation}` where you want the navigation to be, and `{body}` where you want the HTML you create to be. Use `template.html.example` as a starting point.

Create the HTML files you want to be your pages in the `content` folder.

Run `./chocolate.py` (add the `-h` flag if you want to see the optional flags).

Your new site will be in `site`.

You should put any CSS, JS, etc. in the `site` folder for testing purposes. Deployment is as easy as copying the contents of the `site` folder to your hosting platform.
