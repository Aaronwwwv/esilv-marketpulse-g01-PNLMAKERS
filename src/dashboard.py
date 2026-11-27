from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot, load_instruments


# Presentation only: no provider call and no formula in this file.
# Palette: black and gold (default MarketPulse theme).
PAPER = "#0a0908"
SHEET = "#141210"
LINE = "#2E2A20"
ACCENT = "#C9A96A"
INK = "#F0E6CC"
MUTED = "#B3A47C"  # 8.07:1 on PAPER, 7.58:1 on SHEET

CSS = """
:root {
  --paper: #0a0908;
  --sheet: #141210;
  --line: #2E2A20;
  --accent: #C9A96A;
  --ink: #F0E6CC;
  --muted: #B3A47C;
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  min-height: 100%;
  background: var(--paper);
  color: var(--ink);
  font-family: "DM Sans", system-ui, sans-serif;
}
body {
  background:
    radial-gradient(circle at 85% 0%, rgba(201, 169, 106, 0.07), transparent 42%),
    var(--paper);
  min-height: 100vh;
  overflow-x: hidden;
}
html.has-hand, html.has-hand * { cursor: none !important; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }

#sphere, #hand {
  position: fixed;
  pointer-events: none;
  z-index: 0;
}
#sphere { left: 0; top: 0; opacity: 0.7; }
#hand { left: 0; top: 0; z-index: 50; will-change: transform; }

.page {
  position: relative;
  z-index: 1;
  max-width: 1120px;
  margin: 0 auto;
  padding: 48px 16px 40px;
}
h1 {
  margin: 0 0 40px;
  font-family: "Syne", sans-serif;
  font-weight: 800;
  font-size: clamp(44px, 8vw, 96px);
  line-height: 0.95;
  letter-spacing: -0.02em;
}

/* Tilt: cards and buttons lean toward the pointer */
.tilt {
  transform: perspective(900px) rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg));
  transition: transform 0.35s cubic-bezier(0.2, 0.7, 0.2, 1);
  transform-style: preserve-3d;
}

.card {
  position: relative;
  background: var(--sheet);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 26px 26px 22px;
  box-shadow: 0 22px 44px -26px rgba(201, 169, 106, 0.35);
}
.card--hero {
  border-color: var(--accent);
  background:
    linear-gradient(135deg, rgba(201, 169, 106, 0.14), transparent 60%),
    var(--sheet);
}
.card--chart { padding: 24px 24px 14px; }

.row { display: grid; gap: 20px; margin-bottom: 20px; }
.row--top { grid-template-columns: 1fr 1fr 0.7fr; }
.row--top .card:nth-child(2) { margin-top: 34px; }
.row--hero { grid-template-columns: 1.6fr 1fr; }

.label {
  margin: 0 0 14px;
  font-family: "JetBrains Mono", monospace;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
}
.figure {
  margin: 0;
  font-family: "Syne", sans-serif;
  font-weight: 700;
  font-size: 42px;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.figure--xl {
  font-size: clamp(64px, 9vw, 116px);
  font-weight: 800;
  color: var(--accent);
}
.note {
  margin: 12px 0 0;
  font-size: 15px;
  color: var(--muted);
}
.chip {
  margin: 0;
  font-family: "Syne", sans-serif;
  font-weight: 700;
  font-size: 24px;
  line-height: 1.15;
}
.mono {
  margin: 10px 0 0;
  font-family: "JetBrains Mono", monospace;
  font-size: 12px;
  color: var(--muted);
}

/* Gauge: a conic ring, the value sets the arc */
.hero-side { display: flex; align-items: center; justify-content: center; }
.ring {
  position: relative;
  width: 170px;
  height: 170px;
  border-radius: 50%;
}
.ring::after {
  content: "";
  position: absolute;
  inset: 16px;
  border-radius: 50%;
  background: var(--sheet);
}
.ring-core {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: "JetBrains Mono", monospace;
  font-size: 12px;
  color: var(--muted);
}
.ring-core strong {
  font-family: "Syne", sans-serif;
  font-size: 26px;
  color: var(--ink);
}

/* Buttons: pressed relief, thick bottom edge */
.btns { display: flex; gap: 10px; flex-wrap: wrap; }
.btn {
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  color: var(--ink);
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 18px;
  box-shadow: 0 3px 0 #1b170f;
  cursor: pointer;
}
.btn.is-on {
  background: var(--accent);
  color: var(--paper);
  border-color: var(--accent);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.35);
  transform: translateY(2px);
}
.chart-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 6px;
}
.chart-head h2 {
  margin: 0;
  font-family: "Syne", sans-serif;
  font-weight: 700;
  font-size: 22px;
}

@media (max-width: 760px) {
  .row--top, .row--hero { grid-template-columns: 1fr; }
  .row--top .card:nth-child(2) { margin-top: 0; }
  .figure { font-size: 36px; }
  .ring { width: 130px; height: 130px; }
  .ring::after { inset: 12px; }
}
"""

