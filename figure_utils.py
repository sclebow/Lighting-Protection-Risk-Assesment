import plotly.graph_objects as go
import numpy as np

def create_building_collection_figure(l, w, h, metric=True):
    """Create a 3D figure of a building and its collection area.
    Args:
        l (float): Length of the building.
        w (float): Width of the building.
        h (float): Height of the building.
        metric (bool): If True, use metric units; otherwise, use imperial units.
    Returns:
        plotly.graph_objects.Figure: A 3D figure of the building and collection area.
    """
    # Convert units if necessary, assume input is in feet
    if metric:
        l = l * 0.3048  # Convert feet to meters
        w = w * 0.3048  # Convert feet to meters
        h = h * 0.3048  # Convert feet to meters

    # Center the building's base on the origin
    x_offset = -l / 2
    y_offset = -w / 2
    bx = [0 + x_offset, l + x_offset, l + x_offset, 0 + x_offset, 0 + x_offset, l + x_offset, l + x_offset, 0 + x_offset]
    by = [0 + y_offset, 0 + y_offset, w + y_offset, w + y_offset, 0 + y_offset, 0 + y_offset, w + y_offset, w + y_offset]
    bz = [0, 0, 0, 0, h, h, h, h]
    building_edges = [
        [0,1],[1,2],[2,3],[3,0], # bottom
        [4,5],[5,6],[6,7],[7,4], # top
        [0,4],[1,5],[2,6],[3,7]  # sides
    ]
    building_lines = []
    for idx, edge in enumerate(building_edges):
        building_lines.append(go.Scatter3d(
            x=[bx[edge[0]], bx[edge[1]]],
            y=[by[edge[0]], by[edge[1]]],
            z=[bz[edge[0]], bz[edge[1]]],
            mode='lines',
            line=dict(color='blue', width=5),
            showlegend=(idx == 0),
            name='Building',
            legendgroup='Building'
        ))
    buffer = 3 * h
    ca_lines = []
    ca_lines.append(go.Scatter3d(
        x=[x_offset, l + x_offset],
        y=[y_offset - buffer, y_offset - buffer],
        z=[0, 0],
        mode='lines',
        line=dict(color='red', width=4),
        name='Collection Area',
        showlegend=True
    ))
    ca_lines.append(go.Scatter3d(
        x=[x_offset, l + x_offset],
        y=[w + y_offset + buffer, w + y_offset + buffer],
        z=[0, 0],
        mode='lines',
        line=dict(color='red', width=4),
        name='Collection Area',
        showlegend=False
    ))
    ca_lines.append(go.Scatter3d(
        x=[x_offset - buffer, x_offset - buffer],
        y=[y_offset, w + y_offset],
        z=[0, 0],
        mode='lines',
        line=dict(color='red', width=4),
        name='Collection Area',
        showlegend=False
    ))
    ca_lines.append(go.Scatter3d(
        x=[l + x_offset + buffer, l + x_offset + buffer],
        y=[y_offset, w + y_offset],
        z=[0, 0],
        mode='lines',
        line=dict(color='red', width=4),
        name='Collection Area',
        showlegend=False
    ))
    ca_arcs = []
    arc_points = 30
    # Curve 1: bottom left
    arc_start = ca_lines[0].x[0], ca_lines[0].y[0]
    arc_end = ca_lines[2].x[0], ca_lines[2].y[0]
    arc_center = (arc_start[0], arc_end[1])
    arc_radius = abs(arc_center[1] - arc_start[1])
    arc_theta = np.linspace(-np.pi, -np.pi/2, arc_points)
    arc_x = arc_center[0] + arc_radius * np.cos(arc_theta)
    arc_y = arc_center[1] + arc_radius * np.sin(arc_theta)
    arc_z = np.zeros_like(arc_x)
    ca_arcs.append(go.Scatter3d(
        x=arc_x, y=arc_y, z=arc_z, mode='lines',
        line=dict(color='red', width=4, dash='dot'),
        name='Collection Area', showlegend=False))
    # Curve 2: bottom right
    arc_start = ca_lines[0].x[1], ca_lines[0].y[1]
    arc_end = ca_lines[3].x[0], ca_lines[3].y[0]
    arc_center = (arc_start[0], arc_end[1])
    arc_radius = abs(arc_center[1] - arc_start[1])
    arc_theta = np.linspace(-np.pi/2, 0, arc_points)
    arc_x = arc_center[0] + arc_radius * np.cos(arc_theta)
    arc_y = arc_center[1] + arc_radius * np.sin(arc_theta)
    arc_z = np.zeros_like(arc_x)
    ca_arcs.append(go.Scatter3d(
        x=arc_x, y=arc_y, z=arc_z, mode='lines',
        line=dict(color='red', width=4, dash='dot'),
        name='Collection Area', showlegend=False))
    # Curve 3: top right
    arc_start = ca_lines[1].x[1], ca_lines[1].y[1]
    arc_end = ca_lines[3].x[1], ca_lines[3].y[1]
    arc_center = (arc_start[0], arc_end[1])
    arc_radius = abs(arc_center[1] - arc_start[1])
    arc_theta = np.linspace(0, np.pi/2, arc_points)
    arc_x = arc_center[0] + arc_radius * np.cos(arc_theta)
    arc_y = arc_center[1] + arc_radius * np.sin(arc_theta)
    arc_z = np.zeros_like(arc_x)
    ca_arcs.append(go.Scatter3d(
        x=arc_x, y=arc_y, z=arc_z, mode='lines',
        line=dict(color='red', width=4, dash='dot'),
        name='Collection Area', showlegend=False))
    # Curve 4: top left
    arc_start = ca_lines[1].x[0], ca_lines[1].y[0]
    arc_end = ca_lines[2].x[1], ca_lines[2].y[1]
    arc_center = (arc_start[0], arc_end[1])
    arc_radius = abs(arc_center[1] - arc_start[1])
    arc_theta = np.linspace(np.pi/2, np.pi, arc_points)
    arc_x = arc_center[0] + arc_radius * np.cos(arc_theta)
    arc_y = arc_center[1] + arc_radius * np.sin(arc_theta)
    arc_z = np.zeros_like(arc_x)
    ca_arcs.append(go.Scatter3d(
        x=arc_x, y=arc_y, z=arc_z, mode='lines',
        line=dict(color='red', width=4, dash='dot'),
        name='Collection Area', showlegend=False))
    ca_lines.extend(ca_arcs)
    fig = go.Figure(data=building_lines + ca_lines)
    ca_x_min = min(x_offset - buffer, x_offset)
    ca_x_max = max(l + x_offset + buffer, l + x_offset)
    ca_y_min = min(y_offset - buffer, y_offset)
    ca_y_max = max(w + y_offset + buffer, w + y_offset)
    
    if metric:
        xaxis_title = 'Length (m)'
        yaxis_title = 'Width (m)'
        zaxis_title = 'Height (m)'
    else:
        xaxis_title = 'Length (ft)'
        yaxis_title = 'Width (ft)'
        zaxis_title = 'Height (ft)'
        
    fig.update_layout(
        scene=dict(
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            zaxis_title=zaxis_title,
            xaxis=dict(range=[ca_x_min, ca_x_max]),
            yaxis=dict(range=[ca_y_min, ca_y_max]),
            zaxis=dict(range=[0, h*2]),
        ),
        title='Interactive 3D Model: Building and Collection Area',
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig
