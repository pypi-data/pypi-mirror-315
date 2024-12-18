import datetime as dt
import plotly.offline as po


def titlepage_to_html(html, page):
    # Generate the HTML
    title_imgage_src = page['title_image_src']
    if title_imgage_src:
        VAR_TITLE_IMAGE_HTML = f"<img id='title_page_image' src='{title_imgage_src}' style='width:300px; margin:50px 25px 25px 25px;'>"
    else:
        VAR_TITLE_IMAGE_HTML = ws_logo_html()

    # init
    titlepage = """<style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .centered-element {
            text-align: center;
            margin: 20px;
            width: 80%;
        }
    </style>
    <div class='container'>
        <div class='centered-element'>
            VAR_TITLE_IMAGE_HTML
            <h1>VAR_TITLE</h1><br>
            <p style='line-height: 1.5;'>
            VAR_SUMMARY</p>
        </div>
    </div>"""

    titlepage = titlepage.replace('VAR_TITLE_IMAGE_HTML', VAR_TITLE_IMAGE_HTML)
    titlepage = titlepage.replace('VAR_TITLE', page['title'])

    # generate summary html
    summary_html = """
        
        <!-- summary table -->
            <table style="width: 100%; text-align: left; font-size: 1em; border-collapse: collapse; border: 0;">
                <colgroup>
                    <col style="width: 20%;">
                    <col style="width: 80%;">
                </colgroup>
                <tbody style=" line-height:1.5em;">"""

    for k, v in page['summary'].items():
        summary_html += f"""
                    <tr style="border: 0;">
                        <td style="border: 0; padding: 10px; text-decoration: underline; vertical-align: top; text-align: right;">{k}</td>
                        <td style="border: 0; padding: 10px;">{v}</td>
                    </tr>
                    """

    summary_html += """
                </tbody>
            </table>"""

    titlepage = titlepage.replace('VAR_SUMMARY', summary_html)

    html = html.replace('<span></span>', titlepage + '<span></span>')

    # footer
    if 'footer' in page or 'footer_image_url' in page:
        footer = page['footer']
        footer.append(f"{dt.datetime.now().strftime('%e %b. %Y')}")
        footer_html = footer_to_html(page['footer'], footer_image_src=page['footer_image_src'])
        html = html.replace('<span></span>', footer_html + '<span></span>')

    return html


def content_to_html(html, page, show_topcat, show_subcat,
                    show_index_page=False,
                    show_highlights_page=False,
                    footer_image_src=None,
                    show_navi=False,
                    tooltips=None):
    # A. page navigation
    if show_navi:  # dont show for title page
        pagenavi = pagenavi_to_html(pageno=page['pageno'],
                                    pagekey=page['pagekey'],
                                    pageid=page['pageid'],
                                    show_index_page=show_index_page,
                                    show_highlights_page=show_highlights_page,
                                    prev_highlight_key=page.get('hl_prev_key', None),
                                    next_highlight_key=page.get('hl_next_key', None))
        html = html.replace('<span></span>', pagenavi + '<span></span>')

    # B. page title
    if 'title' in page and page['title'] != '':
        title = title_to_html(pageid=page['pageid'],
                              topcat=page['topcat'], subcat=page['subcat'],
                              title=page['title'], show_topcat=show_topcat,
                              show_subcat=show_subcat, tooltips=tooltips)
        html = html.replace('<span></span>', title + '<span></span>')

    # C. highlights
    if 'highlights' in page and page['highlights'] != '' and page['highlights'] != []:
        highlights_html = highlights_to_html(page['highlights'])
        html = html.replace('<span></span>', highlights_html + '<span></span>')

    # D. body
    if 'body' in page:
        body_html = body_to_html(page['body'])
        html = html.replace('<span></span>', body_html + '<span></span>')

    # E. footer
    if ('footer' in page and page['footer'] != '' and page['footer'] != []) or footer_image_src:
        footer_html = footer_to_html(page['footer'], footer_image_src)
        html = html.replace('<span></span>', footer_html + '<span></span>')

    return html