JS = r"""
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var CELL = 6;
  var FRONT = '#E9D59B';   // light gold, front of the sphere
  var BACK = '#6E5424';    // dark gold, back of the sphere

  // ---- Pixel sphere ------------------------------------------------
  var sphere = document.createElement('canvas');
  sphere.id = 'sphere';
  document.body.insertBefore(sphere, document.body.firstChild);
  var sctx = sphere.getContext('2d');
  var pts = [], geo = {};

  function buildSphere() {
    var w = sphere.width = window.innerWidth;
    var h = sphere.height = window.innerHeight;
    var narrow = w <= 760;
    var R = Math.min(w, h) * (narrow ? 0.30 : 0.36);
    geo = { R: R, cx: narrow ? w * 0.5 : w * 0.78, cy: narrow ? h * 0.22 : h * 0.36 };
    pts = [];
    for (var y = -R; y <= R; y += CELL) {
      for (var x = -R; x <= R; x += CELL) {
        var d = x * x + y * y;
        if (d >= R * R) continue;
        pts.push({ nx: x / R, ny: y / R, nz: Math.sqrt(1 - d / (R * R)) });
      }
    }
  }

  function drawSphere(angle) {
    sctx.clearRect(0, 0, sphere.width, sphere.height);
    var c = Math.cos(angle), s = Math.sin(angle);
    var R = geo.R;
    var pass;
    for (pass = 0; pass < 2; pass++) {
      sctx.fillStyle = pass === 0 ? BACK : FRONT;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        var zr = -p.nx * s + p.nz * c;
        var isFront = zr > 0;
        if ((pass === 0) === isFront) continue;
        var xr = p.nx * c + p.nz * s;
        var sx = Math.round((geo.cx + xr * R) / CELL) * CELL;
        var sy = Math.round((geo.cy + p.ny * R) / CELL) * CELL;
        sctx.fillRect(sx, sy, CELL - 1, CELL - 1);
      }
    }
  }

  // ---- Pixel hand cursor -------------------------------------------
  // Blocks of 3 px. Each rect is [x, y, w, h] in blocks.
  var HAND_RECTS = [
    [4, 0, 3, 7], [3, 6, 10, 6], [7, 5, 3, 4], [10, 6, 3, 4],
    [12, 8, 2, 3], [1, 8, 3, 3], [4, 12, 7, 4]
  ];
  var BLOCK = 3;
  var sprite = document.createElement('canvas');
  sprite.width = 14; sprite.height = 16;
  var spctx = sprite.getContext('2d');
  HAND_RECTS.forEach(function (r) {
    spctx.fillStyle = '#F0E6CC';
    spctx.fillRect(r[0] - 1, r[1] - 1, r[2] + 2, r[3] + 2);
  });
  HAND_RECTS.forEach(function (r) {
    spctx.fillStyle = '#C9A96A';
    spctx.fillRect(r[0], r[1], r[2], r[3]);
  });

  var hand = document.createElement('canvas');
  hand.id = 'hand';
  hand.width = 60; hand.height = 56;
  document.body.appendChild(hand);
  var hctx = hand.getContext('2d');
  hctx.imageSmoothingEnabled = false;
  var TIP_X = 30;                 // pivot = fingertip, centred horizontally
  var TIP_LOCAL = 5.5 * BLOCK;    // fingertip position inside the sprite
  var hx = 0, hy = 0, tx = 0, ty = 0, vx = 0, seen = false, pressed = false;

  document.addEventListener('pointermove', function (e) {
    tx = e.clientX; ty = e.clientY;
    if (!seen) { hx = tx; hy = ty; seen = true; }
    if (!fine) return;
    if (!document.documentElement.classList.contains('has-hand')) {
      document.documentElement.classList.add('has-hand');
    }
  }, { passive: true });
  document.addEventListener('pointerdown', function () { pressed = true; });
  document.addEventListener('pointerup', function () { pressed = false; });
  document.addEventListener('pointerleave', function () {
    document.documentElement.classList.remove('has-hand');
    hand.style.opacity = '0';
  });
  document.addEventListener('pointerenter', function () { hand.style.opacity = '1'; });

  function drawHand(t, dt) {
    var k = 1 - Math.pow(0.0008, dt / 1000);
    var nhx = hx + (tx - hx) * k;
    vx = (nhx - hx) / Math.max(dt, 1) * 16;
    hx = nhx;
    hy = hy + (ty - hy) * k;

    var tilt = Math.max(-0.32, Math.min(0.32, -vx * 0.03));
    var sway = Math.sin(t * 0.0021) * 0.04;
    var bob = Math.sin(t * 0.0033) * 1.2;
    var scale = pressed ? 0.88 : 1;

    hctx.clearRect(0, 0, hand.width, hand.height);
    hctx.save();
    hctx.translate(TIP_X, 0);
    hctx.rotate(tilt + sway);
    hctx.scale(scale, scale);
    hctx.drawImage(sprite, -TIP_LOCAL, 0, sprite.width * BLOCK, sprite.height * BLOCK);
    hctx.restore();
    hand.style.transform = 'translate(' + (hx - TIP_X) + 'px,' + (hy + bob) + 'px)';
  }

  // ---- One animation loop ------------------------------------------
  var last = 0;
  function frame(t) {
    var dt = last ? t - last : 16;
    last = t;
    drawSphere(reduce ? 0.6 : t * 0.00035);
    if (fine && !reduce) drawHand(t, dt);
    if (!reduce) requestAnimationFrame(frame);
  }

  function start() {
    buildSphere();
    requestAnimationFrame(frame);
  }
  window.addEventListener('resize', function () {
    buildSphere();
    if (reduce) drawSphere(0.6);
  });
  if (reduce) {
    buildSphere();
    drawSphere(0.6);
    hand.remove();
  } else {
    start();
  }

  // ---- Tilt toward the pointer -------------------------------------
  var activeTilt = null;
  function resetTilt(el) {
    if (!el) return;
    el.style.setProperty('--rx', '0deg');
    el.style.setProperty('--ry', '0deg');
  }
  document.addEventListener('pointermove', function (e) {
    if (reduce || !fine) return;
    var el = e.target.closest && e.target.closest('.tilt');
    if (activeTilt && activeTilt !== el) { resetTilt(activeTilt); activeTilt = null; }
    if (!el) return;
    var r = el.getBoundingClientRect();
    var nx = (e.clientX - r.left) / r.width - 0.5;
    var ny = (e.clientY - r.top) / r.height - 0.5;
    el.style.setProperty('--ry', (nx * 10).toFixed(2) + 'deg');
    el.style.setProperty('--rx', (-ny * 8).toFixed(2) + 'deg');
    activeTilt = el;
  }, { passive: true });

  // ---- Series toggle (client side, no server round trip) -----------
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-view]');
    if (!b) return;
    var gd = document.querySelector('.js-plotly-plot');
    var view = b.getAttribute('data-view');
    if (gd && window.Plotly) {
      var vis = view === 'both' ? [true, true] : view === 'aapl' ? [true, false] : [false, true];
      window.Plotly.restyle(gd, { visible: vis });
    }
    document.querySelectorAll('[data-view]').forEach(function (x) {
      x.classList.toggle('is-on', x === b);
    });
  });
})();
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
  <head>
    {%metas%}
    <title>MarketPulse</title>
    {%favicon%}
    {%css%}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>{css}</style>
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
    <script>{js}</script>
  </body>
</html>
""".replace("{css}", CSS).replace("{js}", JS)


