def generate_index_page(df, show_topcat, show_subcat, tooltips, contents_title):
    """
    :param df: dataframe with page meta data
    :return: list with index page content (list of html strings)
    """

    # initð
    contents_title = 'Contents' if not contents_title else contents_title
    index_page_title = f"<h3 id='id_contents'>{contents_title}</h3>"
    index_page_content = '<table style="line-height: 1.6;"><tr><td style="padding:20px; vertical-align: top;">'
    tooltips_topcat = tooltips.get('topcats', None)
    tooltips_subcat = tooltips.get('subcats', None)


    # calc for splitting index page contents into columns
    helft = max(15, int(df.shape[0] / 2))  # aantal items per html table kolom, maar tenminste 15
    derde = max(15, int(df.shape[0] / 2.7))  # aantal items per html table kolom, maar tenminste 15

    # import category descriptions (to show as tooltip infobutton)
    # cats = import_categories()


    # category
    for i, r in df.iterrows():

        # invoegen top category label
        if 'topcat' in df.columns and show_topcat:
            if r['topcat'] != r['next_tcat']:
                tooltip = tooltips_topcat.get(r['topcat'], '') if tooltips_topcat else r['topcat']
                index_page_content += f"{'<br>' if i > 0 else ''}<span title='{tooltip}' style='color: white; background-color: #008AC9; padding:5px;'>{r['topcat'].upper()}</span><br><br>"

        # invoegen sub category label
        if 'subcat' in df.columns and show_subcat:
            if r['subcat'] != r['next_scat']:
                tooltip = tooltips_subcat.get(r['subcat'], '') if tooltips_subcat else r['subcat']
                index_page_content += f"<b><span title='{tooltip}'>{r['subcat']}</span></b><br>"

        if (i + 1) % derde == 0:  # nieuwe table column
            index_page_content += f'</td><td style="padding:20px; vertical-align: top;">'

        if 'highlight' in df.columns:
            bulb = df[df.index == i].highlight.values[0]  # bullet = &#8226;
        else:
            bulb = False
        index_page_content += f"&nbsp;&nbsp;&nbsp;&nbsp;{i + 1}.&nbsp;<a href='#{r['pagekey']}'>{df[df.index == i].title.values[0]}</a> {'&#128161;' if bulb else ''}<br>"

    index_page_content += f"</td></tr></table>"

    return index_page_title + index_page_content


def generate_highlights_page(df, show_topcat, show_subcat, tooltips):
    """
    :param df: dataframe with page meta data
    :return: list with highlights page content (list of html strings)
    """

    # init
    hl_page_title = f"<h3 id='highlights'>Highlights summary &#128161;</h3><span  style='line-height: 1.6;'>"
    hl_page_content = ''
    tooltips_topcat = tooltips.get('topcats', None)
    tooltips_subcat = tooltips.get('subcats', None)


    # add new line for each content page
    for i, r in df.iterrows():

        # testen of er tenminste 1 highlight binnen de topcat valt (anders topcat naam niet tonen)
        topcat_has_hl = False
        if 'topcat' in df.columns and show_topcat:
            if 'highlights' in df.columns:
                if df[df.topcat == r['topcat']]['highlights'].apply(lambda x: len(x) > 0).sum() > 0:
                    topcat_has_hl = True

        # testen of er tenminste 1 highlight binnen de subcat valt (anders subcat naam niet tonen)
        subcat_has_hl = False
        if 'subcat' in df.columns and show_subcat:
            if 'highlights' in df.columns:
                if df[df.subcat == r['subcat']]['highlights'].apply(lambda x: len(x) > 0).sum() > 0:
                    subcat_has_hl = True


        # invoegen top category label
        if 'topcat' in df.columns and show_topcat and topcat_has_hl:
            if r['topcat'] != r['next_tcat']:
                tooltip = tooltips_topcat.get(r['topcat'], '') if tooltips_topcat else r['topcat']
                hl_page_content += f'<br><span class="topcat" title="{tooltip}" style="color: white; background-color: #008AC9; padding:5px;">{r["topcat"].upper()}</span><br><br>'

        # invoegen sub category label
        if 'subcat' in df.columns and show_subcat and subcat_has_hl:
            if r['subcat'] != r['next_scat']:
                tooltip = tooltips_subcat.get(r['subcat'], '') if tooltips_subcat else r['subcat']
                hl_page_content += f'<b><span class="subcat" title="{tooltip}">{r["subcat"]}</span></b><br>'

        # show comments for highlighted titles
        if r['highlights']:
            for comment in r['highlights']:
                hl_page_content += f'&nbsp;&nbsp;&nbsp;&nbsp;&#8226;&nbsp;<a href="#{r["pagekey"]}">{r["title"]}</a>: {comment}<br>'

    hl_page_content += '</span>'

    return hl_page_title + hl_page_content