def pagenavi_to_html(pageno, show_index_page, pageid, show_highlights_page, pagekey,
                     prev_highlight_key, next_highlight_key):
    """
    :param pageno: int pagenumber
    :param name: str name of the html page (id used to navigate to this page, ie. from index page)
    :param show_index_page: bool if False, references to index page are omitted
    :param show_highlights_page: bool if False, references to highlights page are omitted
    :param prev_highlight_key: str html id of previous highlight page
    :param next_highlight_key: str html id of next highlight page
    :return: string html code to place on top of each page, used for
        - navigation to next/previous highlight page
        - navigation to index page
        - navigation to highlights page
        - display pagenumber
        - page id tag used to navigate to that page
    """

    link_prev = '' if prev_highlight_key == '' else f'<a title="Previous highlight" href="#{prev_highlight_key}">&#9664;</a>'
    link_next = '' if next_highlight_key == '' else f'<a title="Next highlight" href="#{next_highlight_key}">&#9658;</a>'

    pagenavi_index_page = f'<a id="{pagekey}" title="Table of contents" href="#id_contents">&#128196;</a> ' * show_index_page
    pagenavi_highlights_page = f'{link_prev} <a title="Highlights summary" href="#highlights">&#128161;</a> {link_next} ' * show_highlights_page

    pagenavi_html = f'<div class="page_nav" style="width: 100%; margin: 0 auto; text-align:right;" title="{pageid}">{pagenavi_highlights_page}{pagenavi_index_page}p{pageno}</div>'

    return pagenavi_html


def title_to_html(pageid='', topcat='', subcat='', title='', show_topcat=True, show_subcat=True, tooltips=dict()):
    """
    :param title: str title of html page
    :return: string html formatted title
    """

    pageid = title if pageid == '' else pageid
    tooltips_topcat = tooltips.get('topcats', dict())
    tooltips_subcat = tooltips.get('subcats', dict())
    tooltip_topcat = tooltips_topcat.get(topcat, topcat)
    tooltip_subcat = tooltips_subcat.get(subcat, subcat)

    topcat = f"<span class='topcat' style='color: white; background-color: #008AC9; padding:5px;' title='{tooltip_topcat}'>{topcat.upper()}</span> " if len(
        topcat) > 0 else ''
    subcat = f"<span class='subcat' style='font-weight: normal;' title='{tooltip_subcat}'>{subcat}</span>: " if len(
        subcat) > 0 else ''
    return f"<h3 class='page_title' style='line-height: 2;'>{show_topcat * topcat}{show_subcat * subcat}<span title='{pageid}'>{title}</span></h3>"


def highlights_to_html(highlights):
    """
    :param comments: list with text to show in header
    :return: string html formatted header
    """
    html = '''\n   
            <!-- highlights -->
           <div class=page_highlights" style="background-color: #EBEBEB; line-height: 1.6; padding:10px;">'''
    for o in highlights: html += f"{o}<br>"
    html += "</div>"
    return html


def body_to_html(body):
    # insert html string
    if isinstance(body, str):
        # add some padding to the body content
        return f'<div class="page_body" style="padding:3%; line-height:1.5em;">{body}</div>'

    # if not string, must be plotly fig object
    else:
        return f'''
        
            <!-- page body -->
            <div class="page_body" style="padding:3%">{po.plot(body, include_plotlyjs=False, output_type="div")}</div>'''


def footer_to_html(footer, footer_image_src=None):
    """
    :param footer: list with text to show in footer
    :param image_url: URL of the image to display on the right
    :return: string html formatted footer
    """

    html = '''
        
        <!-- footer -->
        <div style="display: flex; justify-content: space-between; align-items: center;">
    
        <!-- Footer text -->
        <div class="page_footer" style="background-color: #FFFFFF; line-height: 1.6; padding:10px; width: calc(100% - 120px);">
    '''

    # horizontal line
    if footer:
        html += '''    <hr style="width:20%; margin-left:0;">'''

    for o in footer:
        html += f"{o}<br>"

    # close footer text div
    html += "</div>\n"

    # image div
    if footer_image_src:
        html += f'''
        <!-- footer image -->
        <div><img src="{footer_image_src}" class="footer_image" alt="footer_image" style="height: auto; max-height: 100px; margin-right: 10px;"></div>
        '''

    # close footer div
    html += "</div>"

    return html


def ws_logo_html():
    return """
        <style>
        .title_page_image {
            width: 400px;
            height: 130px;
            margin: 50px auto;
            background: linear-gradient(to bottom right, white, #006fff);
            border: 3px solid #8ca5ff;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgb(0 0 0 / 30%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 60;
            color: #ededed;
        }
        </style>
        <div class="title_page_image">
            <span>Webslides</span>
        </div>
    """