def pct(value):
    return f"{value:+.2f}%"


def pts(value):
    return f"{value:+.2f} pts"


def stat(label, value, note):
    return html.Div(
        [
            html.P(label, className="label"),
            html.P(value, className="figure"),
            html.P(note, className="note"),
        ],
        className="card tilt",
    )


def ring(relative_performance):
    # Presentation scale: -10 to +10 points maps to 0 to 360 degrees.
    fraction = min(max((relative_performance + 10) / 20, 0), 1)
    degrees = round(fraction * 360, 2)
    background = (
        f"conic-gradient({ACCENT} 0deg, {ACCENT} {degrees}deg, "
        f"{LINE} {degrees}deg, {LINE} 360deg)"
    )
    return html.Div(
        html.Div(
            [html.Span("écart"), html.Strong(f"{relative_performance:+.1f}")],
            className="ring-core",
        ),
        className="ring tilt",
        style={"background": background},
    )


def build_figure(snapshot):
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    figure = go.Figure()
    figure.add_hline(y=100, line=dict(color=LINE, dash="dot", width=1))

    figure.add_trace(go.Scatter(
        x=[row["date"] for row in snapshot["instrument_base_100"]],
        y=[row["value"] for row in snapshot["instrument_base_100"]],
        mode="lines",
        name=instrument["ticker"],
        line=dict(color=ACCENT, width=3),
        hovertemplate="%{y:.2f}<extra>" + instrument["ticker"] + "</extra>",
    ))

    figure.add_trace(go.Scatter(
        x=[row["date"] for row in snapshot["benchmark_base_100"]],
        y=[row["value"] for row in snapshot["benchmark_base_100"]],
        mode="lines",
        name=benchmark["ticker"],
        line=dict(color=INK, width=1.8),
        opacity=0.7,
        hovertemplate="%{y:.2f}<extra>" + benchmark["ticker"] + "</extra>",
    ))

    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, monospace", color=MUTED, size=12),
        margin=dict(l=56, r=24, t=44, b=48),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color=INK),
        ),
        xaxis=dict(gridcolor=LINE, linecolor=LINE, zeroline=False),
        yaxis=dict(
            gridcolor=LINE,
            linecolor=LINE,
            zeroline=False,
            title=dict(text="Base 100"),
        ),
    )
    return figure


