/* Dark-only, GitHub Pages-friendly JS:
   - responsive top nav (open/close)
   - active section highlight on scroll
   - subtle polygon network + bubble background animation (concept copied, implementation rewritten)
*/

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

// Footer year
(() => {
  const y = $("#year");
  if (y) y.textContent = String(new Date().getFullYear());
})();

// Responsive nav
(() => {
  const toggle = $("#navToggle");
  const nav = $("#nav");
  if (!toggle || !nav) return;

  const setOpen = (open) => {
    nav.classList.toggle("isOpen", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  toggle.addEventListener("click", () => setOpen(!nav.classList.contains("isOpen")));

  // Close after click on small screens
  nav.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a) return;
    setOpen(false);
  });

  // Close on escape
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
})();

// Active section highlight
(() => {
  const links = $$(".nav__link");
  if (!links.length) return;

  const byHash = new Map(links.map((a) => [a.getAttribute("href"), a]));
  const sections = $$("section.section[id]");
  if (!sections.length) return;

  const setActive = (id) => {
    links.forEach((a) => a.classList.toggle("isActive", a.getAttribute("href") === `#${id}`));
  };

  const obs = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => (b.intersectionRatio ?? 0) - (a.intersectionRatio ?? 0))[0];
      if (!visible) return;
      setActive(visible.target.id);
    },
    { root: null, threshold: [0.18, 0.28, 0.38, 0.5] },
  );

  sections.forEach((s) => obs.observe(s));

  // initial state (hash)
  const hash = window.location.hash;
  if (hash && byHash.has(hash)) setActive(hash.slice(1));
})();

// Background animation: polygon network
(() => {
  const canvas = $("#bgPolygons");
  if (!canvas) return;

  const ctx = canvas.getContext("2d", { alpha: true });
  const DPR = Math.max(1, Math.min(2, window.devicePixelRatio || 1));

  const state = {
    w: 0,
    h: 0,
    pts: [],
    lastT: performance.now(),
  };

  const resize = () => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    state.w = w;
    state.h = h;
    canvas.width = Math.floor(w * DPR);
    canvas.height = Math.floor(h * DPR);
    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);

    const targetCount = Math.max(55, Math.min(95, Math.floor((w * h) / 22000)));
    state.pts = Array.from({ length: targetCount }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: 1 + Math.random() * 2.4,
    }));
  };

  const clampWrap = (p) => {
    if (p.x < -20) p.x = state.w + 20;
    if (p.x > state.w + 20) p.x = -20;
    if (p.y < -20) p.y = state.h + 20;
    if (p.y > state.h + 20) p.y = -20;
  };

  const draw = (t) => {
    const dt = Math.min(32, t - state.lastT);
    state.lastT = t;
    ctx.clearRect(0, 0, state.w, state.h);

    // Update
    for (const p of state.pts) {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      clampWrap(p);
    }

    // Lines
    const maxDist = 140;
    for (let i = 0; i < state.pts.length; i++) {
      const a = state.pts[i];
      for (let j = i + 1; j < state.pts.length; j++) {
        const b = state.pts[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const d2 = dx * dx + dy * dy;
        if (d2 > maxDist * maxDist) continue;
        const d = Math.sqrt(d2);
        const alpha = Math.max(0, 1 - d / maxDist) * 0.35;
        ctx.strokeStyle = `rgba(125, 240, 234, ${alpha})`;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }

    // Points
    for (const p of state.pts) {
      ctx.fillStyle = "rgba(160, 235, 235, 0.55)";
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(draw);
  };

  resize();
  window.addEventListener("resize", resize);

  // Reduce motion: draw one frame only
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    requestAnimationFrame((t) => {
      state.lastT = t;
      draw(t);
    });
    return;
  }

  requestAnimationFrame(draw);
})();

// Background animation: bubbles (subtle)
(() => {
  const canvas = $("#bgBubbles");
  if (!canvas) return;
  const ctx = canvas.getContext("2d", { alpha: true });
  const DPR = Math.max(1, Math.min(2, window.devicePixelRatio || 1));

  const state = { w: 0, h: 0, bubbles: [] };

  const resize = () => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    state.w = w;
    state.h = h;
    canvas.width = Math.floor(w * DPR);
    canvas.height = Math.floor(h * DPR);
    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);

    const n = Math.max(24, Math.min(60, Math.floor(w / 30)));
    state.bubbles = Array.from({ length: n }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 1.8 + Math.random() * 7.2,
      vy: 0.10 + Math.random() * 0.28,
      drift: (Math.random() - 0.5) * 0.12,
      a: 0.025 + Math.random() * 0.045,
    }));
  };

  const step = () => {
    ctx.clearRect(0, 0, state.w, state.h);
    for (const b of state.bubbles) {
      ctx.fillStyle = `rgba(125, 240, 234, ${b.a})`;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.fill();
      b.y -= b.vy;
      b.x += b.drift;
      if (b.y < -10) {
        b.y = state.h + 10;
        b.x = Math.random() * state.w;
      }
      if (b.x < -10) b.x = state.w + 10;
      if (b.x > state.w + 10) b.x = -10;
    }
    requestAnimationFrame(step);
  };

  resize();
  window.addEventListener("resize", resize);

  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    step();
    return;
  }

  requestAnimationFrame(step);
})();


