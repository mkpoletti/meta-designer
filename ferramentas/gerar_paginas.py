# Meta Designer · gera as páginas de SEO (serviços por setor, cidades e guias)
# Uso (na pasta site/):  python -I ferramentas/gerar_paginas.py
# Depois: rever, atualizar sitemap.xml (é feito aqui) e publicar com git push.
import html
import json
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DOMINIO = "https://metadesigner.site"
HOJE = date.today().isoformat()
WHATS = "https://wa.me/5521966289500?text=" + "Ol%C3%A1!%20Quero%20saber%20mais%20sobre%20um%20site%20para%20o%20meu%20neg%C3%B3cio."

SVG_WHATS = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6a10.6 10.6 0 0 1-5.4-1.5l-.4-.2-3.9 1 1-3.8-.2-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.6 14.6 0 0 0 5.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.1-.3-.2-.6-.4z"/></svg>'

# Projetos reais do portfólio (os "conceito" vão sempre identificados)
PROJ = {
    "dentix": ("Dentix", "Implantologia", "dentix"),
    "oralplus": ("OralPlus", "Medicina dentária", "oralplus"),
    "bica": ("Dr. António Bica", "Reabilitação oral", "antonio-bica"),
    "nacar": ("Nácar", "Projeto conceito · Medicina dentária · Lisboa", "nacar"),
    "legatus": ("Legatus", "Advocacia", "legatus"),
    "terraco": ("Terraço Nobre", "Imobiliário", "terraco-nobre"),
    "nevogilde": ("Residência Nevogilde", "Projeto conceito · Imobiliário · Porto", "nevogilde"),
    "serena": ("Serena", "Projeto conceito · Bem-estar e nutrição", "serena"),
    "gaspar": ("António Gaspar", "Fisioterapia e exercício", "antonio-gaspar"),
    "funchal": ("Clínica em Casa", "Saúde ao domicílio · Funchal", "clinica-domicilio-funchal"),
    "cdt": ("CDT", "Logística · Portugal", "cdt-logistica"),
    "amplify": ("Amplify", "Audiovisual", "amplify"),
    "seo": ("Agência de SEO", "Marketing digital · Lisboa", "agencia-seo"),
    "conecta": ("Conecta Viagens", "Viagens", "conecta-viagens"),
}

PAGINAS_MENU = [
    ("/criacao-de-sites-lisboa", "Criação de sites em Lisboa"),
    ("/criacao-de-sites-porto", "Criação de sites no Porto"),
    ("/sites-para-clinicas-dentarias", "Sites para clínicas dentárias"),
    ("/sites-para-advogados", "Sites para advogados"),
    ("/sites-para-imobiliarias", "Sites para imobiliárias"),
    ("/quanto-custa-um-site", "Quanto custa um site"),
    ("/aparecer-no-chatgpt", "Como aparecer no ChatGPT"),
    ("/criacao-de-sites-braga", "Criação de sites em Braga"),
    ("/criacao-de-sites-coimbra", "Criação de sites em Coimbra"),
    ("/criacao-de-sites-algarve", "Criação de sites no Algarve"),
    ("/criacao-de-sites-madeira", "Criação de sites na Madeira"),
    ("/sites-para-clinicas", "Sites para clínicas e saúde"),
    ("/sites-para-restaurantes", "Sites para restaurantes"),
    ("/sites-para-alojamento-local", "Sites para alojamento local"),
]

PROCESSO = """
<div class="passos">
  <div class="passo"><b>01</b><h3>Desenhar</h3><p>Design exclusivo com as cores, a tipografia e as animações da tua marca. Aprovas o desenho antes de avançarmos.</p></div>
  <div class="passo"><b>02</b><h3>Construir</h3><p>Site rápido, seguro (SSL) e perfeito no telemóvel. Um site de uma página fica online em 2 a 5 dias úteis depois de recebermos os conteúdos.</p></div>
  <div class="passo"><b>03</b><h3>Ser encontrado</h3><p>Estrutura, textos e dados estruturados para o Google e para os buscadores de IA (ChatGPT, Gemini e Perplexity), com ligação ao Google Maps.</p></div>
</div>"""

INCLUIDO = """
<ul class="lista-check">
  <li><strong>Design exclusivo com animações</strong>, sem modelos prontos.</li>
  <li><strong>Perfeito no telemóvel</strong>, onde está a maioria das visitas.</li>
  <li><strong>SEO e GEO incluídos</strong>: títulos, descrições, dados estruturados, velocidade e textos pensados para o Google e para a IA.</li>
  <li><strong>WhatsApp e formulário</strong> visíveis em todas as secções.</li>
  <li><strong>RGPD</strong>: política de privacidade e gestão de cookies.</li>
  <li><strong>Google Analytics</strong> e ligação ao Google Maps.</li>
  <li><strong>Suporte em português</strong> e formação de 15 minutos para editares o site.</li>
</ul>"""


def esc(t):
    return html.escape(t, quote=True)


def projetos(chaves):
    out = []
    for k in chaves:
        nome, setor, img = PROJ[k]
        out.append(f'<figure><img src="/assets/projetos/{img}.webp" alt="Site {esc(nome)}: {esc(setor)}" width="700" height="522" loading="lazy"><figcaption><strong>{esc(nome)}</strong>{esc(setor)}</figcaption></figure>')
    return '<div class="projetos">' + "".join(out) + "</div>"


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faqs) + "</div>"


def chamada(titulo, texto):
    return f'''<section class="chamada">
  <h2>{titulo}</h2>
  <p>{texto}</p>
  <div class="botoes"><a class="botao" href="{WHATS}" target="_blank" rel="noopener">Falar no WhatsApp</a><a class="botao botao--claro" href="/#contacto">Pedir conversa grátis</a></div>
</section>'''


def relacionados(atual):
    links = "".join(f'<a href="{u}">{esc(n)}</a>' for u, n in PAGINAS_MENU if u != atual)
    return f'<section class="cartao"><h2>Também te pode interessar</h2><div class="relacionados">{links}<a href="/#projetos">Ver todos os projetos</a></div></section>'


