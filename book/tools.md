---
title: Tools
description: "The tool categories used in the course, with current examples and open alternatives."
---

# Tools

Across the semester you will meet many tools. The list below is not exhaustive, and any of it may change as the field moves: products merge, are bought, and disappear inside a semester, while the categories have been stable for years. The point is to learn the categories, so that you can evaluate the next tool that appears. Each category names one or two products most students will have heard of in 2026 and one open alternative; the list was last checked in November 2026.

Everything listed here is a tool rather than a model. Every tool wraps one or more models and adds an interface, a system prompt, safety filters, a data policy, and a price. The model behind a tool can change without the name changing. The entries below therefore name only the tool, while your practice log names both, with the model's version or the date. Chapter [2](how-it-works.ipynb#models-and-tools) sets out the difference.

## Apps made for this book

The book also ships with its own small apps: single-page, self-contained tools built to make one idea in a chapter concrete. They run in your browser, need no account, and send no data anywhere. The sixteen below are ready to use.

- [Training loop playground](https://fourms.github.io/Creative-AI/apps/training-loop/): watch a tiny model's loss fall step by step as it trains.
- [Next-token sampler](https://fourms.github.io/Creative-AI/apps/next-token-sampler/): compare greedy, temperature, and top-p sampling on the same next-token distribution.
- [Tokeniser explorer](https://fourms.github.io/Creative-AI/apps/tokeniser-explorer/): see how a sentence splits into tokens, and why Norwegian text costs more tokens than English.
- [Forward diffusion explorer](https://fourms.github.io/Creative-AI/apps/diffusion-explorer/): watch an image dissolve into noise, then step back to see how diffusion models learn to reverse it.
- [Inference energy estimator](https://fourms.github.io/Creative-AI/apps/energy-estimator/): estimate the energy and water cost of running a prompt through a model of a given size.
- [Provenance inspector](https://fourms.github.io/Creative-AI/apps/provenance-inspector/): inspect the metadata a generated file carries, and what it does and does not prove.
- [Word-vector explorer](https://fourms.github.io/Creative-AI/apps/word-vectors/): explore how word embeddings place related words near each other in vector space.
- [Markov melody generator](https://fourms.github.io/Creative-AI/apps/markov-melody/): generate a short melody from a Markov chain trained on a handful of tunes.
- [Agent loop simulator](https://fourms.github.io/Creative-AI/apps/agent-loop/): step through an agent's plan, act, and observe loop one tool call at a time.
- [Rhythm-bot](https://fourms.github.io/Creative-AI/apps/rhythm-bot/): map a tapped rhythm onto a simple generative pattern, live in the browser.
- [Evolve a picture](https://fourms.github.io/Creative-AI/apps/evolve/): breed a drawing by choosing favourites, biomorph style.
- [Seed and guidance grid viewer](https://fourms.github.io/Creative-AI/apps/grid-viewer/): step through a grid of generations that vary one knob at a time, with the settings shown beside each cell.
- [Frame-consistency inspector](https://fourms.github.io/Creative-AI/apps/frame-consistency/): step through a generated clip frame by frame with a difference view beside it, so you can see exactly when and where the drift begins.
- [Splat viewer](https://fourms.github.io/Creative-AI/apps/splat-viewer/): load a Gaussian splat capture and orbit it, with a control that thins the splats so you can see how little geometry is actually there.
- [Translation sketchpad](https://fourms.github.io/Creative-AI/apps/translation-sketchpad/): draw a line and hear it as pitch and loudness, then sing or play into the microphone and see the contour drawn back, with a rule-based text description as a third data type.
- [Sensor-to-sound mapper](https://fourms.github.io/Creative-AI/apps/sensor-mapper/): connect a phone or laptop sensor to a sound parameter, and compare a mapping you can learn with one you cannot.

## Tool categories

<details>
<summary>Text and dialogue</summary>

- [ChatGPT](https://chatgpt.com/), [Claude](https://claude.ai/), [Gemini](https://gemini.google.com/), [Mistral Le Chat](https://chat.mistral.ai/): commercial chat assistants; the UiO AI service wraps one of them for anything that involves personal data
- [Sudowrite](https://www.sudowrite.com/), [NotebookLM](https://notebooklm.google.com/): writing-focused tools

**Open alternative.** [LM Studio](https://lmstudio.ai/) and [Ollama](https://ollama.com/) run open-weight models locally on your own laptop.

</details>

<details>
<summary>Images</summary>

- [Midjourney](https://www.midjourney.com/), [Adobe Firefly](https://www.adobe.com/products/firefly.html), [Ideogram](https://ideogram.ai/): commercial text-to-image; the chat assistants above also generate images, and their free tiers are the easiest place to start
- [Krea](https://www.krea.ai/), [Recraft](https://www.recraft.ai/): design-oriented tools

**Open alternative.** [FLUX](https://blackforestlabs.ai/) and [Stable Diffusion](https://stability.ai/) are open-weight image models you can host yourself, run through [ComfyUI](https://www.comfy.org/) or [InvokeAI](https://invoke.com/). The FLUX.1 schnell weights carry an Apache 2.0 licence; check the licence of any other release before commercial use.

**Free and adjustable.** A hosted Stable Diffusion demo, run as a browser page on a model-hosting site, exposes the seed, the guidance value, and the step count with no account and no installation.

</details>

<details>
<summary>Sound and music</summary>

- [Suno](https://suno.com/): text-to-song. [Udio](https://www.udio.com/) was the other name here until autumn 2026, when it became a closed platform whose songs stay inside the app [2026? confirm the Udio status before teaching]
- [ElevenLabs](https://elevenlabs.io/), [Resemble](https://www.resemble.ai/): voice generation and cloning
- [Stable Audio](https://stability.ai/stable-audio): sound and music generation

**Open alternative.** [AudioCraft](https://github.com/facebookresearch/audiocraft) (MusicGen and AudioGen), [Stable Audio Open](https://huggingface.co/stabilityai/stable-audio-open-1.0), [Magenta RealTime](https://magenta.withgoogle.com/magenta-realtime), a live open-weights music model, and [RAVE](https://github.com/acids-ircam/RAVE) are open tools you can inspect, run, and retrain.

</details>

<details>
<summary>Video and animation</summary>

- [Google Veo](https://deepmind.google/models/veo/), [Runway](https://runwayml.com/), [Kling](https://klingai.com/), [Luma Dream Machine](https://lumalabs.ai/dream-machine): text- and image-to-video, with Veo generating sound along with the picture. OpenAI's Sora [2026? was reported discontinued in 2026; check before naming it] and [Pika](https://pika.art/) are the names students may know from short-form video.

**Open alternative.** Open-weight video models exist and run on a single good GPU, with [Stable Video Diffusion](https://stability.ai/stable-video) the earliest; [2026? name the current best open-weight video model, Wan or HunyuanVideo or a successor, after checking its licence].

</details>

<details>
<summary>Code and creative coding</summary>

- [Claude Code](https://www.anthropic.com/claude-code), [Cursor](https://cursor.com/), [GitHub Copilot](https://github.com/features/copilot): coding assistants that read files, run commands, and loop until the tests pass, the agents of chapter [8](code.ipynb)
- [p5.js](https://p5js.org/), [Processing](https://processing.org/): creative coding host languages
- [Glicol](https://glicol.org/): a graph-oriented live coding language for sound, free in the browser with no account
- [Strudel](https://strudel.cc/): TidalCycles patterns in the browser, free with no account

**Open alternative.** [OpenCode](https://opencode.ai/) or [Aider](https://aider.chat/) run the same loop in a terminal against an open-weight model served locally by [Ollama](https://ollama.com/); [Hugging Face Spaces](https://huggingface.co/spaces) lets you run open models in the browser without a subscription.

</details>

<details>
<summary>3D, XR, design, and games</summary>

- [Luma AI](https://lumalabs.ai/), [Polycam](https://poly.cam/), [Scaniverse](https://scaniverse.com/): Gaussian splats and 3D capture on a phone; Scaniverse is free
- [Meshy](https://www.meshy.ai/), [Tripo3D](https://www.tripo3d.ai/): text or image to 3D mesh
- [Scenario](https://www.scenario.com/), [Layer](https://www.layer.ai/): game-art pipelines
- [Meta Quest Browser](https://www.meta.com/quest/): a headset viewer for exploring Gaussian splats and WebXR scenes in VR
- [Adobe Aero](https://www.adobe.com/products/aero.html): a phone AR viewer for placing a generated 3D asset in the room in front of you
- [Grasshopper](https://www.grasshopper3d.com/): node-based generative design inside the commercial modeller Rhino, the tool architecture and product-design offices use

**Open alternative.** [Nerfstudio](https://docs.nerf.studio/) is an open-source toolkit for building and viewing your own Gaussian splats, and [Hunyuan3D](https://github.com/Tencent/Hunyuan3D-2) is an open-weight image-to-3D model. [Geometry Nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html) in Blender and [OpenSCAD](https://openscad.org/) cover the same ground as Grasshopper for free, and their objects are printable by construction. [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) and [Bambu Studio](https://github.com/bambulab/BambuStudio) are open-source slicers for the printers in the UiO makerspaces named in chapter 7.

</details>

<details>
<summary>Agents and assistants</summary>

- Terminal and editor coding agents that plan, edit files, run code, and report a trace
- Research or deep-research modes inside a commercial chat assistant, which run the same loop over search results
- Browser-using agents, which act on live websites and need the narrowest permissions of the three

**Open alternative.** An agent framework run locally against an open-weight model, which prints its own trace and calls only the tools you define.

</details>

## Hardware to borrow

The following equipment is available through the fourMs Lab. Ask the course coordinator:

- a VR headset
- a 360 camera
- a phone gimbal
- an Arduino kit with sensors
- a small robot platform

:::{warning} Tool turnover
Specific products listed above will appear, merge, and disappear during the semester. Treat the list as a starting point, not a syllabus. In every practice session the course uses whatever currently works well enough for the task at hand.
:::
