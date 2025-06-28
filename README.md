# 🔊 Audiobook Generator: Seu Leitor de Livros Pessoal

Transforme seus documentos e e-books em audiobooks com vozes naturais e de alta qualidade. Perfeito para ouvir seus textos em qualquer lugar!

**Acesse o aplicativo aqui:** [https://tts-master.onrender.com/](https://tts-master.onrender.com/)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Edge TTS](https://img.shields.io/badge/Edge%20TTS-0078D4?style=for-the-badge&logo=microsoftedge&logoColor=white)

## O que o Audiobook Generator faz?

Este aplicativo web gratuito converte seus arquivos de texto em áudio (MP3) que você pode baixar e ouvir quando quiser. É como ter alguém lendo seus documentos ou livros favoritos para você.

Ele suporta os formatos de arquivo mais comuns:
* **PDF**
* **TXT**
* **EPUB** (formato padrão para e-books)
* **DOC** e **DOCX** (arquivos do Microsoft Word)

## Como Usar: Um Guia Passo a Passo

Siga estes passos simples para criar seu primeiro audiobook.

### Passo 1: Acesse o Site

Clique no link a seguir para abrir o aplicativo no seu navegador:
[**tts-master.onrender.com**](https://tts-master.onrender.com/)

### Passo 2: Escolha uma Voz

No menu suspenso "Escolha a Voz", você encontrará várias opções de vozes em português do Brasil, incluindo as populares vozes neurais (como a "Thalita"), que soam muito naturais. Selecione a que você mais gosta.

### Passo 3: Faça o Upload do seu Arquivo

1.  Clique no botão **"Escolher arquivo"**.
2.  Selecione o documento (PDF, TXT, EPUB, DOC/DOCX) do seu computador que você deseja converter.

### Passo 4 (Opcional): Adicione um Título

Você pode dar um nome ao seu livro no campo "Título do Livro". Isso ajuda a organizar seus audiobooks baixados.

### Passo 5 (Opcional, mas recomendado): Aprimoramento com IA (Google Gemini)

Para uma qualidade de áudio ainda melhor, você pode usar a inteligência artificial do Google para revisar e formatar o texto antes da conversão. Isso corrige a pontuação para uma narração mais fluida e expande abreviações (como "Dr." para "Doutor").

**Como ativar:**
1.  Obtenha uma chave de API gratuita do Google AI Studio:
    * Acesse **[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**.
    * Faça login com sua conta Google e clique em "**Create API Key in new project**".
    * Copie a chave gerada.
2.  No site do Audiobook Generator, cole a chave no campo "**Sua Chave API do Google Gemini**" e clique em "**Salvar Chave API**".
3.  Marque a caixa de seleção "**Usar IA Gemini para aprimorar o texto**".

### Passo 6: Gere seu Audiobook!

1.  Clique no botão azul **"Gerar Audiobook"**.
2.  Aguarde enquanto o aplicativo processa seu arquivo. Você verá uma barra de progresso mostrando o andamento da conversão.
3.  Quando o processo terminar, o download do arquivo MP3 começará automaticamente!

Pronto! Agora você pode ouvir seu documento ou livro em qualquer dispositivo que toque arquivos de áudio.

## Recursos Principais

* **Totalmente Gratuito:** Sem custos ou assinaturas.
* **Vozes de Alta Qualidade:** Utiliza a tecnologia Text-to-Speech da Microsoft para criar áudios que soam como uma pessoa de verdade.
* **Fácil de Usar:** Interface simples e intuitiva, projetada para todos.
* **Privacidade:** Seus arquivos são processados e depois excluídos do servidor para garantir sua privacidade.

## Para Desenvolvedores

Este projeto foi construído com as seguintes tecnologias:

* **Backend:** FastAPI (Python)
* **Frontend:** HTML, CSS e JavaScript
* **Conversão de Texto:** `edge-tts` e bibliotecas de extração como `PyPDF2` e `python-docx`.

Se você tiver interesse em contribuir ou executar o projeto localmente, sinta-se à vontade para explorar os arquivos no repositório.

---
Feito com ❤️ por [JonJonesBR](https://github.com/JonJonesBR)
