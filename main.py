
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import io
import asyncio
import edge_tts
from PyPDF2 import PdfReader
from docx import Document
from ebooklib import epub
from bs4 import BeautifulSoup
import traceback
import json
import uuid

import nest_asyncio

nest_asyncio.apply()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

cached_voices = {}
conversion_tasks = {}
NGROK_AUTH_TOKEN = None
PUBLIC_NGROK_URL = None


async def get_text_from_file(file_path: str, task_id: str):
    text = ""
    filename = os.path.basename(file_path)
    total_parts = 1

    try:
        if filename.endswith('.pdf'):
            reader = PdfReader(file_path)
            total_parts = len(reader.pages)
            for i, page in enumerate(reader.pages):
                extracted_page_text = page.extract_text()
                if extracted_page_text:
                    text += extracted_page_text + "\n"
                progress = int(((i + 1) / total_parts) * 50)
                conversion_tasks[task_id].update({"progress": progress, "message": f"Extraindo texto (Página {i+1}/{total_parts})..."})
                await asyncio.sleep(0.01)
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            conversion_tasks[task_id].update({"progress": 50, "message": "Texto de arquivo TXT lido."})
        elif filename.endswith('.docx'):
            doc = Document(file_path)
            total_parts = len(doc.paragraphs)
            for i, paragraph in enumerate(doc.paragraphs):
                text += paragraph.text + "\n"
                progress = int(((i + 1) / total_parts) * 50)
                conversion_tasks[task_id].update({"progress": progress, "message": f"Extraindo texto (Parágrafo {i+1}/{total_parts})..."})
                await asyncio.sleep(0.01)
        elif filename.endswith('.epub'):
            book = epub.read_epub(file_path)
            document_items = [item for item in book.get_items() if item.get_type() == epub.ITEM_DOCUMENT]
            total_parts = len(document_items)
            for i, item in enumerate(document_items):
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text += soup.get_text(separator='\n') + "\n"
                progress = int(((i + 1) / total_parts) * 50)
                conversion_tasks[task_id].update({"progress": progress, "message": f"Extraindo texto (Capítulo {i+1}/{total_parts})..."})
                await asyncio.sleep(0.01)

        conversion_tasks[task_id].update({"progress": 50, "message": "Extração de texto concluída."})
        print(f"Extração de texto para {filename} concluída. Total de caracteres: {len(text)}.")
        return text.strip()
    except Exception as e:
        print(f"Erro na extração de texto de {filename}: {e}")
        conversion_tasks[task_id].update({"status": "failed", "message": f"Erro na extração de texto: {str(e)}"})
        raise

async def get_available_voices():
    global cached_voices
    if cached_voices:
        return cached_voices

    print("Buscando vozes Edge TTS disponíveis...")
    try:
        voices = await edge_tts.list_voices()
        pt_br_voices = {}
        for voice in voices:
            if voice["Locale"] == "pt-BR":
                name = voice["ShortName"].replace("pt-BR-", "")
                name = name.replace("Neural", " (Neural)")
                if voice["Gender"] == "Female":
                    name = f"{name} (Feminina)"
                elif voice["Gender"] == "Male":
                    name = f"{name} (Masculina)"
                pt_br_voices[voice["ShortName"]] = name.strip()

        ordered_voices = {}
        if "pt-BR-ThalitaMultilingualNeural" in pt_br_voices:
            ordered_voices["pt-BR-ThalitaMultilingualNeural"] = pt_br_voices["pt-BR-ThalitaMultilingualNeural"]
        if "pt-BR-FranciscaNeural" in pt_br_voices:
            ordered_voices["pt-BR-FranciscaNeural"] = pt_br_voices["pt-BR-FranciscaNeural"]
        if "pt-BR-AntonioNeural" in pt_br_voices:
            ordered_voices["pt-BR-AntonioNeural"] = pt_br_voices["pt-BR-AntonioNeural"]

        for code, name in pt_br_voices.items():
            if code not in ordered_voices:
                ordered_voices[code] = name

        cached_voices = ordered_voices
        print(f"Vozes carregadas: {len(cached_voices)} opções.")
        return cached_voices
    except Exception as e:
        print(f"Erro ao obter vozes Edge TTS: {e}")
        print(traceback.format_exc())
        return {
            "pt-BR-ThalitaMultilingualNeural": "Thalita (Feminina, Neural) - Fallback",
            "pt-BR-FranciscaNeural": "Francisca (Feminina, Neural) - Fallback",
            "pt-BR-AntonioNeural": "Antonio (Masculina, Neural) - Fallback"
        }

