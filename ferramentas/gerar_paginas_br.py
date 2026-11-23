# Meta Designer · páginas de SEO do BRASIL (pt-BR, "você", sem preço), em /br/...
# Uso (na pasta site/):  python -I ferramentas/gerar_paginas_br.py
# Gera site/br/*.html e reescreve o sitemap.xml com as páginas de Portugal e do Brasil.
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gerar_paginas as pt  # noqa: E402  (reaproveita PROJ, projetos(), faq_html(), sec(), SVG e o sitemap)

SITE, DOMINIO, HOJE = pt.SITE, pt.DOMINIO, pt.HOJE
esc, sec, projetos, faq_html = pt.esc, pt.sec, pt.projetos, pt.faq_html
WHATS = "https://wa.me/5521966289500?text=" + "Ol%C3%A1!%20Vim%20pelo%20site%20e%20quero%20um%20or%C3%A7amento%20de%20site%20para%20a%20minha%20empresa."

PAGINAS_MENU_BR = [
    ("/br/criacao-de-sites-sao-paulo", "Criação de sites em São Paulo"),
    ("/br/criacao-de-sites-rio-de-janeiro", "Criação de sites no Rio de Janeiro"),
    ("/br/criacao-de-sites-belo-horizonte", "Criação de sites em Belo Horizonte"),
    ("/br/sites-para-dentistas", "Sites para dentistas"),
    ("/br/sites-para-advogados", "Sites para advogados"),
    ("/br/sites-para-clinicas-de-estetica", "Sites para clínicas de estética"),
]

PROCESSO = """
<div class="passos">
  <div class="passo"><b>01</b><h3>Desenhar</h3><p>Design exclusivo com as cores, as fontes e as animações da sua marca. Você aprova o layout antes de seguirmos.</p></div>
  <div class="passo"><b>02</b><h3>Construir</h3><p>Site rápido, seguro (SSL) e perfeito no celular. Um site de uma página fica no ar em 2 a 5 dias úteis depois que recebemos os conteúdos.</p></div>
  <div class="passo"><b>03</b><h3>Ser encontrado</h3><p>Estrutura, textos e dados estruturados para o Google e para os buscadores de IA (ChatGPT, Gemini e Perplexity), com integração ao Google Maps.</p></div>
</div>"""

INCLUIDO = """
<ul class="lista-check">
  <li><strong>Design exclusivo com animações</strong>, nada de modelo pronto.</li>
  <li><strong>Perfeito no celular</strong>, onde está a maior parte das visitas.</li>
  <li><strong>SEO e GEO incluídos</strong>: títulos, descrições, dados estruturados, velocidade e textos pensados para o Google e para a IA.</li>
  <li><strong>WhatsApp e formulário</strong> à vista em todas as seções.</li>
  <li><strong>LGPD</strong>: política de privacidade e controle de cookies.</li>
  <li><strong>Google Analytics</strong> e integração com o Google Maps e o Perfil da Empresa.</li>
  <li><strong>Atendimento humano</strong> e um treinamento de 15 minutos para você editar o site.</li>
</ul>"""


BR = dict(pt.PT,
    lang="pt-BR", locale="pt_BR", inicio="/br", whats=WHATS, cta="Falar no WhatsApp", pular="Pular para o conteúdo",
    menu=[("/br#portfolio", "Projetos"), ("/br#metodo", "Método"), ("/br#designer", "Designer"), ("/br#duvidas", "Dúvidas")],
    paginas=PAGINAS_MENU_BR, paginas_titulo="Sites por cidade e setor:",
    navegacao=[("/br", "Início"), ("/br#portfolio", "Portfólio"), ("/br#metodo", "Como funciona"), ("/br#designer", "Designer"), ("/br#duvidas", "Dúvidas")],
    contacto=["Rio de Janeiro, RJ", "Atendimento em todo o Brasil", "Online, por vídeo e WhatsApp"],
    legais=[("/br/privacidade", "Privacidade"), ("/br/termos", "Termos")], outro=("/", "pt-PT", "Portugal"),
    copy="© 2026 Meta Designer · Estúdio de web design no Rio de Janeiro, atendendo todo o Brasil",
    flutuante=("Atendimento personalizado", "Fale com o Mike"), whats_label="Falar com o Mike no WhatsApp",
    ver_projetos="Ver projetos", inicio_nome="Início",
)