def build_layout(snapshot):
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    return html.Main(
        [
            html.H1("MarketPulse"),
            html.Section(
                [
                    stat(
                        "Instrument",
                        pct(snapshot["instrument_return"]),
                        f"{instrument['ticker']} - {instrument['name']}",
                    ),
                    stat(
                        "Benchmark",
                        pct(snapshot["benchmark_return"]),
                        f"{benchmark['ticker']} - {benchmark['name']}",
                    ),
                    html.Div(
                        [
                            html.P("Fournisseur", className="label"),
                            html.P(snapshot["provider"], className="chip"),
                            html.P(snapshot["access_mode"], className="mono"),
                        ],
                        className="card tilt",
                    ),
                ],
                className="row row--top",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.P("Performance relative", className="label"),
                            html.P(
                                pts(snapshot["relative_performance"]),
                                className="figure figure--xl",
                            ),
                            html.P(
                                f"{instrument['ticker']} moins {benchmark['ticker']}",
                                className="note",
                            ),
                        ],
                        className="card card--hero tilt",
                    ),
                    html.Div(
                        ring(snapshot["relative_performance"]),
                        className="card hero-side",
                    ),
                ],
                className="row row--hero",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.H2("Base 100"),
                            html.Div(
                                [
                                    html.Button(
                                        "Les deux",
                                        className="btn tilt is-on",
                                        **{"data-view": "both"},
                                    ),
                                    html.Button(
                                        instrument["ticker"],
                                        className="btn tilt",
                                        **{"data-view": "aapl"},
                                    ),
                                    html.Button(
                                        benchmark["ticker"],
                                        className="btn tilt",
                                        **{"data-view": "sp500"},
                                    ),
                                ],
                                className="btns",
                            ),
                        ],
                        className="chart-head",
                    ),
                    dcc.Graph(
                        figure=build_figure(snapshot),
                        config={"displayModeBar": False},
                    ),
                ],
                className="card card--chart",
            ),
        ],
        className="page",
    )


snapshot = build_market_snapshot(load_instruments())

app = Dash(__name__, title="MarketPulse")
app.index_string = INDEX_TEMPLATE
app.layout = build_layout(snapshot)


if __name__ == "__main__":
    app.run(debug=False)