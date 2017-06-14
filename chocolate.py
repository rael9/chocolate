#!/usr/bin/env python3

import argparse
import json


def init_args():
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
        help='The location of the Generated site files.'
    )
    parser.add_argument(
        '-t', '--template',
        default='./template.html',
        dest='template',
        help='The location of the template file.'
    )
    return parser


def navigation_format(navigation, page):
    out_nav = ''
    try:
        for nav in navigation:
            classes = []
            if nav['page'] == page:
                classes.append('selected')
            if 'classname' in nav:
                classes.append(nav['classname'])
            link = nav['page']
            if link == 'index.html':
                link = ''

            out_nav += '<li'
            if len(classes):
                out_nav += ' class="' + ' '.join(classes) + '"'
            out_nav += '><a href="/' + link + '">' + nav['name'] + '</a></li>\n'
    except Exception as e:
        print('There was an error creating the navigation: {0}'.format(e))

    return out_nav


def main():
    parser = init_args()
    args = parser.parse_args()

    try:
        with open(args.config) as config_file:
            config = json.load(config_file)
    except Exception as e:
        print('The config file could not be parsed: {0}'.format(e))
        exit()

    try:
        with open(args.template) as template_file:
            template = template_file.read()

        for page in config['pages']:
            output_file = page['input_file']
            if 'output_file' in page:
                output_file = page['output_file']
            with open(args.destination + '/' + output_file, 'w') as outfile:
                with open(args.content + '/' + page['input_file']) as infile:
                    source = infile.read()

                outfile.write(
                    template.format(
                        title=page['title'],
                        navigation=navigation_format(config['navigation'], output_file),
                        body=source
                    )
                )
    except Exception as e:
        print('There was a problem processing the site: {0}'.format(e))
        exit()


if __name__ == "__main__":
    main()
