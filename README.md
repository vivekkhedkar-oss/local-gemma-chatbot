# Local Gemma Chatbot

A small terminal chatbot that runs **entirely on your own machine**. It talks to Google's Gemma model through [Ollama](https://ollama.com) and streams the replies token by token. Each "persona" is a plain Markdown file used as the system prompt, so you can change the bot's behavior without touching any code.

- **Stack:** Python 3 (standard library only, no `pip install`), Ollama REST API, `gemma4:e2b`
- **Runs offline:** no API keys or cloud calls, and nothing leaves your laptop

## Demo

Default persona ([`AGENTS.md`](AGENTS.md)):

```text
$ python chatbot.py
Chatting with gemma4:e2b as AGENTS.md. Type /exit to quit.

you> In one sentence, what is retrieval-augmented generation?
bot> Retrieval-Augmented Generation (RAG) is a technique that enhances large language models
     by retrieving relevant, external information and using it to generate more accurate and
     grounded responses.
```

The same model with a different persona ([`personas/socratic-tutor.md`](personas/socratic-tutor.md)):

```text
$ python chatbot.py --persona personas/socratic-tutor.md
Chatting with gemma4:e2b as socratic-tutor.md. Type /exit to quit.

you> Why does ice float on water?
bot> That is a great question that touches upon the principles of density and buoyancy. To start
     thinking about this, what happens to an object when you place it in a liquid?
```

## How it works

- **Streaming:** sends `POST /api/chat` with `stream: true` and prints each JSON line's content as it arrives, so you see replies forming instead of waiting for the whole answer.
- **Conversation memory:** keeps the full user/assistant history in memory and sends it with every request, so the model remembers earlier turns.
- **Persona hot-reload:** re-reads the persona file on every turn, so you can edit the system prompt mid-conversation and see the effect on the next reply.
- **Graceful failure:** if Ollama isn't running, it shows a clear message and drops the unanswered turn from history so the conversation stays consistent.

## Run it

```bash
# one-time setup (needs internet)
ollama pull gemma4:e2b

# chat
python chatbot.py                                    # default persona
python chatbot.py --persona personas/socratic-tutor.md
```

Type `/exit` (or press Ctrl+C) to quit. To use a different model, change `MODEL` at the top of [`chatbot.py`](chatbot.py).

## Write your own persona

Create any Markdown file that describes how the assistant should behave, then point `--persona` at it. Files ending in `.local.md` are git-ignored, so you can keep private personas out of the repo.

---

*Related: [personal-wiki-gemma-rag](https://github.com/vivekkhedkar-oss/personal-wiki-gemma-rag) builds on this same local Gemma setup and adds retrieval and cited answers.*
