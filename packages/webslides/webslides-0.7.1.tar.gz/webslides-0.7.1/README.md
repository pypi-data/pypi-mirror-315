# Webslides

Webslides is a Python package that allows you to create PowerPoint-like slides in HTML format. It provides several advantages over traditional PowerPoint presentations, such as clickable content, interactivity with plotly figures and other elements, and the ability to create and update a presentation using Python.

## [Live demo](https://datadept.nl/webslides/demo.html)
Here is a [live demo](https://datadept.nl/webslides/demo.html) of an output of Webslides, demonstrating most of its features.

## Advantages

Some key advantages of using HTML over PowerPoint include:

- Easy to update by rerun of Python code (!)
- Pages can be as long (or short) as needed, which is handy for taller diagrams
- Content scaling by browser zoom level
- Interactive content (!)
  - Internal and external hyperlinks
  - Interactive tooltips
  - Interactive plotly figures
  - Interactivity with any other HTML elements, such as folium geographical maps
- Can be shared by attachment in email
- Compact file size

## Potential drawbacks

Let's be honest, potential drawbacks may be:

- Python is required to create and alter presentations
- Recipients cannot easily alter the presentation
- No WYSIWYG editing in a graphical user interface
- No easy conversion to PDF / print

## Main Features

Here are some of the things that Webslides does well:

- Generate an index page based on your content
- Generate a highlights page, based on your content
- Includes page navigation to easily navigate through the document
- Converts plotly figures to HTML

## Dependencies

Webslides has two dependencies:

- Pandas: a Python package that provides fast, flexible, and expressive data structures for data analysis
- Plotly: an interactive data visualization library that allows you to create a wide range of charts, graphs, and other visualizations
- Requests: for retrieving title and footer image

Webslides uses Pandas to process the content that is included in your presentation.
The Plotly package is used to convert Plotly figure objects to HTML.

## Installation

To install Webslides, simply run the following command:

`pip install webslides`

## Examples
Here are some examples to get you started:
```
## Create demo presentation and save to file demo.html

# imports
import webslides as ws

ws.demo()
```

```
## create most basic presentation with one slide, basic title page, no index page

# imports
import webslides as ws

# title_page
title_page = {
    'title_image_url': 'mylogo.png',   # or insert url
    'title': 'One Page Presentation',
    'summary': {'Context': 'Just some example to get started', 'Author': 'Me'},
}
    
# content
content = {
    'Topcat A': {
        'Subcat X': {
            'page1': {
                'title': 'Page title 1!',
                'highlights': ['- highlight 1', '- highlight 2'],
                'body': 'Content 1: this is a <b>HTML string</b>',
                'footer': ['- footer 3', '- <i>italic footer 4</i>']
            }
        }
     }
 }

# create presentation
ws.create(content=content
          , title_page=title_page
          , fname='webslides_basic_example.html'
          , open_in_browser=True
          , show_index_page=False
          , show_topcat=False
          , show_subcat=False
          , show_highlights_page=False
          , show_highlights_only=False
          , custom_css='')
```

## `create` Function Documentation

The `create` function is used to generate an HTML file with a custom structure based on the provided input parameters. It has the following parameters:

## Parameters

- **title_page** (dict, _optional_, default=None): A dictionary containing the title page information. It should include an image filename or URL (optional), a title, a summary, and a footer.

Example input:
```
    title_page = {
        'title_image_url': 'myimage.png',
        'title': 'Title of Title Page',
        'summary': {'Summary item 1': 'item text 1', 'Summary item 2': 'item text 2'},
        'footer': ['- use custom title image via the title_image_url parameter', '- footer2']
    }
```

- **content** (dict, _optional_, default=None): A dictionary containing the content pages organized by top categories and subcategories.


  Example input:
```
content = {
    'Topcat A': {
        'Subcat X': {
            'page1': {
                'title': 'Page Title 1 - HTML body',
                'highlights': ['- highlight 1', '- highlight 2'],
                'body': 'Content 1: this is a <b>HTML string</b>',
                'footer': ['- footer 1a', '- <i>italic footer 1b</i>'],
                'show': True},
                ...
            },
        ...
        },
    ...
}
```
- **fname** (str, _optional_, default='output.html'): The output filename or path+filename for the generated HTML file. If path is not existent, a subfolder wsout will be created.

- **open_in_browser** (bool, _optional_, default=True): If set to True, the generated HTML file will be opened in the default web browser.

- **show_index_page** (bool, _optional_, default=False): If set to True, an index page will be displayed with links to all content pages.

- **show_highlights_page** (bool, _optional_, default=False): If set to True, a highlights page will be displayed with a summary of the highlights from each content page.

- **show_topcat** (bool, _optional_, default=False): If set to True, the top category will be displayed in the index and highlights pages.

- **show_subcat** (bool, _optional_, default=False): If set to True, the subcategory will be displayed in the index and highlights pages.

- **show_highlights_only** (bool, _optional_, default=False): If set to True, only content pages with highlights will be shown in the index and highlights pages.

- **footer_image_url** (str, _optional_, default=None): Filename or web url of image to be used for logo in footer.

- **embed_images** : (bool, optional, default = True): If True, images will be embedded in the HTML file. Embedding increases file size.

- **contents_title** : (str, optional, default = 'Contents'): Heading of the contents page.

- **tooltips** (dict, _optional_, default=None): Dictionary with keys 'topcats' and 'subcats' and with topcat/subcat as keys, with each a dict wit keys and values with the respective topcat names and tooltip texts.

- **custom_css** (str, _optional_, default=None): String with custom CSS code to apply to output HTML. Can be used to adjust or overrule any styling, like logo size, background color etc.

## Examples custom CSS
- Change background color to white, font to Arial, remove rounded page corners:
```
custom_css = "body {font-family: Arial, sans-serif; background-color: #FFF} .page {border-radius:0px;}"
```

## Page Dictionary Parameters

Each content page dictionary within the content parameter can include the following keys:

- **title** (str, _mandatory_): The title of the content page.

- **body** (str or object, _mandatory_): The body of the content page. It can be a string containing HTML or an object (e.g., a Plotly figure).

- **highlights** (list of str, _optional_): A list of highlights for the content page. If not provided, no highlights will be displayed, and the page will not have a lightbulb icon in the index page.

- **footer** (list of str, _optional_): A list of footer items for the content page. Each item can include HTML tags.

- **show** (bool, _optional_): If set to False, the content page will be hidden in the output. If not provided or set to True, the page will be shown.



