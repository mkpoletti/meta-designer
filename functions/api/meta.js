// Cloudflare Pages Function: POST /api/meta
// Envia eventos para a API de Conversões da Meta (servidor → Meta), em paralelo com o Pixel do browser.
// A Meta junta os dois pelo event_id, por isso o mesmo evento não é contado duas vezes.
//
// Variáveis no painel da Cloudflare (Pages → metadesigner → Settings → Variables and Secrets):
//   META_CAPI_TOKEN   (Secret, obrigatório) token da API de Conversões, gerado no Gerenciador de Eventos
//   META_PIXEL_ID     (opcional) por defeito 1163218391923665
//   META_TEST_CODE    (opcional) código "Testar eventos" do Gerenciador de Eventos; apagar depois de testar
//   META_API_VERSION  (opcional) por defeito v24.0
//
// O token nunca vai para o browser nem para o GitHub: vive só nas variáveis da Cloudflare.

const EVENTOS = new Set(["PageView", "Lead", "Contact"]);
const ORIGENS = ["https://metadesigner.site", "https://www.metadesigner.site"];

export async function onRequestPost({ request, env }) {
  const token = env.META_CAPI_TOKEN;
  if (!token) return new Response(null, { status: 204 }); // ainda não configurado: não faz nada

  // Só aceita pedidos vindos do próprio site
  const origem = request.headers.get("Origin") || "";
  const referer = request.headers.get("Referer") || "";
  if (!ORIGENS.includes(origem) && !ORIGENS.some((o) => referer.startsWith(o + "/"))) return new Response(null, { status: 403 });

  let corpo;
  try {
    corpo = await request.json();
  } catch {
    return new Response(null, { status: 400 });
  }

  const { event_name, event_id, event_source_url, fbp, fbc } = corpo || {};
  if (!EVENTOS.has(event_name) || typeof event_id !== "string" || event_id.length > 64) {
    return new Response(null, { status: 400 });
  }
  const url = typeof event_source_url === "string" && ORIGENS.some((o) => event_source_url.startsWith(o)) ? event_source_url : ORIGENS[0] + "/";

  const user_data = {
    client_ip_address: request.headers.get("CF-Connecting-IP") || undefined,
    client_user_agent: request.headers.get("User-Agent") || undefined,
  };
  if (typeof fbp === "string" && /^fb\.\d\.\d+\.\d+$/.test(fbp)) user_data.fbp = fbp;
  if (typeof fbc === "string" && /^fb\.\d\.\d+\.[\w-]+$/.test(fbc)) user_data.fbc = fbc;

  const payload = {
    data: [{
      event_name,
      event_id,
      event_time: Math.floor(Date.now() / 1000),
      action_source: "website",
      event_source_url: url,
      user_data,
    }],
  };
  if (env.META_TEST_CODE) payload.test_event_code = env.META_TEST_CODE;

  const pixel = env.META_PIXEL_ID || "1163218391923665";
  const versao = env.META_API_VERSION || "v24.0";
  const r = await fetch(`https://graph.facebook.com/${versao}/${pixel}/events?access_token=${encodeURIComponent(token)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) console.warn("Meta CAPI", r.status, await r.text());
  return new Response(null, { status: r.ok ? 204 : 502 });
}
