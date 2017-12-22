'''
Module with functions to plot a plotly graph
'''
from plotly.graph_objs import Scatter, Marker, Data, Figure, Layout, Font, YAxis, Margin
import networkx as nx

def scatter_nodes(pos, labels=None, size=8, opacity=1,
                  title="Centrality", data=None, nodes=None,
                  colorscale='Hot'):
    '''
    Function to create a trace of scatter points to represent a node
    on the plot.
    Args:
        pos (dict): node positions
        labels (list): labels of len(pos), to be displayed when hovering the
            mouse over the nodes
        size (int): size of the dots representing the nodes
        opacity (float): value between [0,1] defining the node color opacity
        title (str): Title to be put on top of the colorbar
        data (dict): Measure to be plotted
        nodes (list): List with nodes id
        colorscale (str): colorscale for the data measure
        ColorScale options
        'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' |
        'YIGnBu'
    Return:
        A trace object to be used on a plotly plot
    '''
    trace = Scatter(
        x=[],
        y=[],
        mode='markers',
        marker=Marker(
            showscale=True,

            colorscale=colorscale,
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=title,
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)
        )
    )
    for node in nodes:
        trace['x'].append(pos[node][0])
        trace['y'].append(pos[node][1])
        trace['marker']['color'].append(data[node])
    attrib = dict(name='', text=labels, hoverinfo='text', opacity=opacity)
    trace = dict(trace, **attrib)
    trace['marker']['size'] = size
    return trace


def scatter_edges(graph, pos, line_color='#a3a3c2', line_width=1):
    '''
    Function to create a trace to represent an edge on the plot.
    Args:
        graph (NetworkX Graph): the graph to be plotted
        pos (dict): node positions on the graph
        line_color (hex str): the color of the edge
        line_width (int): the width of the edge
    Return:
        A trace object to be used on a plotly plot
    '''
    trace = Scatter(
        x=[],
        y=[],
        mode='lines',
    )
    for edge in graph.edges():
        trace['x'] += [pos[edge[0]][0], pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1], pos[edge[1]][1], None]
        trace['hoverinfo'] = 'none'
        trace['line']['width'] = line_width
        if line_color is not None:
            trace['line']['color'] = line_color
    return trace


def plot_ly(subgraph, title, data, measure, colorscale='Hot'):
    '''
    Function to get a plotly figure object to be plotted
    Args:
        subgraph (NetworkX Graph): the graph to be plotted
        title (str): the title for the plot
        data (dict): the measured data to be plotted
        measure (str): the measure being plotted
        colorscale (str): colorscale for the data measure
        ColorScale options
        'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' |
        'YIGnBu'
    '''
    pos = nx.spring_layout(subgraph, k=.12)
    nodes = list(subgraph.node.keys())
    nodes.sort()
    labels = []
    for node in subgraph.nodes():
        author_name = subgraph.node[node]['data']['author']['name'].title()
        label = "{}<br>{} = {}".format(author_name, measure, str(data[node]))
        labels.append(label)
    trace1 = scatter_edges(subgraph, pos)
    trace2 = scatter_nodes(pos=pos, labels=labels,
                           title=title, data=data,
                           nodes=nodes, colorscale=colorscale)
    width = 800
    height = 600
    axis = dict(
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title=''
    )
    layout = Layout(
        title=title,
        font=Font(),
        showlegend=False,
        autosize=False,
        width=width,
        height=height,
        xaxis=dict(
            title='',
            titlefont=dict(
                size=14,
                color='#7f7f7f'
            ),
            showline=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=YAxis(axis),
        margin=Margin(
            l=40,
            r=40,
            b=85,
            t=100,
            pad=0,

        ),
        hovermode='closest',
        plot_bgcolor='#EFECEA'
    )
    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)
    return fig
