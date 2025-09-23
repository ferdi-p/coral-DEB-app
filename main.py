## nicegui_app.py
from __future__ import annotations
import io, base64
import matplotlib.pyplot as plt
from nicegui import ui

from parameters import default_params, drivers_from_params
from plotting import plot_panel

def fig_to_data_uri(fig) -> str:
    """Render a Matplotlib figure to a PNG data URI for NiceGUI image."""
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('ascii')
    plt.close(fig)  # free memory
    return f'data:image/png;base64,{b64}'

# --- initial state ---
params = default_params()
drivers = drivers_from_params(params)

# --- sidebar controls (auto-run on release/commit via 'change') ---
with ui.left_drawer().props('bordered'):
    ui.label('Simulation')
    tmax_slider = ui.slider(min=30, max=1460, value=int(params['tmax']), step=5) \
                  .props('label="tmax (days)"')
    spd_slider  = ui.slider(min=5, max=200, value=int(params['steps_per_day']), step=5) \
                  .props('label="steps/day"')

    ui.separator()
    ui.label('Initial conditions (y0)')
    s0   = ui.number(value=float(params['y0'][0]), format='%.6g').props('label="S0"')
    h0   = ui.number(value=float(params['y0'][1]), format='%.6g').props('label="H0"')
    jcp0 = ui.number(value=float(params['y0'][2]), format='%.6g').props('label="jCP0"')
    jsg0 = ui.number(value=float(params['y0'][3]), format='%.6g').props('label="jSG0"')

    ui.separator()
    ui.label('Annual cycles (period 365 d)')
    # Light
    L_mean  = ui.number(value=float(params['L_mean'])).props('label="L mean"')
    L_amp   = ui.number(value=float(params['L_amp'])).props('label="L amplitude (±)"')
    L_phase = ui.number(value=float(params['L_phase'])).props('label="L peak day (0–365)"')
    # Temperature
    T_mean  = ui.number(value=float(params['T_mean'])).props('label="T mean (°C)"')
    T_amp   = ui.number(value=float(params['T_amp'])).props('label="T amplitude (±°C)"')
    T_phase = ui.number(value=float(params['T_phase'])).props('label="T peak day (0–365)"')
    # DIN
    Nu_mean  = ui.number(value=float(params['Nu_mean']), format='%.6g').props('label="Nu mean (mol N L⁻¹)"')
    Nu_amp   = ui.number(value=float(params['Nu_amp']),  format='%.6g').props('label="Nu amplitude (±)"')
    Nu_phase = ui.number(value=float(params['Nu_phase'])).props('label="Nu peak day (0–365)"')
    # Prey
    X_mean  = ui.number(value=float(params['X_mean']), format='%.6g').props('label="X mean (mol C L⁻¹)"')
    X_amp   = ui.number(value=float(params['X_amp']),  format='%.6g').props('label="X amplitude (±)"')
    X_phase = ui.number(value=float(params['X_phase'])).props('label="X peak day (0–365)"')

    status = ui.label()  # feedback line

# --- figure area as an image (version-proof) ---
placeholder_fig, _ = plt.subplots()
img = ui.image(fig_to_data_uri(placeholder_fig)).style('max-width: 100%;')

def run_simulation():
    """Pull values from UI -> params, rebuild drivers, run, and update image."""
    params['tmax'] = float(tmax_slider.value)
    params['steps_per_day'] = int(spd_slider.value)
    params['y0'] = [float(s0.value), float(h0.value), float(jcp0.value), float(jsg0.value)]

    params['L_mean'], params['L_amp'], params['L_phase'] = float(L_mean.value), float(L_amp.value), float(L_phase.value)
    params['T_mean'], params['T_amp'], params['T_phase'] = float(T_mean.value), float(T_amp.value), float(T_phase.value)
    params['Nu_mean'], params['Nu_amp'], params['Nu_phase'] = float(Nu_mean.value), float(Nu_amp.value), float(Nu_phase.value)
    params['X_mean'],  params['X_amp'],  params['X_phase']  = float(X_mean.value),  float(X_amp.value),  float(X_phase.value)

    global drivers
    drivers = drivers_from_params(params)

    status.set_text('Running…')
    fig, _ = plot_panel(params, drivers=drivers, show=False)
    img.set_source(fig_to_data_uri(fig))  # swap image content
    status.set_text('Done.')

# --- hook 'change' events so it runs on release/commit (not on every tick) ---
for el in (
    tmax_slider, spd_slider,
    s0, h0, jcp0, jsg0,
    L_mean, L_amp, L_phase,
    T_mean, T_amp, T_phase,
    Nu_mean, Nu_amp, Nu_phase,
    X_mean, X_amp, X_phase,
):
    el.on('change', lambda e: run_simulation())

# initial run so you see a real plot
run_simulation()

ui.run(title='Coral Heat Stress (NiceGUI)', reload=False)

# nicegui_app.py (end of file)
import os
port = int(os.getenv('PORT', 8000))  # Render sets $PORT
ui.run(host='0.0.0.0', port=port, reload=False, title='Coral Heat Stress (NiceGUI)')