def pagina(p):
    url = DOMINIO + p["caminho"]
    texto_faq = [(q, html.unescape(__import__("re").sub("<[^>]+>", "", a))) for q, a in p["faq"]]
    grafo = [
        {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": p["titulo"], "description": p["descricao"],
         "inLanguage": "pt-PT", "isPartOf": {"@id": DOMINIO + "/#website"}, "about": {"@id": DOMINIO + "/#organizacao"},
         "dateModified": HOJE, "breadcrumb": {"@id": url + "#migalhas"}},
        {"@type": "BreadcrumbList", "@id": url + "#migalhas", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"},
            {"@type": "ListItem", "position": 2, "name": p["migalha"], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in texto_faq]},
    ]
    if p["tipo"] == "servico":
        grafo.append({"@type": "Service", "@id": url + "#servico", "name": p["servico"], "serviceType": "Criação de sites",
                      "url": url, "provider": {"@id": DOMINIO + "/#organizacao"},
                      "areaServed": p.get("area", {"@type": "Country", "name": "Portugal"}),
                      "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": 300,
                                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": 300, "priceCurrency": "EUR"}}})
    else:
        grafo.append({"@type": "Article", "@id": url + "#artigo", "headline": p["h1_texto"], "description": p["descricao"],
                      "inLanguage": "pt-PT", "datePublished": HOJE, "dateModified": HOJE,
                      "author": {"@id": DOMINIO + "/#organizacao"}, "publisher": {"@id": DOMINIO + "/#organizacao"},
                      "mainEntityOfPage": {"@id": url + "#pagina"}, "image": DOMINIO + "/assets/img/og.jpg"})
    ld = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False)
    menu = "".join(f'<a href="{u}">{esc(n)}</a>' for u, n in PAGINAS_MENU)
    return f'''<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["titulo"])}</title>
<meta name="description" content="{esc(p["descricao"])}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-PT" href="{url}">
<meta property="og:type" content="{"article" if p["tipo"] == "guia" else "website"}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="pt_PT">
<meta property="og:site_name" content="Meta Designer">
<meta property="og:title" content="{esc(p["titulo"])}">
<meta property="og:description" content="{esc(p["descricao"])}">
<meta property="og:image" content="{DOMINIO}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#7DB8FF">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fontes/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/paginas.css?v={HOJE.replace("-", "")}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="topo"><a href="/"><img src="/assets/logo.svg" alt="Meta Designer" width="95" height="40"></a><a class="botao" href="/#contacto">Conversa grátis</a></header>
<nav class="migalhas" aria-label="Caminho"><ol><li><a href="/">Início</a></li><li aria-current="page">{esc(p["migalha"])}</li></ol></nav>
<main>
<section class="cartao">
  <p class="etiqueta">{p["etiqueta"]}</p>
  <h1>{p["h1"]}</h1>
  <p class="resumo">{p["resumo"]}</p>
  <div class="botoes"><a class="botao" href="{WHATS}" target="_blank" rel="noopener">Falar no WhatsApp</a><a class="botao botao--claro" href="/#projetos">Ver projetos</a></div>
</section>
{p["corpo"]}
<section class="cartao" id="perguntas"><h2>Perguntas <em>frequentes</em></h2>{faq_html(p["faq"])}</section>
{chamada(p["chamada_titulo"], p["chamada_texto"])}
{relacionados(p["caminho"])}
</main>
<footer>
  <nav aria-label="Páginas">{menu}<a href="/privacidade">Privacidade</a><a href="/termos">Termos</a></nav>
  © 2026 Meta Designer · Estúdio brasileiro de web design para negócios em Portugal · CNPJ 38.284.190/0001-99
</footer>
<a class="whats" href="{WHATS}" target="_blank" rel="noopener" aria-label="Falar connosco no WhatsApp">{SVG_WHATS}</a>
</body>
</html>
'''


def sec(titulo, conteudo):
    return f'<section class="cartao"><h2>{titulo}</h2>{conteudo}</section>'


# ───────────────────────── conteúdo ─────────────────────────
P = []

P.append(dict(
    caminho="/criacao-de-sites-lisboa", tipo="servico", migalha="Criação de sites em Lisboa",
    servico="Criação de sites em Lisboa",
    area={"@type": "City", "name": "Lisboa", "containedInPlace": {"@type": "Country", "name": "Portugal"}},
    titulo="Criação de Sites em Lisboa desde 300€ | Meta Designer",
    descricao="Criação de sites profissionais para negócios em Lisboa: design exclusivo com animações, perfeito no telemóvel e pronto para o Google e para o ChatGPT. Desde 300€.",
    etiqueta="Web design · Lisboa", h1_texto="Criação de sites em Lisboa",
    h1="Criação de sites <em>em Lisboa</em>",
    resumo="A Meta Designer cria sites profissionais para negócios de Lisboa e da Grande Lisboa: design exclusivo com animações, rápido no telemóvel e preparado para aparecer no Google e nas respostas do ChatGPT. Sites desde 300€, com atendimento 100% online em português.",
    corpo=sec("Um site feito para <em>competir em Lisboa</em>",
              "<p>Em Lisboa, quase todas as áreas têm dezenas de negócios a disputar a mesma pesquisa: clínicas, restaurantes, imobiliárias, advogados, estúdios. Quem aparece primeiro e transmite mais confiança nos primeiros segundos fica com o contacto.</p>"
              "<p>Por isso cada site que criamos começa pelo que o cliente procura (o serviço, o bairro, a urgência) e só depois passa para o design. O resultado é um site que impressiona, mas que também responde de forma clara a quem pesquisa “perto de mim” no telemóvel.</p>"
              "<h3>Pesquisa local: Lisboa, bairro a bairro</h3><p>Ligamos o site ao teu perfil no Google Maps e escrevemos os textos com a tua zona de atuação (por exemplo Avenidas Novas, Parque das Nações, Alvalade, Oeiras ou Cascais), para que o Google perceba onde estás e a quem serves.</p>")
          + sec("Como <em>trabalhamos</em>", "<p>Tudo online, por videochamada, WhatsApp e e-mail. Não precisas de te deslocar: aprovas cada etapa no teu tempo.</p>" + PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO)
          + sec("Projetos <em>com ligação a Lisboa</em>", "<p>Alguns trabalhos do nosso portfólio. Os projetos conceito estão identificados como tal.</p>" + projetos(["seo", "nacar", "dentix", "legatus"])),
    faq=[
        ("Quanto custa criar um site em Lisboa?", "Os sites da Meta Designer começam nos 300€. O valor final depende do número de páginas e das funcionalidades. Numa conversa grátis de 15 minutos dizemos-te quanto custa o teu, antes de avançares."),
        ("Têm escritório em Lisboa?", "Não. A Meta Designer é um estúdio brasileiro que trabalha 100% online para negócios em Portugal, em português de Portugal, por videochamada, WhatsApp e e-mail."),
        ("Quanto tempo demora a ficar online?", "Um site de uma página fica online em 2 a 5 dias úteis depois de recebermos os conteúdos. Sites maiores dependem do tamanho e da estrutura."),
        ("O site vai aparecer no Google?", "O site sai preparado para competir: estrutura, velocidade, textos e dados estruturados otimizados, e ligação ao Google Maps. Ninguém pode garantir o 1.º lugar, mas o teu site entra na corrida com a base certa."),
    ],
    chamada_titulo="Tens um negócio <em>em Lisboa?</em>",
    chamada_texto="Conversa grátis de 15 minutos: mostramos-te projetos do teu setor e dizemos-te quanto custa o teu site.",
))

P.append(dict(
    caminho="/criacao-de-sites-porto", tipo="servico", migalha="Criação de sites no Porto",
    servico="Criação de sites no Porto",
    area={"@type": "City", "name": "Porto", "containedInPlace": {"@type": "Country", "name": "Portugal"}},
    titulo="Criação de Sites no Porto desde 300€ | Meta Designer",
    descricao="Criação de sites profissionais para negócios do Porto: design com animações, rápido no telemóvel e pronto para o Google e para a IA. Desde 300€, atendimento online.",
    etiqueta="Web design · Porto", h1_texto="Criação de sites no Porto",
    h1="Criação de sites <em>no Porto</em>",
    resumo="Sites profissionais para negócios do Porto e do Grande Porto, de Matosinhos a Gaia: design exclusivo com animações, perfeito no telemóvel e preparado para o Google e para os buscadores de IA. Desde 300€, com atendimento 100% online.",
    corpo=sec("Um site à altura <em>do teu negócio</em>",
              "<p>O Porto tem cada vez mais negócios que vivem da pesquisa online: clínicas, imobiliárias, restaurantes, alojamento local, serviços para empresas. Um site lento ou desatualizado faz o cliente voltar à pesquisa e escolher o vizinho.</p>"
              "<p>Desenhamos cada site do zero para a tua marca e escrevemos os textos a pensar em quem pesquisa no Porto: o serviço, a zona e as dúvidas que aparecem antes de ligar.</p>"
              "<h3>Visível no Google Maps e na pesquisa local</h3><p>Integramos o teu perfil do Google Maps e indicamos a tua zona de atuação (Boavista, Foz, Baixa, Matosinhos, Maia, Gaia), para que apareças a quem procura perto.</p>")
          + sec("Como <em>trabalhamos</em>", "<p>Tudo online e em português, com aprovação tua em cada etapa.</p>" + PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO)
          + sec("Projetos <em>do portfólio</em>", "<p>A Residência Nevogilde é um projeto conceito para o mercado imobiliário do Porto.</p>" + projetos(["nevogilde", "terraco", "cdt", "gaspar"])),
    faq=[
        ("Quanto custa um site no Porto?", "Os sites começam nos 300€. O preço final depende das páginas e funcionalidades de que precisas, e dizemos-te o valor exato numa conversa grátis de 15 minutos."),
        ("Preciso de reunir presencialmente?", "Não. Trabalhamos 100% online, por videochamada, WhatsApp e e-mail, em português de Portugal."),
        ("Posso editar o site depois?", "Sim. Mostramos-te como, em 15 minutos."),
        ("Emitem fatura?", "Sim. Explicamos como funciona a faturação na conversa grátis, antes de avançares."),
    ],
    chamada_titulo="O teu negócio <em>no Porto</em>, com um site à altura.",
    chamada_texto="Fala connosco: em 15 minutos dizemos-te o que precisas, quanto custa e quando fica pronto.",
))

P.append(dict(
    caminho="/sites-para-clinicas-dentarias", tipo="servico", migalha="Sites para clínicas dentárias",
    servico="Criação de sites para clínicas dentárias",
    titulo="Sites para Clínicas Dentárias e Dentistas | Meta Designer",
    descricao="Criação de sites para clínicas dentárias e dentistas em Portugal: marcação por WhatsApp, especialidades explicadas, pronto para o Google e o ChatGPT. Desde 300€.",
    etiqueta="Medicina dentária", h1_texto="Sites para clínicas dentárias",
    h1="Sites para <em>clínicas dentárias</em>",
    resumo="Criamos sites para clínicas dentárias, implantologia e reabilitação oral em Portugal: transmitem confiança logo no primeiro ecrã, explicam cada tratamento com clareza e levam o paciente a marcar consulta pelo WhatsApp ou formulário. Desde 300€.",
    corpo=sec("O que um paciente procura <em>antes de marcar</em>",
              "<p>Quem procura um dentista quer resolver três dúvidas depressa: se a clínica trata o seu caso, se é de confiança e como marcar. O site tem de responder às três no telemóvel, em segundos.</p>"
              "<ul class=\"lista-check\">"
              "<li><strong>Especialidades explicadas</strong>: implantes, ortodontia, estética dentária, higiene oral, cada uma com a sua secção.</li>"
              "<li><strong>Equipa e instalações</strong> com fotografia real, que é o que gera confiança.</li>"
              "<li><strong>Marcação a um toque</strong>: WhatsApp, telefone e formulário sempre visíveis.</li>"
              "<li><strong>Localização e horários</strong> ligados ao Google Maps.</li>"
              "<li><strong>Perguntas frequentes</strong> sobre dor, preços indicativos e acordos, escritas para o Google e para a IA.</li>"
              "</ul>")
          + sec("Projetos <em>de medicina dentária</em>", "<p>Clínicas dentárias que já estão online connosco. O Nácar é um projeto conceito.</p>" + projetos(["dentix", "oralplus", "bica", "nacar"]))
          + sec("Como <em>trabalhamos</em>", PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO),
    faq=[
        ("Quanto custa um site para uma clínica dentária?", "Desde 300€. Uma clínica com várias especialidades costuma precisar de mais páginas; numa conversa grátis de 15 minutos dizemos-te o valor exato."),
        ("O site permite marcar consultas?", "Sim. Incluímos WhatsApp e formulário em todas as secções. Se já usas um software de marcação online, podemos ligar o botão de marcação a esse sistema."),
        ("Posso mostrar casos antes e depois?", "Podes, desde que tenhas autorização dos pacientes e respeites as regras da Ordem dos Médicos Dentistas sobre publicidade. Ajudamos-te a apresentar os casos de forma cuidada."),
        ("O site aparece quando alguém pesquisa “dentista perto de mim”?", "Preparamos o site para a pesquisa local: textos com a tua zona, dados estruturados e ligação ao Google Maps. A posição depende também do teu perfil no Google e das avaliações dos pacientes."),
    ],
    chamada_titulo="Mais pacientes a <em>marcar pelo site</em>.",
    chamada_texto="Mostramos-te outros projetos de clínicas e dizemos-te quanto custa o teu site, numa conversa grátis de 15 minutos.",
))

P.append(dict(
    caminho="/sites-para-advogados", tipo="servico", migalha="Sites para advogados",
    servico="Criação de sites para advogados e escritórios de advocacia",
    titulo="Sites para Advogados e Escritórios | Meta Designer",
    descricao="Criação de sites para advogados e sociedades de advogados em Portugal: sóbrios, credíveis, com áreas de prática claras e prontos para o Google e a IA. Desde 300€.",
    etiqueta="Advocacia", h1_texto="Sites para advogados",
    h1="Sites para <em>advogados</em>",
    resumo="Criamos sites para advogados e sociedades de advogados em Portugal: sóbrios e credíveis, com as áreas de prática bem explicadas e um contacto simples e discreto. Prontos para o Google e para os buscadores de IA, desde 300€.",
    corpo=sec("Credibilidade <em>antes do primeiro contacto</em>",
              "<p>Quem procura um advogado está muitas vezes preocupado e com pressa. O site tem de transmitir seriedade, mostrar experiência e explicar em linguagem simples como podes ajudar.</p>"
              "<ul class=\"lista-check\">"
              "<li><strong>Áreas de prática</strong> com páginas próprias: família, laboral, imobiliário, empresas, imigração.</li>"
              "<li><strong>Perfil dos advogados</strong> com formação e percurso.</li>"
              "<li><strong>Contacto discreto</strong> por formulário, telefone ou WhatsApp, com política de privacidade em regra.</li>"
              "<li><strong>Conteúdo informativo</strong> que responde às perguntas que as pessoas fazem ao Google e ao ChatGPT.</li>"
              "</ul>"
              "<p>Os textos respeitam as regras do Estatuto da Ordem dos Advogados sobre informação e publicidade: informativos, sem promessas de resultados.</p>")
          + sec("Projeto <em>de advocacia</em>", projetos(["legatus"]))
          + sec("Como <em>trabalhamos</em>", PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO),
    faq=[
        ("Quanto custa um site para um escritório de advogados?", "Desde 300€. Escritórios com várias áreas de prática e advogados costumam precisar de mais páginas; dizemos-te o valor exato numa conversa grátis de 15 minutos."),
        ("Os textos respeitam as regras da Ordem dos Advogados?", "Sim. Escrevemos textos informativos e sóbrios, sem promessas de resultados nem comparações. A revisão final do conteúdo é sempre tua."),
        ("Posso ter um blog com artigos jurídicos?", "Sim. Artigos que respondem a dúvidas comuns são uma das melhores formas de aparecer no Google e nas respostas da IA."),
        ("O site está preparado para o RGPD?", "Sim. Incluímos política de privacidade, gestão de cookies e formulários com consentimento."),
    ],
    chamada_titulo="Um site <em>à altura do teu escritório</em>.",
    chamada_texto="Conversa grátis de 15 minutos, sem compromisso.",
))

P.append(dict(
    caminho="/sites-para-imobiliarias", tipo="servico", migalha="Sites para imobiliárias",
    servico="Criação de sites para imobiliárias e empreendimentos",
    titulo="Sites para Imobiliárias e Empreendimentos | Meta Designer",
    descricao="Criação de sites para imobiliárias, consultores e empreendimentos em Portugal: imagens de grande impacto, plantas, galeria e contacto rápido. Desde 300€.",
    etiqueta="Imobiliário", h1_texto="Sites para imobiliárias",
    h1="Sites para <em>imobiliárias</em>",
    resumo="Criamos sites para imobiliárias, consultores e empreendimentos em Portugal, com imagens de grande impacto, animações de cinema e um caminho curto até ao pedido de visita. Prontos para o Google e para a IA, desde 300€.",
    corpo=sec("Vender <em>o espaço antes da visita</em>",
              "<p>No imobiliário, o site é a primeira visita ao imóvel. Fotografia, vídeo e animação têm de mostrar a luz, a vista e os acabamentos, e o pedido de informação tem de estar sempre à mão.</p>"
              "<ul class=\"lista-check\">"
              "<li><strong>Landing pages de empreendimento</strong> com galeria, plantas, tipologias e localização.</li>"
              "<li><strong>Pedido de visita</strong> por WhatsApp ou formulário, em todas as secções.</li>"
              "<li><strong>Mapa e pontos de interesse</strong> da zona: escolas, transportes, praia, comércio.</li>"
              "<li><strong>Versão em inglês</strong> para compradores estrangeiros, quando fizer sentido.</li>"
              "</ul>")
          + sec("Projetos <em>de imobiliário</em>", "<p>A Residência Nevogilde é um projeto conceito.</p>" + projetos(["terraco", "nevogilde"]))
          + sec("Como <em>trabalhamos</em>", PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO),
    faq=[
        ("Quanto custa um site para um empreendimento imobiliário?", "Desde 300€ para uma página de apresentação. Sites com vários imóveis ou integração com portais têm outro valor; dizemos-te qual numa conversa grátis."),
        ("Posso ligar o site ao meu software de imóveis ou aos portais?", "Depende do software. Avaliamos contigo na conversa inicial se a integração é possível e qual o custo."),
        ("O site pode ter versão em inglês?", "Sim, quando o público inclui compradores estrangeiros."),
        ("Quanto tempo demora?", "Uma página de empreendimento fica online em 2 a 5 dias úteis depois de recebermos as imagens e os textos."),
    ],
    chamada_titulo="O teu próximo empreendimento, <em>com um site de cinema</em>.",
    chamada_texto="Mostramos-te projetos do setor e dizemos-te quanto custa, em 15 minutos.",
))

P.append(dict(
    caminho="/quanto-custa-um-site", tipo="guia", migalha="Quanto custa um site",
    titulo="Quanto Custa um Site em Portugal (2026) | Meta Designer",
    descricao="Quanto custa um site profissional em Portugal: o que entra no preço, valores de referência por tipo de site, custos anuais (domínio, alojamento) e como evitar surpresas.",
    etiqueta="Guia · Preços", h1_texto="Quanto custa um site em Portugal?",
    h1="Quanto custa <em>um site em Portugal?</em>",
    resumo="Depende do que o site tem de fazer. Uma página de apresentação simples custa muito menos do que uma loja online ou um site com dezenas de páginas. Neste guia explicamos o que entra no preço, os custos anuais que muitas vezes ficam esquecidos e quanto custa um site na Meta Designer (desde 300€).",
    corpo=sec("O que <em>entra no preço</em> de um site",
              "<table class=\"tabela\"><thead><tr><th>Componente</th><th>O que é</th><th>Pesa no preço?</th></tr></thead><tbody>"
              "<tr><td>Número de páginas</td><td>Uma página única (landing page) ou várias páginas (serviços, sobre, blog, contactos).</td><td>Muito</td></tr>"
              "<tr><td>Design</td><td>Modelo pronto ou design exclusivo, com ou sem animações.</td><td>Muito</td></tr>"
              "<tr><td>Funcionalidades</td><td>Loja online, marcações, área de cliente, várias línguas, integrações.</td><td>Muito</td></tr>"
              "<tr><td>Textos e imagens</td><td>Se és tu a fornecer ou se a agência escreve e trata as imagens.</td><td>Médio</td></tr>"
              "<tr><td>SEO</td><td>Preparação para o Google: estrutura, velocidade, dados estruturados.</td><td>Médio</td></tr>"
              "<tr><td>Domínio e alojamento</td><td>O endereço (.pt, .com) e o servidor onde o site vive. Pagam-se todos os anos.</td><td>Baixo, mas recorrente</td></tr>"
              "</tbody></table>")
          + sec("Custos <em>que se esquecem</em>",
                "<p>Além do valor do projeto, um site tem custos anuais: o domínio, o alojamento e, se houver, licenças de plugins ou de software de marcações. Antes de fechar qualquer orçamento, pergunta sempre:</p>"
                "<ul class=\"lista-check\"><li><strong>O domínio fica em meu nome?</strong> Deve ficar.</li><li><strong>Quanto custa o alojamento por ano</strong> e quem o renova?</li><li><strong>Consigo editar o site sozinho</strong> ou cada alteração é paga?</li><li><strong>O site é meu</strong> se mudar de agência?</li></ul>")
          + sec("Quanto custa <em>na Meta Designer</em>",
                "<p>Os nossos sites começam nos <strong>300€</strong>, com design exclusivo, animações, versão para telemóvel, SEO e preparação para a IA incluídos. O valor final depende do número de páginas e das funcionalidades.</p>"
                "<p>Pagas só 20% para começar. Os restantes 80% só depois de aprovares a última fase, com o site pronto. Domínio e alojamento dependem do plano que escolheres e explicamos tudo antes de avançares.</p>"
                "<div class=\"botoes\"><a class=\"botao\" href=\"/#contacto\">Saber quanto custa o meu</a></div>")
          + sec("Barato <em>pode sair caro?</em>",
                "<p>Um site muito barato pode sair caro se for lento, se não aparecer no Google ou se ficar preso a uma plataforma que não controlas. O preço certo é o de um site que traz contactos e que é teu. Compara sempre o que está incluído, não só o valor.</p>"),
    faq=[
        ("Quanto custa um site simples em Portugal?", "Uma página de apresentação simples é a opção mais económica. Na Meta Designer começa nos 300€, com design exclusivo, versão para telemóvel e SEO incluídos."),
        ("O domínio e o alojamento estão incluídos?", "Depende do plano. Explicamos-te tudo na conversa grátis de 15 minutos, antes de avançares."),
        ("Tenho de pagar tudo no início?", "Na Meta Designer pagas 20% para começar e 80% só depois de aprovares o site pronto."),
        ("Quanto custa manter um site por ano?", "Os custos anuais fixos são o domínio e o alojamento. Alterações de conteúdo podes fazer tu, depois de uma formação de 15 minutos."),
    ],
    chamada_titulo="Queres saber <em>quanto custa o teu?</em>",
    chamada_texto="Em 15 minutos dizemos-te o que precisas, quanto custa e quando fica pronto.",
))

P.append(dict(
    caminho="/aparecer-no-chatgpt", tipo="guia", migalha="Como aparecer no ChatGPT",
    titulo="Como Aparecer no ChatGPT e Gemini (GEO) | Meta Designer",
    descricao="Como fazer o teu negócio aparecer nas respostas do ChatGPT, Gemini e Perplexity: o que é GEO, o que a IA lê num site e uma checklist prática para negócios em Portugal.",
    etiqueta="Guia · SEO para IA", h1_texto="Como aparecer no ChatGPT, no Gemini e no Perplexity",
    h1="Como aparecer <em>no ChatGPT</em>",
    resumo="Cada vez mais pessoas perguntam ao ChatGPT, ao Gemini ou ao Perplexity qual é o melhor serviço perto delas. A IA responde com poucos nomes. Para estares entre eles, o teu site tem de ser fácil de ler, de entender e de citar. A isto chama-se GEO (Generative Engine Optimization).",
    corpo=sec("O que é <em>GEO</em>?",
              "<p>GEO é a otimização de um site para os buscadores de inteligência artificial. Enquanto o SEO tradicional trabalha para aparecer nos links do Google, o GEO trabalha para que a IA use o teu site como fonte quando responde a uma pergunta.</p>"
              "<p>As duas coisas somam-se: muitos buscadores de IA consultam a web em tempo real e apoiam-se em sites bem posicionados e bem estruturados.</p>")
          + sec("O que a IA <em>lê antes de recomendar</em>",
                "<ul class=\"lista-check\">"
                "<li><strong>Serviços explicados com clareza</strong>: o que fazes, onde e para quem, em frases diretas.</li>"
                "<li><strong>Dados estruturados (schema.org)</strong>: nome, serviços, zona, contactos e perguntas frequentes num formato que as máquinas entendem.</li>"
                "<li><strong>Perguntas frequentes reais</strong>, com respostas curtas e completas.</li>"
                "<li><strong>Presença local consistente</strong>: o mesmo nome, morada e telefone no site, no Google Maps e nos diretórios.</li>"
                "<li><strong>Velocidade e acesso</strong>: páginas leves e um robots.txt que deixa entrar os robôs de IA.</li>"
                "<li><strong>Sinais de confiança</strong>: avaliações, menções noutros sites, projetos e equipa reais.</li>"
                "</ul>")
          + sec("Checklist <em>para o teu site</em>",
                "<table class=\"tabela\"><thead><tr><th>Verificar</th><th>Como</th></tr></thead><tbody>"
                "<tr><td>Os robôs de IA podem ler o site?</td><td>No ficheiro robots.txt, não bloquear GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot e Google-Extended.</td></tr>"
                "<tr><td>Há dados estruturados?</td><td>Organization ou LocalBusiness, Service e FAQPage, validados no teste de resultados avançados do Google.</td></tr>"
                "<tr><td>A primeira frase de cada página responde?</td><td>Começa por dizer o que é, para quem e onde. A IA cita frases que se percebem sozinhas.</td></tr>"
                "<tr><td>Tens um ficheiro llms.txt?</td><td>Um resumo em texto do negócio, pensado para modelos de linguagem.</td></tr>"
                "<tr><td>O Google Maps está completo?</td><td>Categoria, horário, fotos e avaliações. Muitos assistentes usam estes dados.</td></tr>"
                "</tbody></table>")
          + sec("Garantias? <em>Não há</em>.",
                "<p>Ninguém controla o que a IA responde, tal como ninguém pode garantir o 1.º lugar no Google. O que se pode fazer é dar à IA a melhor informação possível sobre o teu negócio. Todos os sites da Meta Designer saem com esta base: dados estruturados, perguntas frequentes, llms.txt e acesso aberto aos buscadores de IA.</p>"),
    faq=[
        ("O que é GEO?", "GEO (Generative Engine Optimization) é a otimização de um site para aparecer nas respostas de buscadores de IA como o ChatGPT, o Gemini e o Perplexity."),
        ("SEO e GEO são a mesma coisa?", "Não, mas complementam-se. O SEO trabalha a posição nos resultados do Google; o GEO trabalha a forma como a IA lê, entende e cita o teu site. Uma boa base técnica serve os dois."),
        ("Posso pagar para aparecer no ChatGPT?", "Não é possível comprar uma recomendação orgânica no ChatGPT. O caminho é ter um site claro, estruturado e com sinais de confiança."),
        ("Os sites da Meta Designer já vêm preparados para a IA?", "Sim. Incluem dados estruturados, perguntas frequentes, llms.txt e robots.txt aberto aos buscadores de IA."),
    ],
    chamada_titulo="Queres que a IA <em>recomende o teu negócio?</em>",
    chamada_texto="Criamos sites preparados para o Google e para a IA. Fala connosco: a conversa é grátis.",
))


FAQ_CIDADE = lambda cidade: [
    (f"Quanto custa criar um site em {cidade}?", "Os sites da Meta Designer começam nos 300€. O valor final depende do número de páginas e das funcionalidades, e dizemos-te o preço exato numa conversa grátis de 15 minutos."),
    ("Preciso de reunir presencialmente?", "Não. A Meta Designer é um estúdio brasileiro que trabalha 100% online para negócios em Portugal, em português de Portugal, por videochamada, WhatsApp e e-mail."),
    ("Quanto tempo demora?", "Um site de uma página fica online em 2 a 5 dias úteis depois de recebermos os conteúdos. Sites maiores dependem do tamanho e da estrutura."),
    ("O site aparece no Google Maps?", "Ligamos o site ao teu perfil do Google Maps e indicamos a tua zona de atuação nos textos e nos dados estruturados. A posição no mapa depende também do teu perfil e das avaliações."),
]


def cidade(caminho, nome, prep, regiao, intro, contexto, zonas, proj, nota_proj=""):
    return dict(
        caminho=caminho, tipo="servico", migalha=f"Criação de sites {prep} {nome}",
        servico=f"Criação de sites {prep} {nome}",
        area={"@type": "AdministrativeArea" if regiao else "City", "name": nome, "containedInPlace": {"@type": "Country", "name": "Portugal"}},
        titulo=f"Criação de Sites {prep} {nome} desde 300€ | Meta Designer",
        descricao=f"Criação de sites profissionais para negócios {prep} {nome}: design com animações, rápido no telemóvel e pronto para o Google e para a IA. Desde 300€, atendimento online.",
        etiqueta=f"Web design · {nome}", h1_texto=f"Criação de sites {prep} {nome}",
        h1=f"Criação de sites <em>{prep} {nome}</em>",
        resumo=intro,
        corpo=sec(f"Pensado para <em>quem pesquisa {prep} {nome}</em>", contexto
                  + f"<h3>Pesquisa local {prep} {nome}</h3><p>Escrevemos os textos com a tua zona de atuação ({zonas}) e ligamos o site ao teu perfil do Google Maps, para que o Google perceba onde estás e a quem serves.</p>")
              + sec("Como <em>trabalhamos</em>", "<p>Tudo online e em português, com aprovação tua em cada etapa.</p>" + PROCESSO)
              + sec("O que vem <em>incluído</em>", INCLUIDO)
              + sec("Projetos <em>do portfólio</em>", (f"<p>{nota_proj}</p>" if nota_proj else "") + projetos(proj)),
        faq=FAQ_CIDADE(nome),
        chamada_titulo=f"Tens um negócio <em>{prep} {nome}?</em>",
        chamada_texto="Conversa grátis de 15 minutos: mostramos-te projetos do teu setor e dizemos-te quanto custa o teu site.",
    )


P.append(cidade("/criacao-de-sites-braga", "Braga", "em", False,
    "Sites profissionais para negócios de Braga e do Minho, de Guimarães a Barcelos: design exclusivo com animações, perfeito no telemóvel e preparado para o Google e para os buscadores de IA. Desde 300€, com atendimento 100% online.",
    "<p>Braga é uma das cidades mais jovens do país, com uma universidade forte, uma indústria tecnológica em crescimento e muito comércio e serviços de proximidade. É um público que pesquisa no telemóvel e decide depressa.</p><p>Um site rápido, claro e com contacto a um toque faz a diferença entre receber o pedido ou vê-lo ir para o concorrente da rua ao lado.</p>",
    "centro histórico, Maximinos, São Victor, Guimarães, Barcelos, Vila Verde", ["cdt", "gaspar", "legatus", "dentix"]))

P.append(cidade("/criacao-de-sites-coimbra", "Coimbra", "em", False,
    "Sites profissionais para negócios de Coimbra e da Região Centro: design exclusivo com animações, rápido no telemóvel e pronto para o Google e para a IA. Desde 300€, com atendimento 100% online em português.",
    "<p>Coimbra junta saúde, ensino e turismo: clínicas e consultórios, explicações e formação, restauração e alojamento. Em todos estes setores, a primeira impressão acontece no Google, muitas vezes antes de o cliente saber o teu nome.</p><p>Por isso desenhamos o site a partir do que as pessoas pesquisam em Coimbra e das dúvidas que têm antes de ligar.</p>",
    "Baixa, Celas, Solum, Santa Clara, Figueira da Foz, Cantanhede", ["oralplus", "funchal", "gaspar", "conecta"]))

P.append(cidade("/criacao-de-sites-algarve", "Algarve", "no", True,
    "Sites profissionais para negócios do Algarve, de Faro a Lagos: design exclusivo com animações, perfeito no telemóvel, em português e em inglês quando fizer sentido, e preparado para o Google e para a IA. Desde 300€.",
    "<p>No Algarve, grande parte dos clientes chega pela pesquisa: turistas à procura de alojamento, restaurantes e experiências, e residentes estrangeiros à procura de serviços. Um site bonito mas lento, ou só em português, perde metade dessas pessoas.</p><p>Criamos sites rápidos, com galeria de impacto, reservas e contacto por WhatsApp, e versão em inglês para o público internacional.</p>",
    "Faro, Loulé, Albufeira, Portimão, Lagos, Tavira, Vilamoura", ["conecta", "terraco", "serena", "amplify"], "A Serena é um projeto conceito."))

P.append(cidade("/criacao-de-sites-madeira", "Madeira", "na", True,
    "Sites profissionais para negócios da Madeira, do Funchal ao Porto Santo: design exclusivo com animações, rápido no telemóvel e preparado para o Google e para os buscadores de IA. Desde 300€, com atendimento 100% online.",
    "<p>Na Madeira, turismo, saúde e serviços vivem da pesquisa online. Quem chega à ilha procura no telemóvel, e quem vive cá compara antes de marcar.</p><p>Já temos clientes na Madeira, como a Clínica em Casa, de saúde ao domicílio no Funchal. Sabemos o que um site tem de mostrar para gerar confiança e contactos na ilha.</p>",
    "Funchal, Santa Cruz, Câmara de Lobos, Machico, Caniço, Porto Santo", ["funchal", "gaspar", "oralplus", "conecta"]))

P.append(dict(
    caminho="/sites-para-clinicas", tipo="servico", migalha="Sites para clínicas e saúde",
    servico="Criação de sites para clínicas, consultórios e profissionais de saúde",
    titulo="Sites para Clínicas, Fisioterapia e Saúde | Meta Designer",
    descricao="Criação de sites para clínicas, fisioterapia, nutrição e saúde ao domicílio em Portugal: confiança, especialidades claras e marcação por WhatsApp. Desde 300€.",
    etiqueta="Saúde e bem-estar", h1_texto="Sites para clínicas e profissionais de saúde",
    h1="Sites para <em>clínicas e saúde</em>",
    resumo="Criamos sites para clínicas, consultórios, fisioterapia, nutrição e saúde ao domicílio em Portugal: transmitem confiança, explicam cada serviço com clareza e levam o paciente a marcar pelo WhatsApp ou formulário. Desde 300€.",
    corpo=sec("O que um paciente <em>precisa de ver</em>",
              "<ul class=\"lista-check\">"
              "<li><strong>Serviços e especialidades</strong> explicados em linguagem simples.</li>"
              "<li><strong>Equipa, formação e instalações</strong> com fotografia real.</li>"
              "<li><strong>Marcação a um toque</strong> por WhatsApp, telefone ou formulário.</li>"
              "<li><strong>Zona de atendimento</strong>, horários e acordos ou seguros aceites.</li>"
              "<li><strong>Perguntas frequentes</strong> que respondem às dúvidas antes da primeira consulta.</li>"
              "</ul>"
              "<p>Para clínicas dentárias temos uma página própria: <a href=\"/sites-para-clinicas-dentarias\">sites para clínicas dentárias</a>.</p>")
          + sec("Projetos <em>de saúde e bem-estar</em>", "<p>A Serena é um projeto conceito.</p>" + projetos(["gaspar", "funchal", "serena", "oralplus"]))
          + sec("Como <em>trabalhamos</em>", PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO),
    faq=[
        ("Quanto custa um site para uma clínica?", "Desde 300€. Clínicas com várias especialidades costumam precisar de mais páginas; numa conversa grátis de 15 minutos dizemos-te o valor exato."),
        ("Posso ligar o site ao meu sistema de marcações?", "Sim, se o sistema tiver ligação ou página de marcação online. Avaliamos contigo na conversa inicial."),
        ("Os dados dos pacientes ficam protegidos?", "O site usa ligação cifrada (HTTPS), formulários com consentimento e política de privacidade conforme o RGPD."),
        ("Fazem sites para saúde ao domicílio?", "Sim. A Clínica em Casa, no Funchal, é um dos nossos clientes de saúde ao domicílio."),
    ],
    chamada_titulo="Mais pacientes a <em>marcar pelo site</em>.",
    chamada_texto="Conversa grátis de 15 minutos: dizemos-te o que precisas, quanto custa e quando fica pronto.",
))

P.append(dict(
    caminho="/sites-para-restaurantes", tipo="servico", migalha="Sites para restaurantes",
    servico="Criação de sites para restaurantes, cafés e pastelarias",
    titulo="Sites para Restaurantes, Cafés e Pastelarias | Meta Designer",
    descricao="Criação de sites para restaurantes em Portugal: menu sempre atualizado, reservas por WhatsApp, fotos que dão fome e presença no Google Maps. Desde 300€.",
    etiqueta="Restauração", h1_texto="Sites para restaurantes",
    h1="Sites para <em>restaurantes</em>",
    resumo="Criamos sites para restaurantes, cafés e pastelarias em Portugal: menu fácil de atualizar, reservas por WhatsApp, fotografia que abre o apetite e ligação ao Google Maps. Desde 300€.",
    corpo=sec("O que quem procura <em>onde comer</em> quer ver",
              "<p>Quem pesquisa um restaurante quer saber três coisas, quase sempre no telemóvel: o que se come, quanto custa e se há mesa. Tudo o resto é secundário.</p>"
              "<ul class=\"lista-check\">"
              "<li><strong>Menu em texto</strong>, não em PDF: o Google lê-o e o cliente vê-o sem fazer zoom.</li>"
              "<li><strong>Reservas por WhatsApp</strong> ou ligação ao teu sistema de reservas.</li>"
              "<li><strong>Fotografia de impacto</strong> dos pratos e do espaço.</li>"
              "<li><strong>Horários, localização e estacionamento</strong> ligados ao Google Maps.</li>"
              "<li><strong>Versão em inglês</strong> para zonas turísticas.</li>"
              "</ul>")
          + sec("O nosso <em>portfólio</em>", "<p>Ainda não temos restaurantes no portfólio público. Estes são exemplos do nível de design e de detalhe que trazemos a cada projeto (a Serena é um projeto conceito).</p>" + projetos(["serena", "conecta", "amplify", "terraco"]))
          + sec("Como <em>trabalhamos</em>", PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO),
    faq=[
        ("Quanto custa um site para um restaurante?", "Desde 300€ para uma página com menu, galeria, horários e reservas. Dizemos-te o valor exato numa conversa grátis de 15 minutos."),
        ("Consigo atualizar o menu sozinho?", "Sim. Mostramos-te como, em 15 minutos."),
        ("O site pode receber reservas?", "Sim: por WhatsApp, por formulário ou com ligação ao sistema de reservas que já usas."),
        ("Vale a pena ter site se já estou no Instagram e no Google Maps?", "Sim. O site é o único canal que é teu, aparece nas pesquisas do Google e da IA e junta menu, reservas e contactos num só sítio."),
    ],
    chamada_titulo="Mais mesas cheias <em>a partir do Google</em>.",
    chamada_texto="Fala connosco: a conversa é grátis e sem compromisso.",
))

P.append(dict(
    caminho="/sites-para-alojamento-local", tipo="servico", migalha="Sites para alojamento local",
    servico="Criação de sites para alojamento local, guest houses e turismo rural",
    titulo="Sites para Alojamento Local e Guest Houses | Meta Designer",
    descricao="Criação de sites para alojamento local, guest houses e turismo rural em Portugal: reservas diretas, galeria de impacto, português e inglês. Desde 300€.",
    etiqueta="Turismo", h1_texto="Sites para alojamento local",
    h1="Sites para <em>alojamento local</em>",
    resumo="Criamos sites para alojamento local, guest houses e turismo rural em Portugal: galeria de impacto, reservas diretas por WhatsApp ou motor de reservas, e versão em português e inglês. Desde 300€.",
    corpo=sec("Mais <em>reservas diretas</em>",
              "<p>As plataformas de reservas trazem hóspedes, mas cobram comissão em cada estadia. Um site próprio dá-te um canal direto para quem já te conhece, para quem volta e para quem te encontra no Google.</p>"
              "<ul class=\"lista-check\">"
              "<li><strong>Galeria e vídeo</strong> que mostram a luz, a vista e os quartos.</li>"
              "<li><strong>Reserva direta</strong> por WhatsApp, formulário ou ligação ao teu motor de reservas.</li>"
              "<li><strong>Português e inglês</strong> para o público internacional.</li>"
              "<li><strong>O que fazer na zona</strong>, que responde a pesquisas e à IA.</li>"
              "<li><strong>Número de registo de AL</strong> visível, como a lei exige.</li>"
              "</ul>")
          + sec("Projetos <em>do portfólio</em>", "<p>A Residência Nevogilde é um projeto conceito.</p>" + projetos(["conecta", "nevogilde", "terraco", "amplify"]))
          + sec("Como <em>trabalhamos</em>", PROCESSO)
          + sec("O que vem <em>incluído</em>", INCLUIDO),
    faq=[
        ("Quanto custa um site para alojamento local?", "Desde 300€. Sites com várias unidades, motor de reservas ou várias línguas têm outro valor; dizemos-te qual numa conversa grátis."),
        ("O site pode ligar ao meu motor de reservas?", "Sim, se o teu motor tiver widget ou página de reserva. Avaliamos contigo na conversa inicial."),
        ("Faz sentido ter site se já estou no Booking e no Airbnb?", "Sim: o site traz reservas diretas sem comissão, sobretudo de hóspedes que voltam ou que te encontram no Google."),
        ("O site pode ter versão em inglês?", "Sim, e para alojamento local recomendamos."),
    ],
    chamada_titulo="Mais reservas, <em>menos comissões</em>.",
    chamada_texto="Conversa grátis de 15 minutos para veres o que um site pode fazer pelo teu alojamento.",
))


def main():
    for p in P:
        destino = SITE / (p["caminho"].strip("/") + ".html")
        destino.write_text(pagina(p), encoding="utf-8")
        print("ok", destino.name)
    # sitemap
    urls = [("/", "1.0", "monthly")] + [(p["caminho"], "0.8" if p["tipo"] == "servico" else "0.7", "monthly") for p in P] + [("/privacidade", "0.3", None), ("/termos", "0.3", None)]
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr, cf in urls:
        cfx = f"<changefreq>{cf}</changefreq>" if cf else ""
        linhas.append(f"  <url><loc>{DOMINIO}{u}</loc><lastmod>{HOJE}</lastmod>{cfx}<priority>{pr}</priority></url>")
    linhas.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("ok sitemap.xml", len(urls), "URLs")


if __name__ == "__main__":
    main()
