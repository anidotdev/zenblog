---
title: "Prefill and decode are different workloads"
summary: "Prompt processing and token generation use the same model, but stress inference hardware in different ways."
date: 2026-10-22
draft: true
featured: false
tags:
  - llm inference
  - performance
  - systems
thumbnail: "/images/posts/prefill-decode.svg"
thumbnailAlt: "A diagram contrasting parallel prompt processing with sequential next-token generation."
artifactSummary: "Draft: add timing traces from a reproducible inference run before publishing."
caption: "Conceptual diagram of the two stages; it is not a measured latency trace."
---

LLM inference is often discussed as one operation, but serving a prompt and generating the next token are different phases. Separating them helps explain why a model can have high prompt throughput and still feel slow during generation, or vice versa.

This is an unpublished draft scaffold. The final version should include measurements with the model, sequence lengths, batch size, precision, hardware, and inference runtime stated explicitly.

## Prefill: process the prompt

During prefill, the model processes the input prompt and produces the state needed to begin generation, including the initial key/value cache. The prompt's tokens can generally be processed in parallel within each layer, so prefill often exposes substantial matrix-multiplication work.

Long prompts increase the amount of work and the initial cache size. The exact latency depends on the model and runtime, but input length is a key part of the workload description.

## Decode: generate one token at a time

In ordinary autoregressive decoding, the next token depends on the previous output. The runtime repeats the forward step, reusing cached keys and values for the prefix. This serial dependency makes token generation a different performance problem from prompt processing.

Batching can increase utilization, but each active sequence may also require cache memory. Throughput, time to first token, and inter-token latency should therefore be reported separately rather than collapsed into one latency figure.

## A useful measurement plan

Record prompt length, generated token count, batch size, model precision, hardware, and runtime version. Measure time to first token, steady-state inter-token latency, and total generated tokens per second. Repeat each run, report the distribution, and separate cold-start effects from steady-state behavior.

## Failure modes in comparisons

A benchmark is difficult to interpret if one run includes model loading and another does not, if generated token counts differ, or if prompt lengths are uncontrolled. Different sampling settings can also change when generation stops. State the protocol before comparing runtimes.

## Next experiment

Plot time to first token against prompt length and inter-token latency against batch size. Those plots answer different questions. Keep the raw timings and execution configuration with the figure so a reader can reproduce the result.
