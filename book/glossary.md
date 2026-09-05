# Glossary

This page collects the technical vocabulary of the book in one place, as a lookup list for revision and for writing your reflections. Every term is explained in context in the chapters, so treat these short definitions as reminders rather than as first introductions.

```{glossary}
Agent
: A system given a goal that chooses its own steps, calling tools in a loop of plan, act, and observe until a stopping condition is met.

Conditioning
: Any input besides noise that steers what a generative model produces, such as a text prompt, a reference image, a mask, or a control signal.

Diffusion model
: A generative model trained to remove noise step by step, so that it can turn pure noise into a coherent image, sound, or video.

Foundation model
: A very large model trained once on broad data and then adapted to many tasks by prompting or fine-tuning.

Hallucination
: A fluent, confident output that is false, a direct consequence of training a model to produce plausible rather than true text.

Inference
: Using a trained model to produce an output from an input; the parameters do not change.

Large language model (LLM)
: A transformer trained to predict the next token in text, on which chat, coding, and reasoning behaviours are built.

Prompt
: The text (and sometimes images or audio) given to a model to condition its output; the main interface of current generative tools.

Token
: The unit a language model reads and writes, usually a word piece; Norwegian text uses more tokens than the same text in English.

Training
: Repeatedly adjusting a model's parameters to reduce a loss measured on batches of data.
```
