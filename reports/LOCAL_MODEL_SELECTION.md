# Local model selection — 2026-11-21

Chosen initial candidate: **qwen3.5:2b-q4_K_M**,2B parameters,Q4_K_M;
Ollama library reports1.9GB on disk. This is the largest conservative initial
candidate under the measured8GiB RAM,heavy swap and6.06GB free disk.
It is a supervised assistant for bounded coding/tests,not a mathematical oracle.
A successful load alone will not certify research quality.

Operational limits:one loaded model,one inference request,one agent role at once;
initial context16,384 tokens versus advertised262,144;bounded output2,048 tokens;
short keepalive and explicit unload after a cycle. Estimated runtime model+KV+
scratch2.5–3.5GiB,plus Qwen Code/Node and OS;actual use/speed must be recorded.
These are planning estimates,not measured memory requirements or throughput.
If current pressure prevents a safe run,use a smaller model or report failure;
do not silently download a larger model or use a paid provider.

Alternatives rejected/deferred:

- Qwen3.8-27B:current official newer family,far beyond8GiB at practical quantization.
- Qwen3.6-27B/35B:18–23GB Ollama artifacts,exceed RAM and free disk.
- Qwen3-Coder30B-A3B:19GB weights despite3.3B active;does not fit.
- Qwen3.5-9B:6.6–7.6GB weights leave no runtime/OS headroom.
- Qwen3.5-4B:3.3–4GB default artifact;too little memory/disk margin under current load.
- Qwen3.5-0.8B:smaller fallback if2B cannot run reliably;weaker reasoning/tool use.
- Older Qwen2.5-Coder:small code-specialized alternatives,not preferred before
  testing the newer tool-capable2B family.
- vLLM:unnecessary additional stack for this Apple Silicon CPU/GPU and small RAM.

Official evidence inspected (2026-11-21):

- https://github.com/QwenLM/Qwen3.8/blob/main/README.md (release/family sizes)
- https://ollama.com/library/qwen3.5/tags (exact2b-q4_K_M1.9GB tag)
- https://ollama.com/library/qwen3.6 (27B/35B current alternatives)
- https://ollama.com/library/qwen3-coder (30B artifact size)
- https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/README.md (tool usage and family runtime conventions)

Selection is resource-constrained,not a claim that2B is the strongest scientific
model in general. Astra independently audits every proposed conclusion.

## Observed installation and first model probe

Ollama0.32.0 installed via Homebrew;Qwen Code0.28.0 via official npm.
The downloaded tag identifies1.9B actual parameters,Q4_K_M,GGUF;disk artifact
1,945,781,358 bytes. Digest:
`1e2d21a4f03ab9e4a9c1976a4b7e88f21de61d65f2c5485d8fde8942be73f1e7`.
Ollama reported1,692,223,404 bytes resident on Metal at16,384 context tokens.
The37-token native tool-call generation took1.825s of decoding (~20.3tokens/s),
but cold load plus prompt processing made the whole request52.4s. Large Qwen
system/tool prompts are much slower to prefill;do not equate decode speed with
end-to-end agent latency. These observations are a smoke test,not a benchmark.

A local alias `pasqal-qwen-research:latest` references the exact same blobs
(no second weight download). It avoids Qwen Code's hosted-Qwen-specific thinking
parameter rewrite:Ollama's compatible route needs `reasoning_effort:none`.
The first CLI attempt timed out,then the route was corrected. The alias is the
configured service id;the source model/digest above remain authoritative.

No paid token is used. The SDK's nonsecret localhost placeholder is injected
only into the child environment. Qwen roles remain small supervised assistants.
