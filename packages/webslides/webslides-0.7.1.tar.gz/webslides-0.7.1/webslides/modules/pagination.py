import pandas as pd


def pagination_data(content, show_highlights_only):
    """
    :param pagedata: list of dicts with config and contents per page
    :return: df with pagination data, like pagenumber, category, page order
    """

    data = list()
    for topcat, subcats in content.items():
        for subcat, pages in subcats.items():
            for kp, vp in pages.items():
                item_copy = vp.copy()
                item_copy['topcat'] = topcat
                item_copy['subcat'] = subcat
                item_copy['pageid'] = kp

                # Check for the presence of 'footer' and 'highlights' keys
                if 'footer' not in item_copy:
                    item_copy['footer'] = None
                if 'highlights' not in item_copy:
                    item_copy['highlights'] = None

                data.append(item_copy)

    df = pd.DataFrame(data)

    # only keep page to be shown
    # nb. if shown is not defined for any of the content pages all pages will be shown
    if 'show' in df.columns:
        df = df[df.show != False]

    df['pagekey'] = df.index
    df = df.reset_index(drop=True)

    if 'topcat' in df.columns:
        df['next_tcat'] = df.topcat.shift(1)
    if 'subcat' in df.columns:
        df['next_scat'] = df.subcat.shift(1)

    # determine page keys of previous/next highlight page
    if 'highlights' in df.columns:
        # extra column 'highlight' indicating if page contains any highlights
        df['highlight'] = df.apply(lambda x: True if x['highlights'] else False, axis=1)

    # pagenumber, +1 because index starts on 0
    df['pageno'] = df.index + 1

    if 'highlights' in df.columns:
        df['hl_page'] = df.highlight * df.pageno

        # # define previous highlight page (hl_prev)
        df['hl_max'] = df.hl_page.cummax()  # cum_max
        df['hl_prev'] = df.hl_max.shift(1)  # cum_max

        # # define next highlight page (hl_next)
        df['hl_page2'] = df.hl_page.replace(0, 99)
        df['hl_min'] = df.loc[::-1, 'hl_page2'].cummin()[::-1]
        df['hl_next'] = df.hl_min.shift(-1).astype('Int64')

        # fill invalid references to next and previous highlight
        # dit is geval voor eerste en laatste highlight
        df['hl_prev'] = df['hl_prev'].fillna(0)
        df['hl_next'] = df['hl_next'].fillna(0)

        # next en previous page key toevoegen aan next en previous page number
        pagekey = dict(zip(df.pageno, df.pagekey))
        pagekey[0] = ''
        pagekey[99] = ''
        df['hl_prev_key'] = df.apply(lambda x: pagekey[x['hl_prev']], axis=1)
        df['hl_next_key'] = df.apply(lambda x: pagekey[x['hl_next']], axis=1)

        # drop temp highlight columns
        df = df.drop(['hl_page', 'hl_max', 'hl_page2', 'hl_min', 'hl_next', 'hl_prev'], axis=1)

    # remove nans (occur if certain keys are missing in content pages)
    # replacing with '' allows to check if a value is present
    df = df.fillna('')

    return df