def chamada(titulo, texto):
    return f'''<section class="chamada">
  <h2>{titulo}</h2>
  <p>{texto}</p>
  <div class="botoes"><a class="btn-wa" href="{WHATS}" target="_blank" rel="noopener">{pt.SVG_WA}Pedir orçamento pelo WhatsApp</a></div>
  <p class="nota">Abre o WhatsApp direto, sem preencher nada.</p>
</section>'''


def relacionados(atual):
    links = "".join(f'<a href="{u}">{esc(n)}</a>' for u, n in PAGINAS_MENU_BR if u != atual)
    return f'<section class="bloco"><div class="cartao"><h2>Veja <em>também</em></h2><div class="relacionados">{links}<a href="/br#portfolio">Ver todos os projetos</a></div></div></section>'


def pagina(p):
    url = DOMINIO + p["caminho"]
    texto_faq = [(q, html.unescape(re.sub("<[^>]+>", "", a))) for q, a in p.get("faq", [])]
    grafo = [
        {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": p["titulo"], "description": p["descricao"],
         "inLanguage": "pt-BR", "isPartOf": {"@id": DOMINIO + "/#website"}, "about": {"@id": DOMINIO + "/#organizacao"},
         "dateModified": HOJE, "breadcrumb": {"@id": url + "#migalhas"}},
        {"@type": "BreadcrumbList", "@id": url + "#migalhas", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/br"},
            {"@type": "ListItem", "position": 2, "name": p["migalha"], "item": url}]},
    ]
    if texto_faq:
        grafo.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in texto_faq]})
    if p["tipo"] == "servico":
        grafo.append({"@type": "Service", "@id": url + "#servico", "name": p["servico"], "serviceType": "Criação de sites",
                      "url": url, "provider": {"@id": DOMINIO + "/#organizacao"},
                      "areaServed": p.get("area", {"@type": "Country", "name": "Brasil"})})
    ld = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False)
    if p["tipo"] == "legal":
        return pt.montar(BR, p, url, ld, "", "")
    p = dict(p, cta="Pedir orçamento pelo WhatsApp")
    return pt.montar(BR, p, url, ld, chamada(p["chamada_titulo"], p["chamada_texto"]), relacionados(p["caminho"]))


FAQ_BASE = [
    ("Vocês atendem presencialmente?", "Não. O atendimento é 100% online, por WhatsApp, videochamada e e-mail, o que deixa o processo mais rápido e sem deslocamento. O estúdio fica no Rio de Janeiro e atende empresas de todo o Brasil."),
    ("Em quanto tempo o site fica pronto?", "Um site de uma página fica no ar em 2 a 5 dias úteis depois que recebemos os conteúdos. Sites maiores dependem do tamanho e da estrutura, e o prazo fica combinado antes de começar."),
    ("Como funciona o pagamento?", "Você paga 50% para começar e os outros 50% só depois de aprovar a última etapa, com o site pronto."),
]


