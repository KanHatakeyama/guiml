import ipywidgets as widgets
from io import BytesIO
from PIL import Image
import base64
from rdkit.Chem import Draw
from rdkit import Chem
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.palettes import Turbo256
from bokeh.transform import linear_cmap
from bokeh.models import CategoricalColorMapper
from bokeh.plotting import output_notebook, figure, show
from bokeh import plotting as bplot
from bokeh.transform import factor_cmap
from ipywidgets import interact
from bokeh.io import output_notebook, push_notebook, show


def b64_image_files(images):
    urls = []
    for im in images:
        out = BytesIO()
        im.save(out, format='png')
        png = out.getvalue()
        url = 'data:image_files/png;base64,' + \
            base64.b64encode(png).decode('utf-8')
        urls.append(url)
    return urls


def prepare_images(show_df, df, smiles_col):
    # make molecular images
    images = []
    for smiles in df[smiles_col]:
        images.append(Draw.MolToImage(
            Chem.MolFromSmiles(smiles), size=(128*2, 128*2)))

    filenames = b64_image_files(images)
    img_df = pd.DataFrame()
    img_df['image_files'] = filenames
    show_df = pd.merge(show_df, img_df, left_index=True,
                       right_index=True, how="inner")

    return show_df


def bokeh_plot(show_df, col_x, col_y, hue_name):
    source = ColumnDataSource(show_df)
    vmax = max(show_df[hue_name])
    vmin = min(show_df[hue_name])
    TOOLTIPS = f"""
        <div>
            <table border="0">
                <tr><td>@index</td></tr>
                <tr><td>{col_x} @{col_x}</td></tr>
                <tr><td>{col_y} @{col_y}</td></tr>
                <tr><td>{hue_name} @{hue_name}</td></tr>
                <tr><td style="padding:2px;">
                    <img
                    src="@image_files" height="120" alt="image"
                    style="float: left; margin: 0px 15px 15px 0px; image-rendering: pixelated;"
                    border="2"
                    ></img>
                </td></tr>
            </table>
        </div>
    """

    # bplot.output_file('plot.html')
    # グラフ初期設定
    tools = "pan,box_zoom,lasso_select,box_select,poly_select,tap,wheel_zoom,reset,save,zoom_in"
    p = figure(tools=tools,
               title=hue_name,
               # plot_width=1000,
               # plot_height=800,
               tooltips=TOOLTIPS)

    # numerical hue
    if show_df[hue_name].dtype is pd.Series([1.]).dtype:
        mapper = linear_cmap(field_name=hue_name,
                             palette=Turbo256, low=vmin, high=vmax)
    else:
        # categorical
        try:
            mapper = factor_cmap(hue_name,
                                 palette="Spectral5",
                                 factors=sorted(show_df[hue_name].unique()))
        except:
            mapper = None

    p.circle(x=col_x, y=col_y, source=source, size=12, color=mapper)

    p.xaxis.axis_label = col_x
    p.yaxis.axis_label = col_y
    # p.image_url(x=col_x, y=col_y, source=source,url="image_files",
    #            w=30,h=30, h_units = 'screen', w_units = 'screen',
    #           alpha=0.5)

    return show(p)
    # return show(p, notebook_handle=True)


def select_plot_columns(show_df,
                        x=None,
                        y=None,
                        hue=None):

    col_list = list(show_df.columns)

    plot_col_x_w = widgets.Select(
        description='x',
        options=col_list,
        disabled=False,
        value=x,
    )
    plot_col_y_w = widgets.Select(
        description='y',
        options=col_list,
        disabled=False,
        value=y,
    )
    plot_col_hue_w = widgets.Select(
        description='hue',
        options=col_list,
        disabled=False,
        value=hue,
    )

    box = widgets.HBox([plot_col_x_w, plot_col_y_w, plot_col_hue_w])

    return box, plot_col_x_w, plot_col_y_w, plot_col_hue_w
