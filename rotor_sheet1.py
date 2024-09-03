import holoviews as hv
import panel as pn
import panel.widgets as pnw
import pandas as pd

url = 'https://github.com/Walter-hsieh/web/raw/main/rotor_data.xlsx'

df = pd.read_excel(url, sheet_name='工作表1')

print(df)


hv.extension('bokeh')

columns = sorted(df.columns)

discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(df[x].unique()) > 20]

# Create dropdowns for the x, y, size, and color axes
x = pnw.Select(name='X-Axis', value='dp-inlet', options=quantileable)
y = pnw.Select(name='Y-Axis', value='dp-outlet', options=quantileable)
size = pnw.Select(name='Size', value='None', options=['None', 'gen-temp'] + quantileable)
color = pnw.Select(name='Color', value='None', options=['None'] + discrete)

# Create a function to generate the plot based on the selected axes
@pn.depends(x.param.value, y.param.value, color.param.value, size.param.value)
def create_figure(x, y, color, size):
    opts = dict(cmap='rainbow', width=800, height=600, line_color='black', size=20)
    if color != 'None':
        opts['color'] = color
    if size != 'None':
        opts['size'] = hv.dim(size).norm()*20
    return hv.Points(df, [x, y], label="%s vs %s" % (x.title(), y.title())).opts(**opts)

widgets = pn.WidgetBox(x, y, color, size, width=200)

app = pn.Row(widgets, create_figure)

# # Replace the following lines:
# panel = pn.panel(app)
# if __name__ == '__main__':
#     panel.show()

# With this:
app.servable()