def cidade(caminho, nome, prep, uf, intro, contexto, bairros, proj):
    return dict(
        caminho=caminho, tipo="servico", migalha=f"Criação de sites {prep} {nome}",
        servico=f"Criação de sites {prep} {nome}",
        area={"@type": "City", "name": nome, "containedInPlace": {"@type": "State", "name": uf}},
        titulo=f"Criação de Sites {prep} {nome} | Meta Designer",
        descricao=f"Criação de sites profissionais para empresas {prep} {nome}: design exclusivo com animações, rápido no celular e pronto para o Google e o ChatGPT. Orçamento pelo WhatsApp.",
        etiqueta=f"Web design · {nome}", h1=f"Criação de sites <em>{prep} {nome}</em>",
        resumo=intro,
        corpo=sec(f"Um site feito para <em>competir {prep} {nome}</em>", contexto
                  + f"<h3>Busca local {prep} {nome}</h3><p>Integramos o site ao seu Perfil da Empresa no Google e escrevemos os textos citando a sua região de atendimento (por exemplo {bairros}), para o Google entender onde você está e a quem atende.</p>")
              + sec("Como <em>funciona</em>", "<p>Tudo online, por WhatsApp e videochamada. Você não precisa se deslocar e aprova cada etapa no seu tempo.</p>" + PROCESSO)
              + sec("O que vem <em>incluído</em>", INCLUIDO)
              + sec("Projetos <em>do portfólio</em>", "<p>Alguns trabalhos recentes. Os projetos conceito estão identificados.</p>" + projetos(proj)),
        faq=[
            (f"Quanto custa um site {prep} {nome}?", "Depende do número de páginas e das funcionalidades. Numa conversa grátis pelo WhatsApp entendemos o que a sua empresa precisa e passamos o valor exato, sem compromisso."),
            (f"O site vai aparecer no Google {prep} {nome}?", "O site sai pronto para competir: estrutura, velocidade, textos e dados estruturados otimizados, além da integração com o Google Maps. Ninguém pode garantir a primeira posição, mas o seu site entra na disputa com a base certa."),
        ] + FAQ_BASE,
        chamada_titulo=f"Sua empresa {prep} {nome}, <em>em destaque</em>.",
        chamada_texto="Conversa grátis pelo WhatsApp: dizemos o que você precisa, quanto custa e quando fica pronto.",
    )


