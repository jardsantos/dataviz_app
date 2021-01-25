from matplotlib import transforms, pyplot as plt
import re

def rainbow_text(x, y, texts, params,
                 orientation='horizontal', ax=None, **kwargs):
    """
    Adapted from https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/rainbow_text.html
    
    Take a list of *strings*, *colors* and *fontsizes* and place them next to each
    other, with text strings[i] being shown in colors[i].

    Parameters
    ----------
    x, y : float
        Text position in data coordinates.
    texts : list of str
        The texts to draw.
    params : list of dict
        List of specific kwargs
    orientation : {'horizontal', 'vertical'}
    ax : Axes, optional
        The Axes to draw into. If None, the current axes will be used.
    **kwargs
        All other keyword arguments are passed to plt.text(), so you can
        set the font size, family, etc.
    """
    if ax is None:
        ax = plt.gca()
    t = ax.transData
    canvas = ax.figure.canvas

    assert orientation in ['horizontal', 'vertical']
    if orientation == 'vertical':
        kwargs.update(rotation=90, verticalalignment='bottom')

    for s, p in zip(texts, params):
        _kwargs = kwargs.copy()
        _kwargs.update(p)
        text = ax.text(x, y, s, transform=t, **_kwargs)

        # Need to draw to update the text position.
        text.draw(canvas.get_renderer())
        ex = text.get_window_extent()

        if orientation == 'horizontal':
            t = transforms.offset_copy(
                text.get_transform(), x=ex.width, units='dots')
        else:
            t = transforms.offset_copy(
                text.get_transform(), y=ex.height, units='dots')

def plot_text(x, y, text, orientation='horizontal', ax=None, **kwargs):
    
    text = text.split('\n')
    lines = len(text)-1
    for i, _ in enumerate(text):
        texts = []
        params = []
        for __ in _.split('<style '):
            for j, ___ in enumerate(__.split('</style>')):
                if ___ == '':
                    break
                elif (len(__.split('</style>')) == 1) | (j==1):
                    texts.append('\n'*i + ___ + '\n'*(lines-i))
                    params.append({})
                else:
                    texts.append('\n'*i + re.match('(.*)?>(.*)', ___).group(2) + '\n'*(lines-i))
                    params.append({__key_value(k,0): __key_value(k, 1)
                                   for k in re.match('(.*)?>(.*)', ___).group(1).split(', ')})
        rainbow_text(x, y, texts, params, orientation, ax, **kwargs)
                    
    return texts, params            

def __key_value(x, i):
    x = x.split('=')
    try:
        return int(x[i].strip())
    except:
        return x[i].strip().replace("'", '').replace("\"", '')


def plot_annotate(text, xy, orientation='horizontal', ax=None, **kwargs):
    
    
    if ax is None:
        ax = plt.gca()
    if orientation == 'vertical':
        kwargs.update(rotation=90, verticalalignment='bottom')

    ax.annotate(re.sub('(<style .*?>)|(</style>)', '', text), xy, alpha=0, **kwargs)
    
    valid_kwargs = [
        'agg_filter', 'alpha', 'animated', 'backgroundcolor', 
        'clip_box', 'clip_on', 'clip_path', 'color', 'c', 
        'contains', 'figure', 'fontfamily', 'family', 'fontproperties', 
        'font_properties', 'fontsize', 'size', 'fontstretch', 'stretch', 
        'fontstyle', 'style', 'fontvariant', 'variant', 'fontweight', 
        'weight', 'gid', 'horizontalalignment', 'ha', 'in_layout', 
        'label', 'linespacing', 'multialignment', 'ma', 'path_effects', 
        'picker', 'position', 'rasterized', 'rotation', 'rotation_mode', 
        'sketch_params', 'snap', 'text', 'transform', 'url', 
        'usetex', 'verticalalignment', 'va', 'visible', 'wrap', 
        'x', 'y', 'zorder'
    ]
    
    if('xytext' in kwargs.keys()):
        if(('textcoords' in kwargs.keys()) & (kwargs['textcoords'] == 'offset points')):
            x = xy[0] + kwargs['xytext'][0]
            y = xy[1] + kwargs['xytext'][1]
        else:
            x, y = kwargs['xytext']
    else:
        x, y = xy

    kwargs = {k: v for k,v in kwargs.items() if k in valid_kwargs}

    plot_text(x,y , text, orientation, ax, **kwargs)