# imports
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main as ws
import plotly.graph_objects as go


# simple plotly fig
def simple_fig():
    x = list(range(1, 11))
    y1 = [2 * i for i in x]
    y2 = [3 * i for i in x]
    trace1 = go.Scatter(x=x, y=y1, mode='markers+lines', name='Line 1')
    trace2 = go.Scatter(x=x, y=y2, mode='markers+lines', name='Line 2')
    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_layout(title='Simple Plotly Line Figure with Two Lines', height=600)
    return fig


# title page
title_page = {
    'title': 'Hello World!<br>Title of Title Page',
    'title_image_url': 'https://datadept.nl/webslides/package.png',
    'summary': {'Summary item 1': 'This presentation demonstrates some of the features of webslides and could be used as a starting point for a new presentation', 'Summary item 2': 'item text 2'},
    'footer': ['- configure title page image via the title_image_url parameter', '- configure custom footer image via the footer_image_url parameter']
}

# tooltips (optional!)
tooltips = {'topcats': {'Topcat A': 'Put your own tooltip text here',
                        'Topcat B': 'Put your own tooltip text here'},
            'subcats': {'Subcat X': 'Tooltip text for subcat x here',
                        'Subcat Y': 'Tooltip text for subcat y yere'}}

# content pages
content = {
    'Topcat A': {
        'Subcat X': {
            'page1': {
                'title': 'Page Title 1 - HTML body',
                'highlights': ['- highlight 1', '- highlight 2'],
                'body': 'Content 1: this is a <b>HTML string</b>',
                'footer': ['- footer 1a', '- <i>italic footer 1b</i>'],
                'show': True},
            'page2': {
                'title': 'Page Title 2 - No highlights',
                'body': 'Content 2: this is a <b>HTML string</b>',
                'footer': ['- Note: No highlights, so no lightbulb in the index page', '- <i>italic footer 2b</i>'],
                'show': True}
        },
        'Subcat Y': {
            'page3': {
                'title': 'Page Title 3 - Plotly fig !',
                'highlights': ['- highlight 3', '- note: no footer on this page'],
                'body': simple_fig(),
                'show': True}
        }
    },
    'Topcat B': {
        'Subcat Z': {
            'page4':
                {
                    'title': 'Page Title 4 - Different topcat',
                    'highlights': ['- highlight 5', '- highlight 6'],
                    'body': 'Content 3',
                    'footer': ['- footer 4a', '- footer 4b'],
                    'show': True
                }
        }
    }
}

custom_css = "body {font-family: Arial, sans-serif; background-color: #FFF} .page {border-radius:0px;} #title_page_image {width:400px !important;} .footer_image {width:200px;}"

# MAIN
ws.create(content=content
          , title_page=title_page
          , fname='hello_world.html'
          , open_in_browser=True
          , show_index_page=True
          , show_topcat=True
          , show_subcat=True
          , show_highlights_page=False
          , show_highlights_only=False
          , contents_title='Contents header'
          , footer_image_url='https://datadept.nl/img/datadept_logo_black.png'
          , embed_images=False
          , custom_css=custom_css
          , tooltips=tooltips)