P_BR = [
    cidade("/br/criacao-de-sites-sao-paulo", "São Paulo", "em", "São Paulo",
           "A Meta Designer cria sites profissionais para empresas de São Paulo e da Grande São Paulo: design exclusivo com animações, rápido no celular e preparado para aparecer no Google e nas respostas do ChatGPT. Atendimento 100% online, com orçamento sem compromisso pelo WhatsApp.",
           "<p>São Paulo é o mercado mais disputado do país. Em quase todo segmento existem centenas de empresas brigando pela mesma busca: clínicas, escritórios, restaurantes, imobiliárias, estúdios. Quem aparece primeiro e passa mais confiança nos primeiros segundos fica com o contato.</p>"
           "<p>Por isso cada site começa pelo que o cliente procura (o serviço, o bairro, a urgência) e só depois vai para o design. O resultado é um site que impressiona e que responde de forma clara a quem pesquisa “perto de mim” no celular.</p>",
           "Pinheiros, Vila Mariana, Moema, Itaim Bibi, Santana, Tatuapé ou o ABC", ["seo", "dentix", "legatus", "terraco"]),
    cidade("/br/criacao-de-sites-rio-de-janeiro", "Rio de Janeiro", "no", "Rio de Janeiro",
           "A Meta Designer é um estúdio do Rio de Janeiro que cria sites profissionais para empresas cariocas e de todo o estado: design exclusivo com animações, rápido no celular e pronto para o Google e para o ChatGPT. Orçamento sem compromisso pelo WhatsApp.",
           "<p>No Rio, boa parte dos clientes chega pelo celular, entre uma praia e o trabalho, procurando alguém perto e de confiança. Um site lento ou confuso perde esse cliente para o concorrente da rua de baixo.</p>"
           "<p>Somos do Rio e conhecemos a forma como o carioca pesquisa: por bairro, por indicação e cada vez mais perguntando para a inteligência artificial. O site é pensado para responder a essas três frentes.</p>",
           "Barra da Tijuca, Recreio, Copacabana, Botafogo, Tijuca, Niterói ou a Baixada", ["nacar", "terraco", "amplify", "conecta"]),
    cidade("/br/criacao-de-sites-belo-horizonte", "Belo Horizonte", "em", "Minas Gerais",
           "A Meta Designer cria sites profissionais para empresas de Belo Horizonte e da região metropolitana: design exclusivo com animações, rápido no celular e preparado para aparecer no Google e no ChatGPT. Atendimento online e orçamento pelo WhatsApp.",
           "<p>Belo Horizonte tem um mercado de serviços forte e exigente, em especial saúde, advocacia, gastronomia e construção. O cliente mineiro pesquisa, compara e só depois entra em contato: o site precisa explicar bem e transmitir segurança.</p>"
           "<p>Por isso trabalhamos textos claros, prova do seu trabalho (fotos, casos, avaliações) e um caminho direto para o WhatsApp, sem formulário longo nem página confusa.</p>",
           "Savassi, Lourdes, Funcionários, Pampulha, Buritis ou Contagem e Nova Lima", ["bica", "legatus", "oralplus", "serena"]),
    dict(
        caminho="/br/sites-para-dentistas", tipo="servico", migalha="Sites para dentistas",
        servico="Criação de sites para dentistas e clínicas odontológicas",
        titulo="Sites para Dentistas e Clínicas Odontológicas | Meta Designer",
        descricao="Criação de sites para dentistas e clínicas odontológicas: agendamento pelo WhatsApp, tratamentos bem explicados, pronto para o Google e o ChatGPT e dentro das regras do CFO.",
        etiqueta="Odontologia", h1="Sites para <em>dentistas</em>",
        resumo="Criamos sites para dentistas e clínicas odontológicas que transmitem confiança, explicam cada tratamento e levam o paciente direto para o agendamento pelo WhatsApp. Prontos para o Google, para o ChatGPT e dentro das regras de publicidade do CFO.",
        corpo=sec("O que um bom site de <em>odontologia</em> precisa ter",
                  "<ul class=\"lista-check\">"
                  "<li><strong>Uma página por tratamento</strong> (implantes, lentes, ortodontia, clareamento), que responde às buscas e às perguntas feitas à IA.</li>"
                  "<li><strong>Agendamento em um toque</strong> pelo WhatsApp, à vista em todas as seções.</li>"
                  "<li><strong>Equipe com CRO</strong>, estrutura da clínica e convênios aceitos.</li>"
                  "<li><strong>Localização e horários</strong> integrados ao Google Maps.</li>"
                  "<li><strong>Textos dentro das regras do CFO</strong>: sem promessa de resultado e com responsável técnico identificado.</li>"
                  "</ul>")
              + sec("Projetos <em>de odontologia</em>", "<p>O Nácar é um projeto conceito.</p>" + projetos(["dentix", "oralplus", "nacar", "bica"]))
              + sec("Como <em>funciona</em>", PROCESSO)
              + sec("O que vem <em>incluído</em>", INCLUIDO),
        faq=[
            ("Quanto custa um site para dentista?", "Depende do número de páginas e de tratamentos. Numa conversa grátis pelo WhatsApp passamos o valor exato, sem compromisso."),
            ("O site segue as regras de publicidade do CFO?", "Sim. Os textos não prometem resultados, mostram o responsável técnico com CRO e evitam o que o Código de Ética Odontológica não permite. A revisão final do conteúdo clínico é sempre do dentista."),
            ("Posso mostrar fotos de antes e depois?", "As regras do CFO sobre antes e depois são restritas. Avaliamos o seu caso e sugerimos alternativas, como fotos da clínica, da equipe e explicações dos tratamentos."),
        ] + FAQ_BASE,
        chamada_titulo="Mais pacientes <em>chegando pelo Google</em>.",
        chamada_texto="Conversa grátis pelo WhatsApp, sem compromisso.",
    ),
    dict(
        caminho="/br/sites-para-advogados", tipo="servico", migalha="Sites para advogados",
        servico="Criação de sites para advogados e escritórios de advocacia",
        titulo="Sites para Advogados e Escritórios de Advocacia | Meta Designer",
        descricao="Criação de sites para advogados e escritórios de advocacia: áreas de atuação bem explicadas, contato pelo WhatsApp e textos dentro do Provimento 205/2021 da OAB.",
        etiqueta="Advocacia", h1="Sites para <em>advogados</em>",
        resumo="Criamos sites para advogados e escritórios que passam autoridade, explicam cada área de atuação em linguagem clara e facilitam o primeiro contato pelo WhatsApp, respeitando as regras de publicidade da OAB.",
        corpo=sec("Autoridade <em>sem exagero</em>",
                  "<p>Quem procura um advogado está, quase sempre, preocupado. Um site sério, rápido e fácil de entender é o primeiro sinal de que vale a pena conversar com você.</p>"
                  "<ul class=\"lista-check\">"
                  "<li><strong>Uma página por área de atuação</strong> (trabalhista, família, previdenciário, empresarial), escrita para quem não é da área.</li>"
                  "<li><strong>Perfil dos advogados</strong> com número da OAB e formação.</li>"
                  "<li><strong>Artigos e perguntas frequentes</strong>, que respondem às buscas e às perguntas feitas ao ChatGPT.</li>"
                  "<li><strong>Contato discreto</strong> pelo WhatsApp ou formulário.</li>"
                  "<li><strong>Dentro do Provimento 205/2021 da OAB</strong>: publicidade informativa, sem captação indevida nem promessa de resultado.</li>"
                  "</ul>")
              + sec("Projetos <em>do portfólio</em>", projetos(["legatus", "seo", "terraco", "amplify"]))
              + sec("Como <em>funciona</em>", PROCESSO)
              + sec("O que vem <em>incluído</em>", INCLUIDO),
        faq=[
            ("Quanto custa um site para escritório de advocacia?", "Depende do número de páginas e de áreas de atuação. Numa conversa grátis pelo WhatsApp passamos o valor exato, sem compromisso."),
            ("O site respeita as regras da OAB?", "Sim. Seguimos o Provimento 205/2021: conteúdo informativo, sem promessa de resultado, sem menção a valores e sem captação indevida de clientela. A revisão final é sempre do advogado responsável."),
            ("Vale a pena ter um blog jurídico?", "Sim. Artigos que respondem dúvidas comuns são uma das melhores formas de aparecer no Google e de ser citado pelas ferramentas de IA."),
        ] + FAQ_BASE,
        chamada_titulo="Mais consultas <em>a partir do Google</em>.",
        chamada_texto="Conversa grátis pelo WhatsApp, sem compromisso.",
    ),
    dict(
        caminho="/br/sites-para-clinicas-de-estetica", tipo="servico", migalha="Sites para clínicas de estética",
        servico="Criação de sites para clínicas de estética e harmonização",
        titulo="Sites para Clínicas de Estética e Harmonização | Meta Designer",
        descricao="Criação de sites para clínicas de estética, harmonização facial e biomedicina: visual premium, procedimentos bem explicados e agendamento pelo WhatsApp.",
        etiqueta="Estética", h1="Sites para <em>clínicas de estética</em>",
        resumo="Criamos sites para clínicas de estética, harmonização facial e biomedicina com visual à altura do seu atendimento: procedimentos bem explicados, galeria do espaço e agendamento direto pelo WhatsApp.",
        corpo=sec("Um site <em>tão cuidado quanto a sua clínica</em>",
                  "<p>Na estética, a primeira impressão decide. O paciente compara o Instagram, o site e as avaliações antes de chamar. Um site com cara de modelo pronto passa a mensagem errada.</p>"
                  "<ul class=\"lista-check\">"
                  "<li><strong>Visual premium com animações</strong>, alinhado à identidade da clínica.</li>"
                  "<li><strong>Uma página por procedimento</strong>, com indicações, cuidados e perguntas frequentes.</li>"
                  "<li><strong>Agendamento pelo WhatsApp</strong> em um toque.</li>"
                  "<li><strong>Integração com o Instagram</strong> e com o Google Maps.</li>"
                  "<li><strong>Responsável técnico identificado</strong> e textos sem promessa de resultado, como pedem os conselhos profissionais.</li>"
                  "</ul>")
              + sec("Projetos <em>do portfólio</em>", "<p>A Serena é um projeto conceito.</p>" + projetos(["serena", "nacar", "oralplus", "funchal"]))
              + sec("Como <em>funciona</em>", PROCESSO)
              + sec("O que vem <em>incluído</em>", INCLUIDO),
        faq=[
            ("Quanto custa um site para clínica de estética?", "Depende do número de páginas e de procedimentos. Numa conversa grátis pelo WhatsApp passamos o valor exato, sem compromisso."),
            ("Já tenho Instagram. Preciso de site?", "Sim. O Instagram não aparece bem no Google nem nas respostas do ChatGPT, e você não controla o algoritmo. O site é o lugar onde o paciente confirma a confiança e agenda."),
            ("O site segue as regras dos conselhos (CFM, CFBM, CFO)?", "Os textos evitam promessa de resultado e identificam o responsável técnico. A revisão final do conteúdo é sempre da clínica."),
        ] + FAQ_BASE,
        chamada_titulo="Mais agendamentos <em>a partir do Google</em>.",
        chamada_texto="Conversa grátis pelo WhatsApp, sem compromisso.",
    ),
]

