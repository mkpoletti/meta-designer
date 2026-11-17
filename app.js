/* Meta Designer · interações 2D e scroll */
(() => {
  const S = window.SITE || {};
  const reduzir = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const movel = () => innerWidth <= 760;
  const toque = matchMedia("(hover: none)").matches;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const lim = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;

  // estado partilhado com o céu 3D (ceu.js)
  const MD = (window.MD = { hero: 0, ceu: 0, total: 0, rato: { x: 0, y: 0 }, inicio: 0, reduzir, velocidade: 0 });

  /* ── Preloader: no máximo 0,8 s ───────────────────────────── */
  const t0 = performance.now();
  const abrir = () => {
    if (document.documentElement.classList.contains("carregado")) return;
    document.documentElement.classList.add("carregado");
    MD.inicio = performance.now();
    $$(".hero .linhas").forEach((el) => setTimeout(() => el.classList.add("visto"), reduzir ? 0 : 150));
    mostrarCookies();
  };
  addEventListener("load", () => setTimeout(abrir, Math.max(0, 250 - (performance.now() - t0))));
  setTimeout(abrir, 800);

  /* ── Céu 3D: só carrega depois da página estar pronta (não atrasa o 1.º ecrã) ── */
  let ceuPedido = false;
  const carregarCeu = () => {
    if (ceuPedido) return; ceuPedido = true;
    import("./ceu.js?v=20261116b").catch(() => document.documentElement.classList.add("sem-webgl"));
  };
  const ocioso = window.requestIdleCallback || ((fn) => setTimeout(fn, 200));
  // desktop: assim que o browser fica livre · telemóvel: no 1.º toque/rolagem (ou ao fim de 3,5 s)
  addEventListener("load", () => (movel() ? setTimeout(carregarCeu, 3500) : ocioso(carregarCeu, { timeout: 2500 })));
  ["pointerdown", "touchstart", "wheel", "keydown", "scroll"].forEach((ev) => addEventListener(ev, carregarCeu, { once: true, passive: true }));

  /* ── Smooth scroll (Lenis) + ScrollTrigger ────────────────── */
  let lenis = null;
  if (!reduzir && window.Lenis) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (window.gsap) {
      gsap.registerPlugin(ScrollTrigger);
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add((t) => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }
  const irPara = (alvo) => {
    const el = typeof alvo === "string" ? $(alvo) : alvo;
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: 0, duration: 1.4, easing: (t) => (t < 0.5 ? 16 * t ** 5 : 1 - (-2 * t + 2) ** 5 / 2) });
    else el.scrollIntoView({ behavior: reduzir ? "auto" : "smooth" });
  };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.hasAttribute("data-whats")) return;
    const id = a.getAttribute("href");
    if (id.length < 2) return;
    e.preventDefault();
    fecharMenu();
    irPara(id);
  });

  /* ── Navegação ────────────────────────────────────────────── */
  const nav = $(".nav");
  const ham = $(".nav-hamburguer");
  const menu = $("#menu-movel");
  function fecharMenu() {
    if (!menu || menu.hidden) return;
    menu.classList.remove("aberto");
    ham.setAttribute("aria-expanded", "false");
    ham.setAttribute("aria-label", "Abrir menu");
    lenis && lenis.start();
    setTimeout(() => (menu.hidden = true), 300);
  }
  ham && ham.addEventListener("click", () => {
    if (!menu.hidden) return fecharMenu();
    menu.hidden = false;
    requestAnimationFrame(() => menu.classList.add("aberto"));
    ham.setAttribute("aria-expanded", "true");
    ham.setAttribute("aria-label", "Fechar menu");
    lenis && lenis.stop();
  });
  addEventListener("keydown", (e) => { if (e.key === "Escape") fecharMenu(); });

  /* ── Rato ─────────────────────────────────────────────────── */
  addEventListener("pointermove", (e) => {
    MD.rato.x = (e.clientX / innerWidth) * 2 - 1;
    MD.rato.y = (e.clientY / innerHeight) * 2 - 1;
  }, { passive: true });

  /* ── Revelar ao entrar no ecrã ────────────────────────────── */
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("visto"); io.unobserve(e.target); }
  }), { threshold: 0.3 });
  $$(".linhas:not(.hero .linhas), .bento, .faq-lista").forEach((el) => io.observe(el));
  new IntersectionObserver(([e]) => { if (e.isIntersecting) e.target.classList.add("visto"); }, { threshold: 0.35 }).observe($(".chamada"));
  $$(".bento-cartao").forEach((el, i) => el.style.setProperty("--i", i));
  $$(".faq-item").forEach((el, i) => el.style.setProperty("--i", i));

  /* ── Pilares: texto a escrever (pílula e pesquisa) ───────── */
  const escrever = (el, frases, { vel = 45, pausa = 1800 } = {}) => {
    if (!el) return;
    if (reduzir) { el.textContent = frases[0]; return; }
    let f = 0, c = 0, apagar = false;
    const passo = () => {
      const fr = frases[f];
      c += apagar ? -1 : 1;
      el.textContent = fr.slice(0, c);
      let t = apagar ? vel / 2 : vel;
      if (!apagar && c >= fr.length) { apagar = true; t = pausa; }
      else if (apagar && c <= 0) { apagar = false; f = (f + 1) % frases.length; t = 400; }
      setTimeout(passo, t);
    };
    passo();
  };
  escrever($(".pp-texto"), ["Quanto tempo demora o meu site?", "Vou aparecer no Google?", "E no ChatGPT?", "Funciona bem no telemóvel?"], { pausa: 2000 });
  escrever($(".pv-busca-txt"), ["dentista em lisboa", "fisioterapia lisboa", "advogado cascais"], { vel: 70, pausa: 5200 });

  /* ── Galeria em cilindro ──────────────────────────────────── */
  const cil = $(".cilindro"), anel = $(".cilindro-anel");
  const cartoes = $$(".cartao-projeto");
  let rotArrasto = 0, rotEntrada = 1, galeriaVista = false;
  const G = { R: 1700, passo: 0, w: 440 };
  const medirGaleria = () => {
    G.w = Math.round(lim(Math.min(innerWidth * 0.36, (innerHeight * 0.4 - 26) / 0.625), 320, 620));
    G.R = G.w * 3.6;
    G.passo = (G.w + 56) / G.R;
    anel.style.setProperty("--cw", G.w + "px");
    cartoes.forEach((c) => c.style.setProperty("--cw", G.w + "px"));
  };
  medirGaleria();
  addEventListener("resize", medirGaleria);
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting && !galeriaVista) {
      galeriaVista = true;
      if (window.gsap && !reduzir) gsap.fromTo(G, { ent: 1 }, { ent: 0, duration: 1.6, ease: "power3.out", onUpdate: () => (rotEntrada = G.ent) });
      else rotEntrada = 0;
    }
  }, { threshold: 0.2 }).observe(cil);
  if (!galeriaVista) rotEntrada = reduzir ? 0 : 1;
  // arrastar
  let arr = null;
  cil.addEventListener("pointerdown", (e) => { if (movel()) return; arr = { x: e.clientX, r: rotArrasto }; cil.classList.add("arrastando"); cil.setPointerCapture(e.pointerId); });
  cil.addEventListener("pointermove", (e) => { if (arr) rotArrasto = arr.r - (e.clientX - arr.x) / G.R * 1.6; });
  const soltar = () => { arr = null; cil.classList.remove("arrastando"); };
  cil.addEventListener("pointerup", soltar);
  cil.addEventListener("pointercancel", soltar);
  // inclinação 3D no hover
  const inclinar = (el, alvo, max) => {
    if (toque) return;
    el.addEventListener("pointermove", (e) => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      alvo.style.transform = `perspective(900px) rotateX(${((0.5 - y) * max * 2).toFixed(2)}deg) rotateY(${((x - 0.5) * max * 2).toFixed(2)}deg)`;
      el.style.setProperty("--mx", x * 100 + "%");
      el.style.setProperty("--my", y * 100 + "%");
    });
    el.addEventListener("pointerleave", () => (alvo.style.transform = ""));
  };
  cartoes.forEach((c) => inclinar(c, c.querySelector("figure"), 8));
  $$(".bento-cartao").forEach((c) => inclinar(c, c, 8));

  // portfólio completo + visualizador de cada projeto
  const dlg = $(".portfolio");
  const grelha = $(".portfolio-grelha");
  const vis = $(".projeto-vis");
  const longos = {}; (S.telas || []).forEach((t) => { if (t.longo) longos[t.nome] = t.img; });
  const projetos = cartoes.map((c) => {
    const img = c.querySelector("img"), cap = c.querySelector("figcaption");
    const nome = cap.querySelector("strong").textContent;
    return { nome, setor: cap.querySelector("span").textContent, src: img.getAttribute("src"), alt: img.alt, longo: longos[nome], link: c.dataset.link };
  });
  const barra = '<span class="tela-pc-barra" aria-hidden="true"><i></i><i></i><i></i></span>';
  // projetos com "link" abrem o site publicado numa página nova; os outros abrem o visualizador
  grelha.innerHTML = projetos.map((p, i) => {
    const miolo = `<span class="tela-pc">${barra}<img src="${p.src}" alt="${p.alt}" width="1000" height="625" loading="lazy"></span>
      <span class="num">${String(i + 1).padStart(2, "0")}</span><span class="titulo">${p.nome}</span><span class="setor">${p.setor}</span>`;
    return p.link
      ? `<li style="--i:${i}"><a class="portfolio-cartao" href="${p.link}" target="_blank" rel="noopener" aria-label="Abrir o site ${p.nome} numa nova página">${miolo}
      <span class="ver">Ver site ao vivo <i aria-hidden="true">↗</i></span></a></li>`
      : `<li style="--i:${i}"><button type="button" class="portfolio-cartao" data-i="${i}" aria-label="Ver o projeto ${p.nome}">${miolo}
      <span class="ver">Ver projeto <i aria-hidden="true">→</i></span></button></li>`;
  }).join("");
  // cilindro: clicar (sem arrastar) num cartão com link abre o site
  // (o cilindro captura o ponteiro, por isso decide-se no pointerdown/pointerup do próprio cilindro)
  cartoes.forEach((c) => c.dataset.link && c.classList.add("com-link"));
  let toqueCartao = null;
  cil.addEventListener("pointerdown", (e) => {
    const c = e.target.closest(".cartao-projeto.com-link");
    toqueCartao = c ? { c, x: e.clientX, y: e.clientY } : null;
  }, true);
  cil.addEventListener("pointerup", (e) => {
    if (toqueCartao && Math.hypot(e.clientX - toqueCartao.x, e.clientY - toqueCartao.y) < 6) window.open(toqueCartao.c.dataset.link, "_blank", "noopener");
    toqueCartao = null;
  });
  const numWhats = String(S.whatsapp?.numero || "").replace(/\D/g, "");
  const abrirProjeto = (i) => {
    const p = projetos[i];
    $(".projeto-vis-nome", vis).textContent = p.nome;
    $(".projeto-vis-setor", vis).textContent = p.setor;
    const ecra = $(".projeto-vis-ecra", vis);
    ecra.classList.toggle("longo", !!p.longo);
    ecra.scrollTop = 0;
    const im = $("img", ecra); im.src = p.longo || p.src; im.alt = p.alt;
    $(".projeto-vis-whats", vis).href = `https://wa.me/${numWhats}?text=${encodeURIComponent(`Olá! Vi o projeto ${p.nome} no vosso portfólio e gostava de saber mais sobre um site para o meu negócio.`)}`;
    vis.hidden = false;
    requestAnimationFrame(() => vis.classList.add("aberto"));
    $(".projeto-vis-fechar", vis).focus();
  };
  const fecharProjeto = () => { vis.classList.remove("aberto"); setTimeout(() => (vis.hidden = true), 300); };
  grelha.addEventListener("click", (e) => { const c = e.target.closest("button.portfolio-cartao"); if (c) abrirProjeto(+c.dataset.i); });
  $(".projeto-vis-fechar", vis).addEventListener("click", fecharProjeto);
  vis.addEventListener("click", (e) => { if (e.target === vis) fecharProjeto(); });
  $(".projeto-vis-contacto", vis).addEventListener("click", (e) => {
    e.preventDefault(); e.stopPropagation();
    vis.hidden = true; vis.classList.remove("aberto"); dlg.close();
    lenis && lenis.start();
    setTimeout(() => irPara("#contacto"), 50);
  });
  dlg.addEventListener("cancel", (e) => { if (!vis.hidden) { e.preventDefault(); fecharProjeto(); } });
  $(".abrir-projetos").addEventListener("click", () => { dlg.showModal(); lenis && lenis.stop(); });
  $(".portfolio-fechar").addEventListener("click", () => dlg.close());
  dlg.addEventListener("close", () => { vis.hidden = true; vis.classList.remove("aberto"); lenis && lenis.start(); });
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });

  /* ── Google + IA: textos que se escrevem ──────────────────── */
  const gia = $(".gia");
  const digitar = $(".gia-digitar"), txtPesquisa = digitar.dataset.texto;
  const resposta = $(".gia-resposta"), palavras = resposta.dataset.texto.split(" ");
  const resultados = $$(".gia-res"), topo = $(".gia-res--top"), fonte = $(".gia-fonte"), mapa = $(".gia-mapa");
  const pontos = $$(".gia-pontos li");

  /* ── Integrações: órbita ──────────────────────────────────── */
  const ICONES = {
    whatsapp: '<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="#25D366"/><path fill="#fff" d="M16 7.5a8.5 8.5 0 0 0-7.3 12.8L7.6 24l3.8-1a8.5 8.5 0 1 0 4.6-15.5zm4.4 11.3c-.2.6-1.1 1.1-1.6 1.1-.4 0-.9.1-2.9-.7a10 10 0 0 1-4-3.6 4.4 4.4 0 0 1-.9-2.4 2.6 2.6 0 0 1 .8-1.9.9.9 0 0 1 .6-.3h.5c.2 0 .4 0 .6.5l.8 1.8c.1.2 0 .4 0 .5l-.4.5-.4.4c.4.7 2 2.6 3.7 3.1l.6-.7c.2-.2.3-.2.5-.1l1.7.8c.3.1.4.2.4.3a2 2 0 0 1-.1 1.2z"/></svg>',
    instagram: '<svg viewBox="0 0 32 32"><defs><linearGradient id="ig" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FEC053"/><stop offset=".5" stop-color="#F2203E"/><stop offset="1" stop-color="#5258CF"/></linearGradient></defs><rect x="3" y="3" width="26" height="26" rx="8" fill="url(#ig)"/><rect x="9" y="9" width="14" height="14" rx="4.5" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="16" cy="16" r="3.4" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="21.6" cy="10.4" r="1.3" fill="#fff"/></svg>',
    facebook: '<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="#1877F2"/><path fill="#fff" d="M17.6 30V19.6h3.3l.5-3.9h-3.8v-2.5c0-1.1.3-1.9 1.9-1.9h2V7.9a27 27 0 0 0-3-.2c-2.9 0-4.9 1.8-4.9 5.1v2.9h-3.3v3.9h3.3V30z"/></svg>',
    maps: '<svg viewBox="0 0 32 32"><path fill="#EA4335" d="M16 2a10 10 0 0 0-10 10c0 7.5 10 18 10 18s10-10.5 10-18A10 10 0 0 0 16 2z"/><path fill="#FBBC04" d="M6 12c0 2.6 1.4 5.8 3.3 8.7L16 12z"/><path fill="#34A853" d="M16 12l-6.7 8.7C12 25 16 30 16 30s4-4.3 6.9-9.3z"/><circle cx="16" cy="12" r="3.8" fill="#fff"/></svg>',
    analytics: '<svg viewBox="0 0 32 32"><rect x="20" y="4" width="7" height="24" rx="3.5" fill="#F9AB00"/><rect x="12.5" y="12" width="7" height="16" rx="3.5" fill="#E37400"/><circle cx="8.5" cy="24.5" r="3.5" fill="#E37400"/></svg>',
  };
  const integ = $$(".integra-lista li").map((li) => ({ nome: li.textContent, ic: ICONES[li.dataset.ic] }));
  const orbAnel = $(".orbita-anel"), raios = $(".orbita-linhas .raios");
  const orbIcones = integ.map((d, i) => {
    const el = document.createElement("div");
    el.className = "orbita-ic vidro";
    el.innerHTML = d.ic + `<small>${d.nome}</small>`;
    orbAnel.appendChild(el);
    const ln = document.createElementNS("http://www.w3.org/2000/svg", "line");
    ln.setAttribute("x1", 0); ln.setAttribute("y1", 0);
    ln.style.animationDelay = i * 0.5 + "s";
    raios.appendChild(ln);
    return { el, ln, a0: (i / integ.length) * Math.PI * 2 - Math.PI / 2 };
  });
  const marquee = document.createElement("div");
  marquee.className = "marquee";
  marquee.setAttribute("aria-hidden", "true");
  const faixa = integ.concat(integ).map((d) => `<div class="orbita-ic vidro">${d.ic}<small>${d.nome}</small></div>`).join("");
  marquee.innerHTML = `<div class="marquee-faixa">${faixa}</div>`;
  $(".integra").appendChild(marquee);
  let orbAng = 0;

  /* ── Botão magnético ──────────────────────────────────────── */
  const mag = $(".magnetico");
  if (mag && !toque && !reduzir) {
    addEventListener("pointermove", (e) => {
      if (movel()) return;
      const r = mag.getBoundingClientRect();
      const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      const dx = e.clientX - cx, dy = e.clientY - cy, d = Math.hypot(dx, dy);
      const raio = 80 + r.width / 2;
      mag.style.transform = d < raio ? `translate(${dx * 0.3}px, ${dy * 0.35}px)` : "";
    }, { passive: true });
  }

  /* ── FAQ: só uma aberta ───────────────────────────────────── */
  $$(".faq-item button").forEach((b) => b.addEventListener("click", () => {
    const item = b.closest(".faq-item"), abrir = !item.classList.contains("aberto");
    $$(".faq-item").forEach((it) => { it.classList.remove("aberto"); it.querySelector("button").setAttribute("aria-expanded", "false"); });
    if (abrir) { item.classList.add("aberto"); b.setAttribute("aria-expanded", "true"); }
  }));

  /* ── WhatsApp ─────────────────────────────────────────────── */
  const linkWhats = `https://wa.me/${String(S.whatsapp?.numero || "").replace(/\D/g, "")}?text=${encodeURIComponent(S.whatsapp?.mensagem || "")}`;
  $$("[data-whats]").forEach((a) => { a.href = linkWhats; a.target = "_blank"; a.rel = "noopener"; });
  const whats = $(".whats");
  let formNoEcra = false;
  new IntersectionObserver(([e]) => (formNoEcra = e.isIntersecting), { threshold: 0.2 }).observe($(".contacto-cartao"));

  /* ── Formulário ───────────────────────────────────────────── */
  const form = $(".form");
  const regras = {
    "Nome": (v) => (v.trim().length >= 2 ? "" : "Indica o teu nome."),
    "Telemóvel ou WhatsApp": (v) => (/^\+?[\d\s().-]{9,20}$/.test(v.trim()) && v.replace(/\D/g, "").length >= 9 ? "" : "Indica um número válido."),
    "Tipo de negócio": (v) => (v.trim().length >= 2 ? "" : "Diz-nos qual é o teu negócio."),
  };
  const validar = (campo) => {
    const box = campo.closest(".campo");
    let msg = "";
    if (campo.type === "radio") msg = form.querySelector(`[name="${campo.name}"]:checked`) ? "" : "Escolhe uma opção.";
    else if (campo.type === "checkbox") msg = campo.checked ? "" : "Para continuar, aceita a Política de Privacidade.";
    else msg = regras[campo.name] ? regras[campo.name](campo.value) : "";
    box.classList.toggle("erro", !!msg);
    box.querySelector(".campo-erro").textContent = msg;
    campo.setAttribute("aria-invalid", msg ? "true" : "false");
    return !msg;
  };
  $$("input[required]", form).forEach((c) => {
    c.addEventListener("blur", () => c.type !== "radio" && validar(c));
    c.addEventListener("input", () => (c.closest(".campo").classList.contains("erro") || c.type === "radio" || c.type === "checkbox") && validar(c));
    c.addEventListener("change", () => validar(c));
  });
  const status = $(".form-status", form);
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    if (form.elements._honey.value) return;
    const vistos = new Set();
    let ok = true;
    $$("input[required]", form).forEach((c) => {
      if (c.type === "radio") { if (vistos.has(c.name)) return; vistos.add(c.name); }
      if (!validar(c)) ok = false;
    });
    if (!ok) { status.className = "form-status falha"; status.textContent = "Revê os campos assinalados."; form.querySelector(".erro input")?.focus(); return; }
    const dados = Object.fromEntries(new FormData(form));
    delete dados._honey;
    const assunto = S.contato?.assunto || "Novo contacto pelo site";
    let url, corpo;
    if (S.contato?.web3formsChave) { url = "https://api.web3forms.com/submit"; corpo = { access_key: S.contato.web3formsChave, subject: assunto, from_name: S.nome, ...dados }; }
    else { url = `https://formsubmit.co/ajax/${encodeURIComponent(S.contato?.email || "")}`; corpo = { _subject: assunto, _template: "table", _captcha: "false", ...dados }; }
    const botao = form.querySelector("button[type=submit]");
    botao.disabled = true;
    status.className = "form-status"; status.textContent = "A enviar…";
    try {
      const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(corpo) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || j.success === false || j.success === "false") throw new Error(j.message || r.status);
      form.reset();
      status.textContent = "";
      const cartao = $(".contacto-cartao");
      cartao.style.minHeight = cartao.offsetHeight + "px";
      cartao.classList.add("enviado");
      $(".contacto-sucesso").hidden = false;
      window.mdConversao?.("formulario");
    } catch (e) {
      console.warn("Falha no envio:", e);
      status.className = "form-status falha";
      status.textContent = "Não foi possível enviar agora. Fala connosco no WhatsApp.";
    } finally { botao.disabled = false; }
  });

  /* ── Cookies (RGPD) ───────────────────────────────────────── */
  const ban = $(".cookies");
  const lerConsent = () => { try { return JSON.parse(localStorage.getItem("md-cookies") || "null"); } catch { return null; } };
  const gravar = (v) => { try { localStorage.setItem("md-cookies", JSON.stringify(v)); } catch {} };
  /* Google Analytics 4 + Google Ads com Consent Mode v2 (modo básico: nada carrega sem consentimento) */
  const ADS = S.googleAds || {};
  let tagsCarregadas = false;
  const consentimento = (c) => ({
    analytics_storage: c.estatistica ? "granted" : "denied",
    ad_storage: c.marketing ? "granted" : "denied",
    ad_user_data: c.marketing ? "granted" : "denied",
    ad_personalization: c.marketing ? "granted" : "denied",
  });
  const carregarTags = (c) => {
    if (!c || !(c.estatistica || c.marketing)) return;
    const ids = [c.estatistica && S.analytics, c.marketing && ADS.id].filter(Boolean);
    if (!ids.length) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { dataLayer.push(arguments); };
    if (tagsCarregadas) { gtag("consent", "update", consentimento(c)); ids.forEach((id) => gtag("config", id)); return; }
    tagsCarregadas = true;
    gtag("consent", "default", consentimento(c));
    gtag("js", new Date());
    ids.forEach((id) => gtag("config", id));
    const s = document.createElement("script");
    s.async = true; s.src = `https://www.googletagmanager.com/gtag/js?id=${ids[0]}`;
    document.head.appendChild(s);
  };
  /* Conversões: formulário enviado e clique no WhatsApp */
  window.mdConversao = (tipo) => {
    if (!window.gtag) return;
    const c = lerConsent() || {};
    if (c.estatistica && S.analytics) gtag("event", tipo === "formulario" ? "generate_lead" : "contacto_whatsapp", { metodo: tipo });
    const rotulo = ADS.conversoes?.[tipo];
    if (c.marketing && ADS.id && rotulo) gtag("event", "conversion", { send_to: `${ADS.id}/${rotulo}` });
  };
  document.addEventListener("click", (e) => { if (e.target.closest('a[href*="wa.me/"]')) window.mdConversao("whatsapp"); });
  function mostrarCookies() {
    const c = lerConsent();
    if (c) { carregarTags(c); return; }
    setTimeout(() => (ban.hidden = false), 1800);
  }
  ban.addEventListener("click", (e) => {
    const b = e.target.closest("[data-cookies]");
    if (!b) return;
    const acao = b.dataset.cookies;
    const op = $(".cookies-opcoes");
    let escolha;
    if (acao === "personalizar") {
      if (op.hidden) { op.hidden = false; b.textContent = "Guardar escolhas"; return; }
      escolha = { estatistica: op.querySelector('[name="estatistica"]').checked, marketing: op.querySelector('[name="marketing"]').checked };
    } else {
      const sim = acao === "aceitar";
      escolha = { estatistica: sim, marketing: sim };
    }
    gravar(escolha);
    carregarTags(escolha);
    if (tagsCarregadas && !escolha.estatistica && !escolha.marketing) gtag("consent", "update", consentimento(escolha));
    ban.hidden = true;
  });
  $(".link-cookies").addEventListener("click", () => { ban.hidden = false; });

  /* ── Ciclo principal: lê o scroll e atualiza tudo ─────────── */
  const hero = $(".hero"), heroTexto = $(".hero-texto"), dica = $(".hero-dica");
  const pil = $(".pilares"), pilaresLi = $$(".pilar");
  const gal = $(".galeria"), tese = $(".tese"), palavrasTese = $$(".tese-titulo .p"), sub = $(".sublinhar"), raiosEl = $("#raios");
  const rodape = $(".rodape"), gigante = $(".rodape-gigante");
  const secCeu = { pil, gal, func: $("#funcionalidades"), integ: $(".integra"), cont: $("#contacto"), rod: rodape };

  // Geometria em cache: medida só quando algo muda (evita recalcular o layout a cada frame)
  const geo = new Map();
  let docAlt = 0, orbLarg = 0;
  const medir = () => {
    [hero, pil, gal, tese, gia, rodape, secCeu.func, secCeu.integ, secCeu.cont].forEach((el) => {
      const r = el.getBoundingClientRect();
      geo.set(el, { top: r.top + scrollY, h: el.offsetHeight });
    });
    docAlt = document.documentElement.scrollHeight;
    orbLarg = $(".orbita").clientWidth;
  };
  const G_ = (el) => geo.get(el);
  const progresso = (el) => { const g = G_(el); return lim((scrollY - g.top) / Math.max(1, g.h - innerHeight)); };
  const topoDoc = (el) => G_(el).top;
  const caixa = (el) => { const g = G_(el), top = g.top - scrollY; return { top, height: g.h, bottom: top + g.h }; };
  medir();
  addEventListener("resize", medir);
  addEventListener("load", medir);
  if (document.fonts) document.fonts.ready.then(medir);
  if (window.ResizeObserver) new ResizeObserver(medir).observe(document.body);
  let corTopo = "", corHor = "";

  let ultimoY = scrollY, pilarAtivo = 0, mGia = 0, ultimoT = performance.now();
  const ciclo = (agora) => {
    const dt = Math.min(0.05, (agora - ultimoT) / 1000); ultimoT = agora;
    const y = scrollY, vh = innerHeight;
    const docH = docAlt - vh;
    MD.total = lim(y / Math.max(1, docH));
    MD.velocidade = lerp(MD.velocidade, Math.abs(y - ultimoY) / Math.max(dt, 0.001) / 1000, 0.1);

    // navegação esconde a descer, volta a subir
    if (Math.abs(y - ultimoY) > 4) nav.classList.toggle("escondida", y > ultimoY && y > 200 && menu.hidden);
    ultimoY = y;

    // céu: 0 manhã · 1 meio-dia · 2 fim de tarde · 3 crepúsculo
    const c = y + vh * 0.5;
    const paradas = [
      [topoDoc(secCeu.pil) + G_(secCeu.pil).h * 0.6, 0],
      [topoDoc(secCeu.gal) + vh * 0.5, 1],
      [topoDoc(secCeu.func) + G_(secCeu.func).h, 1],
      [topoDoc(secCeu.integ) + G_(secCeu.integ).h * 0.6, 2],
      [topoDoc(secCeu.cont) + G_(secCeu.cont).h * 0.55, 2.25],
      [Math.min(topoDoc(secCeu.rod) + vh * 0.2, docH + vh * 0.5 - 2), 3], // no telemóvel o ecrã é mais alto que o rodapé: garante o crepúsculo no fim
    ];
    let ceu = 0;
    if (c <= paradas[0][0]) ceu = 0;
    else if (c >= paradas[paradas.length - 1][0]) ceu = 3;
    else for (let i = 0; i < paradas.length - 1; i++) {
      const [a, va] = paradas[i], [b, vb] = paradas[i + 1];
      if (c >= a && c <= b) { ceu = lerp(va, vb, (c - a) / Math.max(1, b - a)); break; }
    }
    MD.ceu = ceu;

    // hero
    const h = reduzir ? 0 : progresso(hero);
    MD.hero = h;
    const ht = lim(h / 0.45);
    heroTexto.style.transform = `translate3d(0, ${-ht * 120}px, 0)`;
    heroTexto.style.opacity = 1 - ht;
    heroTexto.style.visibility = ht >= 1 ? "hidden" : "";
    dica.style.opacity = h > 0.02 ? 0 : 1;

    // pilares: o cartão ativo segue o scroll
    const p = progresso(pil);
    const rp = caixa(pil);
    const ip = p < 1 / 3 ? 0 : p < 2 / 3 ? 1 : 2;
    if (ip !== pilarAtivo) {
      pilaresLi.forEach((li, i) => li.classList.toggle("ativo", i === ip));
      pilarAtivo = ip;
    }

    // galeria
    if (!movel()) {
      const g = reduzir ? 0.3 : progresso(gal);
      const max = (cartoes.length - 1) * G.passo;
      const rot = lim(g * max + rotArrasto, -G.passo, max + G.passo) - rotEntrada * G.passo * 5;
      anel.style.transform = `translateZ(${G.R}px) rotateY(${rot}rad)`;
      let melhor = null, menor = 9;
      cartoes.forEach((card, i) => {
        const a = i * G.passo;
        const rel = a - rot;
        card.style.transform = `rotateY(${-a}rad) translateZ(${-G.R}px)`;
        const d = Math.abs(rel);
        card.style.opacity = d > 1.1 ? 0 : (1 - lim((d - 0.7) / 0.4)).toFixed(3);
        card.style.filter = `brightness(${(1 - lim(d / 0.9) * 0.28).toFixed(3)})`;
        if (d < menor) { menor = d; melhor = card; }
      });
      cartoes.forEach((cd) => cd.classList.toggle("frente", cd === melhor));
    }

    // tese: palavra a palavra + raios de sol
    const t = reduzir ? 1 : progresso(tese);
    palavrasTese.forEach((w, i) => w.classList.toggle("on", t > 0.08 + i * 0.16));
    sub.classList.toggle("on", t > 0.08 + (palavrasTese.length - 1) * 0.16);
    const rt = caixa(tese);
    const vis = lim(1 - Math.abs((rt.top + rt.height / 2) - vh / 2) / (rt.height / 2 + vh / 2));
    raiosEl.style.opacity = reduzir ? 0 : (vis * 0.9).toFixed(3);

    // Google + IA
    const q = reduzir ? 0.2 : progresso(gia);
    const m = q < 0.3 ? 1 : q < 0.6 ? 2 : 3;
    if (m !== mGia) { gia.dataset.m = m; pontos.forEach((li, i) => li.classList.toggle("ativo", i === m - 1)); mGia = m; }
    const nLetras = Math.round(lim((q - 0.02) / 0.12) * txtPesquisa.length);
    if (digitar.textContent.length !== nLetras) digitar.textContent = txtPesquisa.slice(0, nLetras);
    resultados.forEach((r, i) => r.classList.toggle("on", q > 0.15 + i * 0.03));
    topo.classList.toggle("brilha", q > 0.23);
    const nPal = Math.round(lim((q - 0.34) / 0.16) * palavras.length);
    if (resposta.dataset.n != nPal) { resposta.textContent = palavras.slice(0, nPal).join(" "); resposta.dataset.n = nPal; }
    fonte.classList.toggle("on", q > 0.52);
    mapa.classList.toggle("on", m === 3);
    gia.classList.toggle("fim", q > 0.88);

    // órbita (o scroll acelera)
    const orbW = orbLarg;
    if (!reduzir && orbW > 0) {
      orbAng += dt * (0.12 + Math.min(MD.velocidade, 4) * 0.5);
      const R = Math.min(230, orbW * 0.38);
      orbIcones.forEach((o) => {
        const a = o.a0 + orbAng, x = Math.cos(a) * R, yv = Math.sin(a) * R;
        o.el.style.transform = `translate(${x.toFixed(1)}px, ${yv.toFixed(1)}px)`;
        const k = 600 / orbW;
        o.ln.setAttribute("x2", (x * k).toFixed(1)); o.ln.setAttribute("y2", (yv * k).toFixed(1));
      });
    }

    // rodapé: palavra gigante enche da esquerda para a direita
    const rr = caixa(rodape);
    const enche = reduzir ? 1 : lim((vh - rr.top) / Math.max(1, rr.height));
    gigante.style.setProperty("--enche", (enche * 100).toFixed(1) + "%");

    // cor do céu para o fundo CSS (reserva se o WebGL falhar)
    const ct = corCeu(ceu, 0), ch = corCeu(ceu, 1);
    if (ct !== corTopo) { corTopo = ct; document.documentElement.style.setProperty("--ceu-topo", ct); }
    if (ch !== corHor) { corHor = ch; document.documentElement.style.setProperty("--ceu-horizonte", ch); }

    requestAnimationFrame(ciclo);
  };

  const PALETA = [["#7DB8FF", "#DCEEFF"], ["#4A90F0", "#CFE6FF"], ["#F6B27A", "#FFE3C2"], ["#1C2B54", "#6D6A9C"]];
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const PAL_RGB = PALETA.map((p) => p.map(hex));
  window.MD.paleta = PAL_RGB;
  function corCeu(v, k) {
    const i = Math.min(2, Math.floor(v)), f = v - i;
    const a = PAL_RGB[i][k], b = PAL_RGB[Math.min(3, i + 1)][k];
    return `rgb(${a.map((x, j) => Math.round(lerp(x, b[j], f))).join(",")})`;
  }

  requestAnimationFrame(ciclo);
})();
