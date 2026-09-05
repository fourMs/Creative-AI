---
title: Tools
description: "The tool categories used in the course, with current examples and open alternatives."
---

# Tools

Across the semester you will meet many tools. The list below is not exhaustive, and any of it may change as the field moves. The point is to *learn the categories*, so that you can evaluate the next tool that appears.

## Apps made for this book

The book also ships with its own small apps: single-page, self-contained tools built to make one idea in a chapter concrete. They run in your browser, need no account, and send no data anywhere. Most are still being built; each link below goes live once its app lands, and the "in preparation" label disappears at the same time.

- [Training loop playground](https://fourms.github.io/Creative-AI/apps/training-loop/): watch a tiny model's loss fall step by step as it trains.
- [Next-token sampler](https://fourms.github.io/Creative-AI/apps/next-token-sampler/): compare greedy, temperature, and top-p sampling on the same next-token distribution.
- [Tokeniser explorer](https://fourms.github.io/Creative-AI/apps/tokeniser-explorer/): see how a sentence splits into tokens, and why Norwegian text costs more tokens than English.
- [Forward diffusion explorer](https://fourms.github.io/Creative-AI/apps/diffusion-explorer/): watch an image dissolve into noise, then step back to see how diffusion models learn to reverse it.
- [Inference energy estimator](https://fourms.github.io/Creative-AI/apps/energy-estimator/): estimate the energy and water cost of running a prompt through a model of a given size.
- [Provenance inspector](https://fourms.github.io/Creative-AI/apps/provenance-inspector/) (in preparation): inspect the metadata a generated file carries, and what it does and does not prove.
- [Word-vector explorer](https://fourms.github.io/Creative-AI/apps/word-vectors/) (in preparation): explore how word embeddings place related words near each other in vector space.
- [Markov melody generator](https://fourms.github.io/Creative-AI/apps/markov-melody/) (in preparation): generate a short melody from a Markov chain trained on a handful of tunes.
- [Agent loop simulator](https://fourms.github.io/Creative-AI/apps/agent-loop/) (in preparation): step through an agent's plan, act, and observe loop one tool call at a time.
- [Rhythm-bot](https://fourms.github.io/Creative-AI/apps/rhythm-bot/) (in preparation): map a tapped rhythm onto a simple generative pattern, live in the browser.

## Tool categories

<details>
<summary>Text and dialogue</summary>

- [ChatGPT](https://chatgpt.com/), [Claude](https://claude.ai/), [Gemini](https://gemini.google.com/), [Mistral Le Chat](https://chat.mistral.ai/) — commercial chat assistants
- [Sudowrite](https://www.sudowrite.com/), [NotebookLM](https://notebooklm.google.com/) — writing-focused tools

**Open alternative.** [LM Studio](https://lmstudio.ai/) and [Ollama](https://ollama.com/) run open-weight models locally on your own laptop.

</details>

<details>
<summary>Images</summary>

- [Midjourney](https://www.midjourney.com/), [DALL·E](https://openai.com/index/dall-e-3/), [Adobe Firefly](https://www.adobe.com/products/firefly.html), [Ideogram](https://ideogram.ai/) — commercial text-to-image
- [Krea](https://www.krea.ai/), [Recraft](https://www.recraft.ai/) — design-oriented tools

**Open alternative.** [Stable Diffusion](https://stability.ai/), run through [ComfyUI](https://www.comfy.org/) or [InvokeAI](https://invoke.com/), is an open-weight image model you can host yourself.

</details>

<details>
<summary>Sound and music</summary>

- [Suno](https://suno.com/), [Udio](https://www.udio.com/) — text-to-song
- [ElevenLabs](https://elevenlabs.io/), [Resemble](https://www.resemble.ai/) — voice generation and cloning
- [Riffusion](https://riffusion.com/), [Stable Audio](https://stability.ai/stable-audio) — sound and music generation

**Open alternative.** [Magenta](https://magenta.tensorflow.org/) and [RAVE](https://github.com/acids-ircam/RAVE) are research-grade open tools you can inspect and retrain.

</details>

<details>
<summary>Video and animation</summary>

- [Runway](https://runwayml.com/), [Pika](https://pika.art/), [Luma Dream Machine](https://lumalabs.ai/dream-machine), [OpenAI Sora](https://openai.com/sora) — text- and image-to-video
- [Kaiber](https://kaiber.ai/) — stylised animation

**Open alternative.** [Stable Video Diffusion](https://stability.ai/stable-video) is an open-weight video model you can run on your own hardware.

</details>

<details>
<summary>Code and creative coding</summary>

- [Cursor](https://cursor.com/), [GitHub Copilot](https://github.com/features/copilot), [Claude Code](https://www.anthropic.com/claude-code) — AI-assisted development environments
- [p5.js](https://p5js.org/), [Processing](https://processing.org/) — creative coding host languages

**Open alternative.** [Hugging Face Spaces](https://huggingface.co/spaces) lets you run open models in the browser without a commercial subscription.

</details>

<details>
<summary>3D, XR, design, and games</summary>

- [Luma AI](https://lumalabs.ai/), [Polycam](https://poly.cam/) — Gaussian splats and 3D capture
- [Meshy](https://www.meshy.ai/), [Tripo3D](https://www.tripo3d.ai/) — text/image to 3D mesh
- [Scenario](https://www.scenario.com/), [Layer](https://www.layer.ai/) — game-art pipelines
- [Meta Quest Browser](https://www.meta.com/quest/): a headset viewer for exploring Gaussian splats and WebXR scenes in VR
- [Adobe Aero](https://www.adobe.com/products/aero.html): a phone AR viewer for placing a generated 3D asset in the room in front of you

**Open alternative.** [Nerfstudio](https://docs.nerf.studio/) is an open-source toolkit for building and viewing your own Gaussian splats.

</details>

## Hardware to borrow

The following equipment is available through the fourMs Lab, ask the course coordinator:

- a VR headset
- a 360 camera
- a phone gimbal
- an Arduino kit with sensors
- a small robot platform

:::{warning} Tool turnover
Specific products listed above will appear, merge, and disappear during the semester. Treat the list as a starting point, not a syllabus. In every practice session we will use whatever currently works well enough for the task at hand.
:::
