# Blue Hammer Remodeling — website completo (pré-lançamento)

> **Produção (Netlify) — leia primeiro.** O site publicado em https://bluehammermd.com é servido pelo Netlify a partir
> desta pasta (`netlify.toml` na raiz do repo). O formulário usa **Netlify Forms** (não o `server.mjs`).
> **As páginas HTML desta pasta são geradas**: edite os fragmentos em `../site-src/pages/*.html` e rode
> `python3 scripts/build.py --check` na raiz do repo. O script monta cabeçalho, navegação, rodapé, formulário,
> canonical/Open Graph, JSON-LD e `sitemap.xml` para todas as páginas de forma consistente. Não edite os HTML gerados à mão.
> Imagens: `python3 scripts/gen-image.py "<prompt>" <nome>` (chave OpenAI no Keychain). Registro de trabalho do agente: `AGENT-LOG.md`.

Este pacote contém **18 páginas HTML** em inglês, CSS responsivo, identidade visual azul escolhida, navegação mobile, SEO local de base, imagens de conceito de cozinha/banheiro/porão em WebP, otimizadas e hospedadas junto ao site, formulário de consulta em duas etapas, privacidade e um servidor Node.js sem dependências que **registra leads em arquivo privado**.

## Abrir / visualizar

1. Extraia o ZIP.
2. Em um computador com Node.js 20 ou superior, abra um terminal na pasta do site e execute `npm start` (ou `node server.mjs`).
3. Abra `http://127.0.0.1:4173`.

É possível abrir o arquivo `index.html` diretamente apenas para visualizar o layout; **o formulário não funciona nesse modo**. Ele precisa de um servidor com o endpoint `/api/leads`.

## Cadastro de leads

No servidor Node incluído, os formulários salvam nome, telefone, email, ZIP, serviço, prazo e mensagem em `data/leads.jsonl`, protegido de acesso pela web. O visitante recebe confirmação somente quando o servidor realmente salva o pedido.

Para receber alertas também no email comercial, configure estas variáveis de ambiente no servidor:

- `RESEND_API_KEY`: chave de API da conta Resend;
- `LEADS_TO_EMAIL`: caixa da Blue Hammer que receberá os avisos;
- `LEADS_FROM_EMAIL`: remetente autorizado no serviço de envio;
- `HOST=0.0.0.0` e `PORT=4173` em um servidor com HTTPS na frente.

Sem isso, **os leads são salvos localmente, mas não são enviados automaticamente por email**. Em hospedagens estáticas (por exemplo, apenas GitHub Pages), é necessário conectar um serviço de formulários ou hospedar o endpoint. Não ofereça o site ao público sem testar esse fluxo em ambiente de produção, backup e proteção de dados.

## Antes de publicar para clientes

1. Edite `assets/site-config.js` e adicione somente **telefone real, email comercial real e licença/MHIC real**, se aplicável. O site oculta campos que ainda não foram confirmados. Verifique seguro, licença e áreas atendidas antes de afirmar publicamente credenciais.
2. Substitua as imagens de inspiração pelas **fotos reais dos projetos da Blue Hammer**, com autorização quando necessário. As imagens atuais são ilustrativas; não são obras executadas pela empresa. Agora as 6 imagens de conceito são arquivos WebP locais em `assets/` (duas resoluções cada); o site não depende de Unsplash ou de conexão externa para exibi-las. As pessoas ilustradas na cena de consulta não são funcionários reais da Blue Hammer.
3. Depois de confirmar o domínio, execute `python configure-domain.py https://SEU-DOMINIO.com` para gerar `sitemap.xml`, atualizar `robots.txt` e adicionar URLs canônicas e Open Graph automaticamente.
4. Publique somente avaliações reais e verificáveis. O site **não inventa reviews, 5 estrelas, anos de experiência, números de licença, financiamento ou descontos**.
5. Revisar política de privacidade conforme a plataforma de hospedagem, retenção, pixels, analytics, emails e eventuais formulários externos. Uma revisão jurídica local pode ser apropriada.
6. Ative HTTPS, backups automáticos, proteção antispam, política de retenção e monitoramento do backend.
7. Conecte Search Console e Google Business Profile após domínio e dados comerciais confirmados.

## Conteúdo / arquitetura

- `index.html` — homepage com CTAs e formulário;
- `services.html` — visão geral;
- `kitchen-remodeling.html`, `bathroom-remodeling.html`, `basements-interiors.html` — páginas de serviço;
- `projects.html` — inspiração/galeria filtrável (somente fotos ilustrativas);
- `about.html`, `process.html`, `reviews.html` — confiança e processo;
- `service-areas.html` + páginas de área (Olney, Potomac, Bethesda, Chevy Chase, Kensington & Garrett Park, Rockville, Silver Spring, Howard County) — localização/SEO regional; `silver-spring-md.html` voltou a ser página ativa em 2026-11-19 (pedido do dono; sem redirect);
- `faq.html`, `contact.html`, `thank-you.html`, `privacy.html`, `terms.html`.

**Cores:** royal blue `#1E4FA3`, navy `#0B2347`, white `#FFFFFF` e tons neutros. A identidade do martelo + casa veio da direção visual escolhida anteriormente, como arte de pré-produção.

## Observações

Este é um site desenvolvido e navegável, pronto para avaliação técnica, não um site já hospedado publicamente. Os arquivos estão editáveis e podem ser enviados a um desenvolvedor ou serviço de hospedagem. Layout responsivo e fluxo do formulário devem ser retestados no ambiente final.

## Imagens inseridas nesta versão

- `hero-kitchen-*`: destaque principal e ambientes de cozinha
- `kitchen-design-*`: Kitchen Remodeling e inspirações de armários
- `bathroom-design-*`: Bathroom Remodeling e galeria
- `basement-design-*`: Basements & Interiors e galeria
- `consultation-scene-*`: About Us (cena ilustrativa, não equipe real)
- `design-gallery-collage-*`: cabeçalho da página Design Gallery (projects.html)

As imagens são **conceitos visuais gerados por IA**, não fotos de serviços executados. Cada imagem possui `srcset` WebP em 720 e 1440 pixels para celular e desktop. CSS e JS continuam sem frameworks externos.