PRIVACIDADE = """
<h1>Política de Privacidade</h1>
<p class="nota">Última atualização: 19 de novembro de 2026. Versão-base, a ser revisada por um advogado antes da versão definitiva.</p>
<h2>1. Quem é o controlador dos seus dados</h2>
<p>Agência de Publicidade e Marketing Digital Meta Design Ltda. (Meta Designer), CNPJ 38.284.190/0001-99, Rio de Janeiro, RJ. Para qualquer questão sobre dados pessoais, fale com a gente pelo e-mail <a href="mailto:mike.polettiaarte@gmail.com">mike.polettiaarte@gmail.com</a>.</p>
<h2>2. Quais dados coletamos</h2>
<ul><li>Dados que você envia pelo formulário: nome, WhatsApp, ramo da empresa e se já tem site.</li>
<li>Dados que você envia pelo WhatsApp ou por e-mail, quando fala com a gente por esses canais.</li>
<li>Dados de navegação, apenas se você aceitar cookies de estatística ou de marketing (veja o item 7).</li></ul>
<h2>3. Para que usamos os dados</h2>
<ul><li>Responder ao seu pedido de contato e de orçamento.</li>
<li>Preparar e enviar propostas e, se você contratar, prestar o serviço e emitir os documentos fiscais.</li>
<li>Melhorar o site e medir nossos anúncios, com base em estatísticas, se você autorizar.</li></ul>
<h2>4. Bases legais (LGPD)</h2>
<p>Tratamos os dados com base no seu consentimento (formulário e cookies não essenciais), na execução de procedimentos preliminares a um contrato que você pediu (orçamento e proposta) e no cumprimento de obrigação legal ou regulatória (documentos fiscais), conforme o artigo 7º da Lei Geral de Proteção de Dados (Lei nº 13.709/2018).</p>
<h2>5. Com quem compartilhamos</h2>
<p>Não vendemos dados. Usamos fornecedores que tratam dados em nosso nome: o serviço de envio do formulário (FormSubmit ou Web3Forms), o e-mail, o WhatsApp, a hospedagem do site (Cloudflare) e, com o seu consentimento, o Google Analytics, o Google Ads e o Meta Pixel. Alguns desses fornecedores podem tratar dados fora do Brasil, com as garantias previstas nos artigos 33 e seguintes da LGPD.</p>
<h2>6. Por quanto tempo guardamos</h2>
<ul><li>Pedidos de contato que não viram contrato: até 12 meses.</li>
<li>Dados de clientes: durante a relação comercial e pelo prazo exigido pela legislação fiscal.</li></ul>
<h2 id="cookies">7. Cookies</h2>
<p>Usamos cookies e armazenamento local essenciais para o site funcionar e para guardar a sua escolha sobre cookies. Cookies de estatística (Google Analytics) e de marketing (Google Ads e Meta Pixel, do Facebook e do Instagram, para medir se nossos anúncios trazem contatos) só são ativados se você clicar em "Aceitar" ou escolher em "Personalizar".</p>
<p>Com o consentimento de marketing, nosso servidor também envia à Meta os mesmos eventos (visita, contato pelo WhatsApp e envio do formulário), com o endereço IP, o navegador e o identificador do cookie da Meta, para medir os anúncios com precisão. Nosso servidor não envia o seu nome nem o seu número. O Pixel da Meta pode usar a correspondência avançada automática, que envia à Meta, de forma criptografada (hash), dados de contato preenchidos no site para associar o evento a uma conta da Meta.</p>
<p>Você pode mudar a sua escolha a qualquer momento no link "Preferências de cookies", no rodapé da <a href="/br">página inicial</a>.</p>
<h2>8. Seus direitos</h2>
<p>Pelo e-mail acima, você pode pedir a confirmação do tratamento, o acesso, a correção, a anonimização, o bloqueio ou a eliminação dos seus dados, a portabilidade, informações sobre o compartilhamento e a revogação do consentimento, conforme o artigo 18 da LGPD. Você também pode apresentar reclamação à Autoridade Nacional de Proteção de Dados (<a href="https://www.gov.br/anpd" target="_blank" rel="noopener">ANPD</a>).</p>
<h2>9. Segurança</h2>
<p>O site usa conexão criptografada (HTTPS) e adotamos medidas razoáveis para proteger os dados contra acesso não autorizado.</p>
<h2>10. Alterações</h2>
<p>Podemos atualizar esta política. A versão em vigor é sempre a publicada nesta página.</p>
"""

