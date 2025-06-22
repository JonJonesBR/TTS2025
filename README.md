# 🔊 TTS2025: Gerador de Audiobook Gratuito (PDF, TXT, EPUB, DOC/DOCX para MP3)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![Edge TTS](https://img.shields.io/badge/Edge%20TTS-0078D4?style=for-the-badge&logo=microsoftedge&logoColor=white)

Este repositório contém o código-fonte de um projeto simples para converter documentos de texto (PDF, TXT, EPUB, DOC/DOCX) em arquivos de áudio MP3 (audiobooks) usando a tecnologia de Text-to-Speech (TTS) da Microsoft Edge. O projeto foi desenvolvido inicialmente no Google Colab e utiliza FastAPI para o backend e um frontend HTML/JavaScript para interação.

## 🚀 Visão Geral

O TTS2025 oferece uma solução prática e gratuita para transformar seus documentos em áudio. Ele permite que usuários façam upload de um arquivo e escolham entre diversas vozes disponíveis (principalmente vozes brasileiras, incluindo a Thalita Neural) para gerar um audiobook.

**Funcionalidades Principais:**

* **Suporte a Múltiplos Formatos:** Converte arquivos `.pdf`, `.txt`, `.epub`, `.doc` e `.docx`.
* **Vozes Naturais:** Utiliza as vozes de alta qualidade da Microsoft Edge TTS, incluindo a popular voz "Thalita" em português do Brasil.
* **Processamento Assíncrono:** As conversões são realizadas em segundo plano, permitindo que o usuário acompanhe o progresso.
* **Frontend Intuitivo:** Uma interface web simples para upload de arquivos e seleção de voz.
* **Download Direto:** O audiobook gerado é disponibilizado para download diretamente pelo navegador.

## ⚙️ Como Funciona

1.  **Upload do Arquivo:** O usuário faz upload de um documento via interface web.
2.  **Extração de Texto:** O backend extrai o texto do documento uploaded, tratando diferentes formatos (PDF, DOCX, EPUB, TXT).
3.  **Conversão TTS:** O texto extraído é enviado para a API do Edge TTS, que o converte em áudio.
4.  **Geração do MP3:** O áudio é streamado e salvo como um arquivo MP3.
5.  **Download e Limpeza:** O usuário pode baixar o audiobook. Após o download, o arquivo gerado e os arquivos temporários são automaticamente limpos para economizar espaço e manter a privacidade.

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * [FastAPI](https://fastapi.tiangolo.com/): Framework web para construção de APIs rápidas e assíncronas.
    * [PyPDF2](https://pypdf2.readthedocs.io/): Para extração de texto de arquivos PDF.
    * [python-docx](https://python-docx.readthedocs.io/): Para extração de texto de arquivos DOCX.
    * [EbookLib](https://github.com/aerkalov/ebooklib): Para manipulação de arquivos EPUB.
    * [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Usado em conjunto com EbookLib para parsing HTML em EPUBs.
    * [edge-tts](https://github.com/rany2/edge-tts): Biblioteca para interfacear com o serviço de Text-to-Speech da Microsoft Edge.
* **Frontend:**
    * HTML, CSS, JavaScript Puro.
* **Implantação/Ambiente de Desenvolvimento (Exemplo):**
    * [Google Colab](https://colab.research.google.com/): Ambiente de notebook para desenvolvimento e execução inicial.
    * [Uvicorn](https://www.uvicorn.org/): Servidor ASGI para rodar aplicações FastAPI.
    * [ngrok](https://ngrok.com/): Para expor o servidor local do Colab à internet.

## 🚀 Como Rodar o Projeto (no Google Colab)

Este projeto é otimizado para ser executado no Google Colab, onde todas as dependências são facilmente instaladas e o servidor pode ser exposto publicamente via ngrok.

1.  **Abra o Notebook:** Faça upload do arquivo `tts2025.py` (ou `TTS2025.ipynb` se você o salvou como notebook) para o Google Colab.
2.  **Execute as Células:**
    * **Célula 1: Instalar Bibliotecas:** Execute a primeira célula para instalar todas as dependências Python necessárias.
    * **Célula 2: Criar Pastas:** Execute a célula para criar os diretórios `uploads`, `audiobooks` e `static`.
    * **Célula 3: Criar `main.py`:** Execute esta célula (`%%writefile main.py`). Ela irá criar o arquivo principal da API FastAPI.
    * **Célula 4: Criar `index.html`:** Execute esta célula (`%%writefile static/index.html`). Ela irá criar o arquivo HTML do frontend na pasta `static`.
    * **Célula 5: Iniciar Uvicorn e ngrok:** **IMPORTANTE:** Antes de executar esta célula, você precisará obter seu próprio `NGROK_AUTH_TOKEN` em [ngrok.com](https://ngrok.com/). Substitua `"2xbaQNvi6miSZUVf8MzgZAQfTh6_t2wYSecnyeuys1qhr5vc"` pelo seu token real.
        ```python
        # SUBSTITUA "SEU_AUTH_TOKEN_AQUI" PELO SEU TOKEN REAL
        ngrok.set_auth_token("SEU_AUTH_TOKEN_AQUI")
        ```
        Após configurar o token, execute esta célula. Ela iniciará o servidor FastAPI e fornecerá uma URL pública do ngrok.
3.  **Acesse o Projeto:** Copie a URL gerada pelo ngrok (geralmente algo como `https://xxxxx.ngrok-free.app`) e cole-a no seu navegador. Você verá a interface do gerador de audiobook.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para bugs ou sugestões de novas funcionalidades, ou envie pull requests.

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` (se houver) para mais detalhes.

---
Feito com ❤️ por [JonJonesBR](https://github.com/JonJonesBR)
