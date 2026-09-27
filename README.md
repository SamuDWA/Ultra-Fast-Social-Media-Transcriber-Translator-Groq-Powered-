# ⚡ Ultra-Fast Social Media Transcriber & Translator (Groq Powered)

[English description below / Descrição em português abaixo]

---

## 🇺🇸 ENGLISH

Professional Skill developed for content creators, marketing agencies, and media professionals who need maximum speed in extracting and translating international content.

### ✨ Business Highlights
* **Record Speed:** Full processing in under 10 seconds leveraging **Groq API's** ultra-fast infrastructure (Whisper-large-v3 + Qwen).
* **Smart Translation:** Keeps brand names, software, and technical terms capitalized correctly in their original language while accurately translating the context.
* **Ready Export:** Automatically generates a high-quality, structured **PDF** report ready for download.

### 📥 Input Parameters (JSON)
```json
{
  "url": "https://instagram.com...",
  "idioma": "English"
}
```

### 📤 Output Parameters (JSON)
```json
{
  "sucesso": true,
  "transcricao": "Translated and reviewed content here...",
  "url_pdf": "/download/transcricao_17123456.pdf"
}
```

---

## 🇧🇷 PORTUGUÊS

Skill profissional desenvolvida para criadores de conteúdo, agências de marketing e profissionais de mídia que precisam de máxima velocidade na extração e tradução de conteúdo internacional.

### ✨ Diferenciais Comerciais
* **Velocidade Recorde:** Processamento completo em menos de 10 segundos utilizando a infraestrutura ultra-rápida da **Groq API** (Whisper-large-v3 + Qwen).
* **Tradução Inteligente:** Mantém nomes de marcas, softwares e termos técnicos com a capitalização correta no idioma original, traduzindo com precisão o restante do contexto para o idioma escolhido.
* **Exportação Pronta:** Gera um relatório executivo estruturado em formato **PDF** de alta qualidade pronto para download.

### 📥 Parâmetros de Entrada (Input JSON)
```json
{
  "url": "https://instagram.com...",
  "idioma": "Português do Brasil"
}
```

### 📤 Parâmetros de Saída (Output JSON)
```json
{
  "sucesso": true,
  "transcricao": "Conteúdo traduzido e revisado aqui...",
  "url_pdf": "/download/transcricao_17123456.pdf"
}
```