TERMOS = """
<h1>Termos de Uso</h1>
<p class="nota">Última atualização: 19 de novembro de 2026. Versão-base, a ser revisada por um advogado antes da versão definitiva.</p>
<h2>1. Identificação</h2>
<p>Este site pertence à Agência de Publicidade e Marketing Digital Meta Design Ltda. (Meta Designer), CNPJ 38.284.190/0001-99, Rio de Janeiro, RJ. Contato: <a href="mailto:mike.polettiaarte@gmail.com">mike.polettiaarte@gmail.com</a>.</p>
<h2>2. Objeto</h2>
<p>Estes termos regulam o uso do site e o pedido de orçamentos para criação de sites. A contratação de um serviço é sempre formalizada por proposta escrita, com escopo, valor, prazos e condições de pagamento.</p>
<h2>3. Valores e pagamento</h2>
<p>O site não divulga preços: o valor depende do tamanho e da estrutura de cada projeto e é apresentado na proposta. O pagamento é feito em duas partes: 50% na aprovação da proposta, para iniciar o projeto, e 50% após a aprovação da última etapa pelo cliente, antes da publicação final.</p>
<h2>4. Prazos</h2>
<p>Os prazos indicados (por exemplo, 2 a 5 dias úteis para um site de uma página) contam a partir do recebimento de todos os conteúdos e da aprovação da proposta, e podem variar conforme a complexidade do projeto.</p>
<h2>5. Resultados nos buscadores</h2>
<p>Preparamos os sites para competir nas buscas do Google e nos buscadores de IA. Não garantimos posições específicas, porque elas dependem de fatores fora do nosso controle.</p>
<h2>6. Propriedade intelectual</h2>
<p>O conteúdo deste site (textos, imagens, logotipo e código) pertence à Meta Designer ou aos respectivos titulares. As imagens de projetos são exibidas como portfólio. A titularidade dos sites desenvolvidos para clientes é definida na proposta.</p>
<h2>7. Responsabilidade</h2>
<p>Fazemos o possível para manter o site disponível e as informações corretas, mas não garantimos que estejam sempre livres de erros ou interrupções.</p>
<h2>8. Direitos do consumidor e foro</h2>
<p>Se você for consumidor, valem os direitos previstos no Código de Defesa do Consumidor. Em caso de reclamação, fale primeiro com a gente pelo e-mail acima: buscamos sempre uma solução amigável. Fica eleito o foro da comarca do Rio de Janeiro/RJ, ressalvado o foro do domicílio do consumidor.</p>
<h2>9. Alterações</h2>
<p>Podemos atualizar estes termos. A versão em vigor é sempre a publicada nesta página.</p>
"""

P_LEGAL = [
    dict(caminho="/br/privacidade", tipo="legal", migalha="Política de Privacidade", titulo="Política de Privacidade | Meta Designer Brasil",
         descricao="Como a Meta Designer trata os dados pessoais de quem visita o site e pede orçamento no Brasil, conforme a LGPD.", corpo=PRIVACIDADE),
    dict(caminho="/br/termos", tipo="legal", migalha="Termos de Uso", titulo="Termos de Uso | Meta Designer Brasil",
         descricao="Termos de uso do site e condições gerais para orçamentos de criação de sites no Brasil.", corpo=TERMOS),
]


def main():
    (SITE / "br").mkdir(exist_ok=True)
    for p in P_BR + P_LEGAL:
        destino = SITE / (p["caminho"].strip("/") + ".html")
        destino.write_text(pagina(p), encoding="utf-8")
        print("ok", destino.relative_to(SITE))
    pt.escrever_sitemap()


if __name__ == "__main__":
    main()
