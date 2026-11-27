/* Tyr Capital: hero particle wave and glass pointer highlight.
   Plain WebGL, no library. The wave only animates while the hero is on
   screen, and draws a single still frame when reduced motion is requested. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Pointer highlight on glass surfaces ---- */
  if (window.matchMedia('(hover: hover)').matches) {
    var target = null, px = 0, py = 0, queued = false;
    document.addEventListener('pointermove', function (e) {
      var el = e.target.closest ? e.target.closest('.glass, .guide') : null;
      if (!el) return;
      target = el; px = e.clientX; py = e.clientY;
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        var r = target.getBoundingClientRect();
        target.style.setProperty('--mx', (px - r.left) + 'px');
        target.style.setProperty('--my', (py - r.top) + 'px');
      });
    }, { passive: true });
  }

  /* ---- Hero wave ---- */
  var canvas = document.getElementById('heroWave');
  if (!canvas) return;

  function useStill() { canvas.classList.add('is-static'); }

  var gl = null;
  try {
    gl = canvas.getContext('webgl', { alpha: true, antialias: false, premultipliedAlpha: true, depth: false, stencil: false });
  } catch (err) { gl = null; }
  if (!gl) { useStill(); return; }

  var VERT = [
    'attribute vec2 p;',
    'attribute float s;',
    'uniform float t;',
    'uniform float aspect;',
    'uniform float dpr;',
    'uniform float intro;',
    'uniform vec2 par;',
    'varying float vA;',
    'varying float vH;',
    'varying float vS;',
    'void main() {',
    '  vec3 w;',
    '  float base = 1.0;',
    '  if (s < 0.0) {',
    '    float x = p.x * 12.0;',
    '    float z = p.y * 14.0 + 0.4;',
    '    float y = sin(x * 0.42 + t * 0.42) * 0.78',
    '            + sin(z * 0.6 - t * 0.36 + x * 0.22) * 0.6',
    '            + sin(x * 0.9 + z * 1.3 + t * 0.66) * 0.16;',
    '    float swell = exp(-pow((x - 2.2) * 0.3, 2.0));',
    '    y += swell * sin(z * 0.85 - t * 0.5) * 0.6;',
    '    y *= intro;',
    '    w = vec3(x, y, z);',
    '    vH = y;',
    '    base = smoothstep(1.0, 0.82, abs(p.x));',
    '  } else {',
    '    float x = p.x * 12.0 + sin(t * 0.11 + s * 40.0) * 0.6;',
    '    float z = p.y * 14.0 + 0.4;',
    '    float y = 1.0 + s * 4.2 + sin(t * 0.17 + s * 90.0) * 0.35;',
    '    w = vec3(x, y, z);',
    '    vH = 0.35;',
    '    base = 0.35 + 0.3 * sin(t * 0.9 + s * 200.0);',
    '  }',
    '  vec3 c = w - vec3(par.x * 0.7, 2.0 + par.y * 0.25, -3.2);',
    '  float cs = cos(0.2);',
    '  float sn = sin(0.2);',
    '  vec3 v = vec3(c.x, c.y * cs + c.z * sn, -c.y * sn + c.z * cs);',
    '  float d = max(v.z, 0.001);',
    '  gl_Position = vec4(v.x * 1.55 / aspect, v.y * 1.55 + 0.1 * d, 0.0, v.z);',
    '  float near = clamp((6.5 - d) / 6.5, 0.0, 1.0);',
    '  float size = dpr * (24.0 / d) * (1.0 + near * near * 3.2);',
    '  gl_PointSize = max(size, 1.7 * dpr);',
    '  float ny = gl_Position.y / d;',
    '  vA = base * intro',
    '     * (1.0 / (1.0 + near * near * 5.0))',
    '     * smoothstep(17.0, 9.0, d)',
    '     * smoothstep(-1.0, -0.72, ny);',
    '  vS = near;',
    '}'
  ].join('\n');

  var FRAG = [
    'precision mediump float;',
    'varying float vA;',
    'varying float vH;',
    'varying float vS;',
    'void main() {',
    '  float r = length(gl_PointCoord - 0.5) * 2.0;',
    '  float a = (1.0 - smoothstep(mix(0.5, 0.0, vS), 1.0, r)) * vA;',
    '  vec3 gold = mix(vec3(0.66, 0.52, 0.26), vec3(1.0, 0.93, 0.74), smoothstep(-0.3, 1.1, vH));',
    '  gl_FragColor = vec4(gold * a, a);',
    '}'
  ].join('\n');

  function compile(type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    return gl.getShaderParameter(sh, gl.COMPILE_STATUS) ? sh : null;
  }

  var vs = compile(gl.VERTEX_SHADER, VERT);
  var fs = compile(gl.FRAGMENT_SHADER, FRAG);
  if (!vs || !fs) { useStill(); return; }
  var prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { useStill(); return; }
  gl.useProgram(prog);

  // Point cloud: a grid for the wave surface plus loose dust above it.
  var small = window.innerWidth < 760;
  var cols = small ? 110 : 210;
  var rows = small ? 54 : 84;
  var dust = small ? 120 : 320;
  var count = cols * rows + dust;
  var data = new Float32Array(count * 3);
  var i = 0, cx, rz;
  for (rz = 0; rz < rows; rz++) {
    for (cx = 0; cx < cols; cx++) {
      data[i++] = (cx / (cols - 1)) * 2 - 1;
      data[i++] = rz / (rows - 1);
      data[i++] = -1;
    }
  }
  for (var k = 0; k < dust; k++) {
    data[i++] = Math.random() * 2 - 1;
    data[i++] = Math.random();
    data[i++] = Math.random() * 0.999 + 0.001;
  }

  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
  var aP = gl.getAttribLocation(prog, 'p');
  var aS = gl.getAttribLocation(prog, 's');
  gl.enableVertexAttribArray(aP);
  gl.vertexAttribPointer(aP, 2, gl.FLOAT, false, 12, 0);
  gl.enableVertexAttribArray(aS);
  gl.vertexAttribPointer(aS, 1, gl.FLOAT, false, 12, 8);

  var uT = gl.getUniformLocation(prog, 't');
  var uAspect = gl.getUniformLocation(prog, 'aspect');
  var uDpr = gl.getUniformLocation(prog, 'dpr');
  var uIntro = gl.getUniformLocation(prog, 'intro');
  var uPar = gl.getUniformLocation(prog, 'par');

  gl.disable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE);
  gl.clearColor(0, 0, 0, 0);

  var dpr = 1, time = 14, intro = reduceMotion ? 1 : 0;
  var parX = 0, parY = 0, aimX = 0, aimY = 0;
  var running = false, onScreen = false, raf = 0, last = 0;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 1.75);
    var w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    gl.viewport(0, 0, w, h);
    gl.uniform1f(uAspect, w / h);
    gl.uniform1f(uDpr, dpr);
    if (!running) draw();
  }

  function draw() {
    var e = 1 - Math.pow(1 - intro, 3);
    gl.uniform1f(uT, time);
    gl.uniform1f(uIntro, e);
    gl.uniform2f(uPar, parX, parY);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.POINTS, 0, count);
  }

  function frame(now) {
    raf = 0;
    if (!running) return;
    var dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    time += dt;
    if (intro < 1) intro = Math.min(1, intro + dt / 1.8);
    parX += (aimX - parX) * 0.04;
    parY += (aimY - parY) * 0.04;
    draw();
    raf = requestAnimationFrame(frame);
  }

  function start() {
    if (running || reduceMotion || !onScreen || document.hidden) return;
    running = true;
    last = performance.now();
    raf = requestAnimationFrame(frame);
  }

  function stop() {
    running = false;
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
  }

  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
  else window.addEventListener('resize', resize);
  resize();

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      onScreen = entries[entries.length - 1].isIntersecting;
      if (onScreen) start(); else stop();
    }).observe(canvas);
  } else {
    onScreen = true;
    start();
  }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop(); else start();
  });

  canvas.addEventListener('webglcontextlost', function (e) {
    e.preventDefault();
    stop();
    useStill();
  });

  if (!reduceMotion && window.matchMedia('(hover: hover)').matches) {
    window.addEventListener('pointermove', function (e) {
      aimX = (e.clientX / window.innerWidth) * 2 - 1;
      aimY = (e.clientY / window.innerHeight) * 2 - 1;
    }, { passive: true });
  }
})();
