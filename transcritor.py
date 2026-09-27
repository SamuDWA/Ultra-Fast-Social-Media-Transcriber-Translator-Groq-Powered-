import os
import time
from groq import Groq
import yt_dlp
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def traduzir_texto(texto_original, idioma_destino):
    try:
        system_instruction = (
            f"Você é um tradutor automático avançado e revisor gramatical. Sua tarefa é traduzir textos para o {idioma_destino}.\n"
            "Siga rigorosamente estas duas regras:\n"
            "1. IDENTIFICAÇÃO E CAPITALIZAÇÃO: Identifique todos os nomes próprios, marcas, softwares, empresas, sites e ferramentas. "
            "Garanta que a primeira letra de cada palavra desses nomes seja estritamente MAIÚSCULA (ex: mude 'web explorer' para 'Web Explorer', "
            "'instagram' para 'Instagram', 'linux' para 'Linux').\n"
            "2. PRESERVAÇÃO: NÃO traduza nenhum desses nomes próprios ou marcas. Mantenha-os exatamente no idioma original, apenas corrigindo as maiúsculas.\n"
            "Retorne APENAS o texto final traduzido e corrigido. Não adicione nenhuma introdução, explicação ou comentário."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Traduza e aplique as iniciais maiúsculas neste texto:\n\n{texto_original}"}
            ],
            model="qwen/qwen3.8-27b", 
            temperature=0.1,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Erro na tradução: {e}. Mantendo o original.")
        return texto_original

def exportar_tudo_para_pdf(url, texto, nome_arquivo):
    try:
        os.makedirs("static", exist_ok=True)
        caminho_completo = os.path.join("static", nome_arquivo)
            
        doc = SimpleDocTemplate(caminho_completo, pagesize=letter, title="Relatório de Transcrição")
        styles = getSampleStyleSheet()
        
        estilo_titulo_doc = ParagraphStyle('TituloDoc', parent=styles['Heading1'], fontSize=22, leading=26, spaceAfter=20, alignment=1)
        estilo_sub_video = ParagraphStyle('SubVideo', parent=styles['Heading2'], fontSize=14, leading=18, spaceBefore=15, spaceAfter=5)
        estilo_link = ParagraphStyle('LinkPersonalizado', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=10)
        estilo_texto = ParagraphStyle('TextoPersonalizado', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=15)
        
        elementos = [
            Paragraph("Relatório de Transcrição Avançada", estilo_titulo_doc),
            Spacer(1, 10),
            Paragraph("Vídeo Processado", estilo_sub_video),
            Paragraph(f"<b>Link:</b> <a href='{url}'><font color='blue'><u>{url}</u></font></a>", estilo_link),
            Paragraph(texto.replace('\n', '<br/>'), estilo_texto)
        ]
        
        doc.build(elementos)
        return caminho_completo
    except Exception as e:
        raise Exception(f"Erro ao gerar o PDF: {e}")

def processar_video_completo(url_video, idioma_escolhido):
    id_unico = int(time.time())
    nome_temporario = f"video_{id_unico}"
    
    ydl_opts = {
        'format': 'best', 
        'outtmpl': f'{nome_temporario}.%(ext)s',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }

    arquivo_final = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_video, download=True)
            extensao = info.get('ext', 'mp4')
            arquivo_final = f"{nome_temporario}.{extensao}"

        with open(arquivo_final, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=(arquivo_final, audio_file.read()),
            )

        texto_original = transcription.text
        texto_traduzido = traduzir_texto(texto_original, idioma_escolhido)
        
        nome_pdf = f"transcricao_{id_unico}.pdf"
        exportar_tudo_para_pdf(url_video, texto_traduzido, nome_pdf)
        
        return {
            "texto": texto_traduzido,
            "pdf_nome": nome_pdf
        }

    finally:
        if arquivo_final and os.path.exists(arquivo_final):
            os.remove(arquivo_final)
