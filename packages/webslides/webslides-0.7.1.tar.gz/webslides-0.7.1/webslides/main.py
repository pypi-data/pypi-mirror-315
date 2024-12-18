import os
import codecs
import webbrowser

from webslides.modules.other import *
from webslides.modules.tohtml import *
from webslides.modules.generate import *
from webslides.modules.pagination import *
from webslides.modules.input_validations import *


def create(content=None
           , title_page=None
           , fname=None
           , open_in_browser=True
           , show_title_page=True
           , show_index_page=False
           , show_topcat=False
           , show_subcat=False
           , show_highlights_page=False
           , show_highlights_only=False
           , contents_title=None
           , custom_css=None
           , footer_image_url=None
           , embed_images=True
           , tooltips=dict()):
    """
    Create an interactive presentation using the WebSlides framework.

    Parameters:
    -----------
    content : dict of dicts, mandatory
        page contents, organised in topcats, subcats and pages. Example structure:

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

    title_page : str, optional
        Custom content for the title page. If None, defaults to a standard title page.

    fname : str, optional
        The filename for the output HTML file. Defaults to 'output.html' if not specified.

    open_in_browser : bool, optional
        Whether to automatically open the generated HTML in a browser. Defaults to True.

    show_title_page : bool, optional
        Whether to include a title page. Defaults to True.

    show_index_page : bool, optional
        Whether to include an index page. Defaults to False.

    show_topcat : bool, optional
        Whether to display top categories on the index page. Defaults to True.

    show_subcat : bool, optional
        Whether to display subcategories on the index page. Defaults to True.

    show_highlights_page : bool, optional
        Whether to include a highlights page. Defaults to False.

    show_highlights_only : bool, optional
        If True, display only the highlights page and exclude other content. Defaults to False.

    footer_image_url : str, optional
        Filename or web url of image to be used for image in footer

    contents_title : str, optional
        Heading of the contents page, default = 'Contents'

    embed_images : bool, optional
        If True, images will be embedded in the HTML file. Embedding increases file size. default = True

    tooltips : dict, optional
        A dictionary of tooltips to enhance interactivity in the slides. Keys are element identifiers, and values are tooltip text.

    Returns:
    --------
    str
        The HTML code for the presentation.

    Notes:
    ------
    - Requires the WebSlides framework to be properly configured in your environment.
    - Ensure that any Plotly figure objects included in the content are properly serialized.
    """

    # INPUT VALIDATIONS
    if title_page:
        title_error = validate_title_page(title_page)
        if title_error:
            print(title_error)
            return

    if content:
        content_error = validate_content(content)
        if content_error:
            print(content_error)
            return
    else:
        print('content variable is mandatory')

    # create dataframe from pagedata list and enrich with pagination data
    df = pagination_data(content=content, show_highlights_only=show_highlights_only)

    #################
    ## CREATE HTML ##
    #################

    # page shadow css options: https://getcssscan.com/css-box-shadow-examples
    html = """
    <html>
    <head><meta charset="utf-8" />
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .page {padding:50px; margin:100px; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; background-color: white; border-radius:5px;}
        body {font-family: Verdana, Geneva, Arial, sans-serif; background-color: #EEE;}
        a {text-decoration: none;}
    </style>
    </head>
    <body>
    <span></span>
    </body>
    </html>
    """

    # get image source code from url
    title_image_src = retrieve_image_src(title_page.get('title_image_url'), embed_images)
    footer_image_src = retrieve_image_src(footer_image_url, embed_images)

    # 1. title page
    if title_page and show_title_page:
        page = {'title': title_page.get('title', ''),
                'title_image_src': title_image_src,
                'footer_image_src': footer_image_src,
                'summary': title_page.get('summary', ''),
                'footer': title_page.get('footer', list())}

        # start new page
        html = html.replace('<span></span>', '''
        <!-- TITLE PAGE -->
        <div class="page"><span></span></div>
        ''')

        # reuse contenpage_to_html function (normally used for content slides)
        html = titlepage_to_html(html, page)

        # close page
        html = html.replace('<span></span></div>', '</div><span></span>')

    # 2. index page
    if show_index_page:
        # start new page
        html = html.replace('<span></span>', '''
        
            <!-- INDEX PAGE -->
            <div class="page"><span></span></div>
            ''')
        indexpage_html = generate_index_page(df, show_topcat=show_topcat,
                                             show_subcat=show_subcat, tooltips=tooltips,
                                             contents_title=contents_title)
        html = html.replace('<span></span>', indexpage_html + '<span></span>')

        # close page
        html = html.replace('<span></span></div>', '</div><span></span>')

    # 3. highlights page
    if show_highlights_page:
        # start new page
        html = html.replace('<span></span>', '''
        
                    <!-- HIGHLIGHTS PAGE -->
            <div class="page"><span></span></div>
            ''')

        hlpage_html = generate_highlights_page(df, show_topcat=show_topcat, show_subcat=show_subcat, tooltips=tooltips)
        html = html.replace('<span></span>', hlpage_html + '<span></span>')

        # close page
        html = html.replace('<span></span></div>', '</div><span></span>')

    # 4. content pages
    for idx, page in df.iterrows():
        # start new page
        html = html.replace('<span></span>', '''
        
            <!-- CONTENT PAGE -->
            <div class="page"><span></span></div>
            ''')

        # insert content html
        html = content_to_html(html, page,
                               show_topcat=show_topcat,
                               show_subcat=show_subcat,
                               show_index_page=show_index_page,
                               show_highlights_page=show_highlights_page,
                               footer_image_src=footer_image_src,
                               show_navi=True,
                               tooltips=tooltips)

        # close page
        html = html.replace('<span></span></div>', '</div><span></span>')

    # 5. custom css
    if custom_css:
        # Style tag with custom css
        style_tag = f"<style>{custom_css}</style>"

        # instert style tag before closing </head> tag
        html = html.replace("</head>", f"{style_tag}\n   </head>")


    ###################
    ## HANDLE OUTPUT ##
    ###################

    # default output = wsout/output.html
    if not fname or fname == '':
        fname = 'output.html'
    current_working_dir = os.getcwd()
    fpath = os.path.join(current_working_dir, 'wsout', fname)
    wsoutpath = os.path.join(current_working_dir, 'wsout')

    # test if fname contains filename (with extension) or just base
    base, ext = os.path.splitext(fname)

    # fname contains a filename
    if ext:
        if os.path.exists(fname) or os.path.exists(base):
            fpath = fname

    # fname only contains directory name
    else:
        if os.path.isdir(fname):
            fpath = os.path.join(fname, 'output.html')
        else:
            fpath = os.path.join(current_working_dir, 'wsout', 'output.html')

    # create output directory 'wsout' if not present
    if 'wsout' in fpath and not os.path.exists(wsoutpath):
        os.makedirs(wsoutpath)

    with codecs.open(f"{fpath}", "w", encoding='utf-8') as f:
        f.write(html)
        print(f'INFO: output saved as {fpath}')


    # open in browser to check result
    if open_in_browser:
        webbrowser.open(fpath)
        print(f'INFO: opened in browser {fpath}')

    return None
