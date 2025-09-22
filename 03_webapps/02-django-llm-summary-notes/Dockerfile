FROM ollama/ollama:latest
ARG OLLAMA_MODEL=qwen2.5:7b-instruct
RUN /bin/sh -lc "ollama serve & sleep 3 && \
                 ollama pull ${OLLAMA_MODEL} && \
                 kill %1 || true"
EXPOSE 11434
