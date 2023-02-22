#!/usr/bin/env python3

import argparse
import json
import re


def init_args():
    """
    Get the command line arguments.
    :return:
    """
    parser = argparse.ArgumentParser(description='Build a templated site from HTML files.')
    parser.add_argument(
        '-c', '--config',
        default='./config.json',
        dest='config',
        help='The location of the global config file.'
    )
    parser.add_argument(
        '-s', '--source',
        default='./content',
        dest='content',
        help='The location of the HTML files to be included in the template.'
    )
    parser.add_argument(
        '-d', '--destination',
        default='./site',
        dest='destination',
        help='The location of the generated site files.'
    )
    parser.add_argument(
        '-t', '--template',
        default='./template.html',
        dest='template',
        help='The location of the template file.'
    )
    return parser


def navigation_format(navigation, page):
    """
    Generate navigation for the site
    :param navigation:
    :param page:
    :return:
    """
    out_nav = ''
    try:
        for nav in navigation:
            if not nav.get('nav_exclude', False):
                classes = []
                output_file = nav.get('output_file', nav['input_file'])
                if output_file == page:
                    classes.append('selected')
                if 'classname' in nav:
                    classes.append(nav['classname'])
                link = output_file
                if link == 'index.html':
                    link = ''

                out_nav += '<li class="{classes}"><a href="/{link}">{name}</a></li>\n'.format(
                    classes=' '.join(classes),
                    link=link,
                    name=nav['name']
                )
    except Exception as e:
        print('There was an error creating the navigation: {0}'.format(e))

    return out_nav


def main():
    # Get command line arguments
    parser = init_args()
    args = parser.parse_args()

    # Parse configuration file
    try:
        with open(args.config) as config_file:
            config = json.load(config_file)
    except Exception as e:
        print('The config file could not be parsed: {0}'.format(e))
        exit()

    # Get settings from the config
    settings = {}
    if 'settings' in config:
        settings = config['settings']
    auto_index = settings.get('auto_index', False)
    index_length = settings.get('index_length', 10)
    index_title = settings.get('index_title', 'Home')
    preview_length = settings.get('preview_length', 1)
    nav_inc_index = settings.get('nav_inc_index', False)
    slug_class = settings.get('slug_class', 'slug')

    count = 0

    # If configured, set up to auto-generate the index
    if auto_index and nav_inc_index:
        index_item = {
            "page": "index.html",
            "name": index_title
        }
        config['navigation'] = [index_item] + config['navigation']
    index_items = []
    preview_matcher = re.compile(r"(<p[^>]*>.*?</p>)")
    slug_matcher = re.compile(r'(<[^>]+class="{0}"[^>]*>[^<]+<[^>]+>)'.format(slug_class))

    # Process the site
    try:
        # Read in the specified template
        with open(args.template) as template_file:
            template = template_file.read()

        # Generate the configured pages
        for page in config['pages']:
            # Default to outputting to the same filename, unless overridden
            output_file = page.get('output_file', page['input_file'])

            # Open the output file
            with open(args.destination + '/' + output_file, 'w') as outfile:
                # Open the input file and read it
                with open(args.content + '/' + page['input_file']) as infile:
                    source = infile.read()

                # If configured to auto-generate the index, get the titles and previews from the
                # matched data in the pages
                if auto_index and count < index_length:
                    count += 1
                    data = {
                        "link": output_file,
                        "title": page['title'],
                        "slug": slug_matcher.search(source).group(),
                        "content": ''
                    }
                    paragraphs = preview_matcher.findall(source)
                    if paragraphs:
                        for paragraph in paragraphs[0:preview_length]:
                            data['content'] += paragraph + "\n"
                    index_items.append(data)

                # Generate and write the pages
                outfile.write(
                    template.format(
                        title=page['title'],
                        navigation=navigation_format(config['pages'], output_file),
                        body=source
                    )
                )
        # If configured to auto-generate the index, generate it and output it
        if auto_index:
            # Open the index file
            with open(args.destination + '/index.html', 'w') as index_file:
                index_str = ''
                # Generate the page content
                for ii in index_items:
                    index_str += '<h2><a href="{link}">{title}</a></h2>\n'.format(
                        link=ii['link'],
                        title=ii['title']
                    )
                    index_str += '{0}\n'.format(ii['slug'])
                    index_str += ii['content']
                # Generate and write the index
                index_file.write(
                    template.format(
                        title='Home',
                        navigation=navigation_format(config['pages'], 'index.html'),
                        body=index_str
                    )
                )
    # If there were any errors, let the user know
    except Exception as e:
        print('There was a problem processing the site: {0}'.format(e))
        exit()


if __name__ == "__main__":
    main()
