window.SITE = {
  nome: "Meta Designer",

  whatsapp: {
    numero: "5521966289500", // só dígitos, com DDI
    mensagem: "Olá! Quero saber mais sobre um site para o meu negócio.",
  },

  contato: {
    email: "mike.polettiaarte@gmail.com",
    // Opcional: chave do Web3Forms (https://web3forms.com). Se vazio, usa FormSubmit.
    web3formsChave: "",
    assunto: "Novo contacto pelo site Meta Designer",
  },

  // ID do Google Analytics 4 (ex.: "G-XXXXXXX"). Só carrega depois de o visitante aceitar cookies de estatística.
  // Propriedade GA4 "Contacto" (conta Agencia Meta Designer), ligada ao Google Ads "Mike o Design".
  analytics: "G-W6BKJHF1BF",

  // Nomes dos eventos GA4. Têm de ser EXATAMENTE estes: o Google Ads importa-os como conversões principais
  // ("Contacto (web) whatsapp_click" e "Contacto (web) conato_click"). Não corrigir a grafia de "conato".
  eventosGA4: { formulario: "conato_click", whatsapp: "whatsapp_click" },

  // Google Ads (opcional): só é preciso se criares conversões nativas do Ads em vez das importadas do GA4.
  // ID da conta (ex.: "AW-123456789") e o rótulo de cada conversão (a parte depois da "/" no "send_to").
  googleAds: {
    id: "",
    conversoes: { formulario: "", whatsapp: "" },
  },

  // Meta (Facebook/Instagram) Pixel. Só carrega com consentimento de marketing.
  // Eventos: PageView, Lead (formulário enviado) e Contact (clique no WhatsApp).
  // NUNCA colocar aqui o token da API de Conversões: este ficheiro é público.
  metaPixel: "1163218391923665",


  // Telas 3D do hero (a do meio é a principal). "longo" = screenshot de página inteira que rola dentro da tela.
  telas: [
    // no telemóvel aparecem só as posições 1, 3 e 5 (Nevogilde, Serena, Nácar)
    // "link" = site publicado (referência; as telas do hero não são clicáveis)
    { img: "assets/projetos/dentix.webp", nome: "Dentix", setor: "Implantologia", url: "dentix" },
    { img: "assets/projetos/nevogilde-longo.webp", nome: "Residência Nevogilde", setor: "Imobiliário · Porto", url: "residencia-nevogilde", longo: true, link: "https://mkpoletti.github.io/residencia-nevogilde/" },
    { img: "assets/projetos/santa-zita-longo.webp", nome: "Santa Zita", setor: "Medicina dentária", url: "clinicasantazita.pt", longo: true },
    { img: "assets/projetos/serena-longo.webp", nome: "Serena", setor: "Bem-estar e nutrição", url: "serena", longo: true, link: "https://mkpoletti.github.io/serena-landing/" },
    { img: "assets/projetos/terraco-nobre.webp", nome: "Terraço Nobre", setor: "Imobiliário", url: "terraconobre" },
    { img: "assets/projetos/nacar-longo.webp", nome: "Nácar", setor: "Medicina dentária · Lisboa", url: "nacar", longo: true, link: "https://mkpoletti.github.io/nacar-site/" },
    { img: "assets/projetos/legatus.webp", nome: "Legatus", setor: "Advocacia", url: "legatus" },
  ],
};