async def perform_conversion_task(task_id: str, file_path: str, voice: str):
    try:
        conversion_tasks[task_id].update({"status": "extracting", "message": "Iniciando extração de texto...", "progress": 0})
        text = await get_text_from_file(file_path, task_id)

        if not text:
            conversion_tasks[task_id].update({"status": "failed", "message": "Não foi possível extrair texto do arquivo."})
            return

        audio_filename = os.path.splitext(os.path.basename(file_path))[0] + ".mp3"
        audio_filepath = os.path.join("audiobooks", audio_filename)
        conversion_tasks[task_id]["file_path"] = audio_filepath
        conversion_tasks[task_id]["total_characters"] = len(text)

        print(f"Iniciando geração de áudio com Edge TTS (Voz: {voice}) para {len(text)} caracteres...")
        conversion_tasks[task_id].update({"status": "converting", "message": "Convertendo texto em áudio...", "progress": 50})

        communicate = edge_tts.Communicate(text, voice)
        audio_data_bytes = b""
        chunk_counter = 0

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data_bytes += chunk["data"]
                chunk_counter += 1
                progress_tts = int(50 + (chunk_counter / 500) * 50)
                progress_tts = min(progress_tts, 99)
                conversion_tasks[task_id].update({"progress": progress_tts, "message": f"Gerando áudio ({progress_tts-50}% concluído)..."})
                await asyncio.sleep(0.001)
            elif chunk["type"] == "end":
                print(f"Fim do stream TTS para tarefa {task_id}.")

        with open(audio_filepath, "wb") as out:
            out.write(audio_data_bytes)
        print(f"Áudio para tarefa {task_id} gerado e salvo em {audio_filepath}.")

        conversion_tasks[task_id].update({"status": "completed", "message": "Audiobook pronto para download!", "progress": 100})
    except Exception as e:
        print(f"Erro na conversão da tarefa {task_id}: {e}")
        print(traceback.format_exc())
        conversion_tasks[task_id].update({"status": "failed", "message": f"Erro na conversão: {str(e)}"})
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo de texto temporário {os.path.basename(file_path)} removido.")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/voices", response_class=JSONResponse)
async def list_voices_endpoint():
    voices = await get_available_voices()
    return voices

@app.post("/process_file")
async def process_file_endpoint(file: UploadFile = File(...), voice: str = "pt-BR-ThalitaMultilingualNeural", background_tasks: BackgroundTasks = BackgroundTasks()):
    
    current_available_voices = await get_available_voices()
    if voice not in current_available_voices:
        raise HTTPException(status_code=400, detail=f"Voz '{voice}' não é válida. Escolha uma das opções disponíveis.")
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado.")

    task_id = str(uuid.uuid4())
    temp_input_filepath = os.path.join("uploads", f"{task_id}_{file.filename}")

    try:
        content = await file.read()
        with open(temp_input_filepath, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo temporário: {str(e)}")

    conversion_tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Tarefa iniciada, aguardando processamento...",
        "file_path": None,
        "total_characters": 0
    }

    background_tasks.add_task(perform_conversion_task, task_id, temp_input_filepath, voice)

    return JSONResponse({"task_id": task_id, "message": "Processamento iniciado. Use o endpoint /status para verificar o progresso."})

@app.get("/status/{task_id}")
async def get_conversion_status(task_id: str):
    status = conversion_tasks.get(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="ID da tarefa não encontrado ou tarefa já concluída e limpa.")
    return JSONResponse(status)

@app.get("/download/{task_id}")
async def download_audiobook(task_id: str, background_tasks: BackgroundTasks):
    status = conversion_tasks.get(task_id)
    if not status or status["status"] != "completed" or not status["file_path"] or not os.path.exists(status["file_path"]):
        print(f"Tentativa de download para tarefa {task_id} falhou. Status: {status}")
        raise HTTPException(status_code=404, detail="Audiobook não encontrado ou ainda não pronto para download.")

    audio_filepath = status["file_path"]
    filename = os.path.basename(audio_filepath)

    response = FileResponse(audio_filepath, media_type="audio/mpeg", filename=filename, background=background_tasks)

    background_tasks.add_task(cleanup_file_after_download, audio_filepath, task_id)

    return response

async def cleanup_file_after_download(file_path: str, task_id: str):
    print(f"Iniciando limpeza do arquivo temporário: {file_path}")
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Arquivo temporário {file_path} removido com sucesso.")
    else:
        print(f"Arquivo temporário {file_path} não encontrado para remoção (já removido?).")

    if task_id in conversion_tasks:
        del conversion_tasks[task_id]
        print(f"Status da tarefa {task_id} removido.")
