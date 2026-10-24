---
title: "KV cache: where inference memory goes"
summary: A practical mental model for why autoregressive generation keeps
  growing its memory footprint as the context gets longer.
date: 2026-10-23
draft: false
featured: false
tags:
  - llm inference
  - gpu memory
  - systems
thumbnail: /images/posts/kv-cache.svg
thumbnailAlt: Rows of key and value blocks accumulate as generated tokens extend the context.
artifactSummary: "Draft: replace this illustration with a measurement or memory
  estimate from a real run before publishing."
caption: Conceptual illustration. The number and size of cached tensors depend
  on the model architecture and runtime.
updatedDate: 2026-10-24
---
The KV cache is easy to describe as a speed optimization. The more useful question is what it stores, why it prevents repeated work, and how its memory cost grows with the context.

This article is a draft scaffold. Before publishing, replace the conceptual artifact with a measured example and state the model, precision, batch size, context length, and runtime used.

## The mental model

In autoregressive generation, each new token can attend to earlier tokens. Attention layers produce keys and values for the tokens they process. Instead of recomputing those tensors for the entire prefix at every decode step, an inference runtime can retain the earlier keys and values and reuse them.

That saved computation is the benefit. The persistent key/value tensors are also a memory cost, and the cost grows with the number of cached tokens.

## Estimate the memory

For a conventional dense decoder-only transformer, a first-order estimate for KV-cache bytes is:

$$
M_{KV} \approx 2 \times L \times B \times T \times H_{KV} \times D_H \times S
$$

where L is the number of layers, B is the effective batch size, T is cached sequence length, H_{KV} is the number of key/value heads, D_H is head dimension, and S is bytes per element. The leading two accounts for keys and values.

This is an estimate, not an allocator-level measurement. Architecture choices such as multi-query or grouped-query attention, cache quantization, tensor parallelism, paging, and implementation details change how memory is represented or distributed.

## What to measure

Before publishing, add a reproducible experiment with a named model, dtype, batch size, prompt length, generation length, and measurement method. Distinguish allocated memory from reserved memory, and compare the measured slope with the estimate rather than expecting the two to match exactly.

## Where the model breaks down

The formula does not capture temporary activations, model weights, workspaces, allocator fragmentation, attention implementation details, or runtime-specific paging. A single GPU-memory number without those conditions is hard to interpret.

## Next experiment

Measure memory across several context lengths while holding the rest of the setup constant. Include the raw observations and enough metadata to reproduce the run. Then investigate where the linear approximation stops matching the allocator's reported behavior.