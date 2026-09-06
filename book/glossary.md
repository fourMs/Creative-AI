# Glossary

This page collects the technical vocabulary of the book in one place, as a lookup list for revision and for writing your reflections. Every term is explained in context in the chapters, so treat these short definitions as reminders rather than as first introductions.

```{glossary}
4E cognition
: The view that cognition is embodied, embedded, enactive, and extended. That is, it is shaped by the body, fitted to a physical and social setting, brought forth through activity, and reaching into external resources that are reliably available and trusted the way memory is trusted.

Aesthetic control
: The precision with which a person can steer a generative system towards the artefact they actually want. Sampler settings, conditioning, and reference material are the layers of a pipeline that give a maker this control.

Agent
: A system given a goal that chooses its own steps, calling tools in a loop of plan, act, and observe until a stopping condition is met.

AI literacy
: The competencies a non-specialist needs in order to use, evaluate, and live alongside AI systems, including the habit of asking what a claim asserts, what evidence supports it, how it was measured, and what it leaves out. The term comes from Long and Magerko's 2020 framework.

Alignment training (RLHF)
: Shaping a raw next-token predictor into a system that answers questions, follows instructions, and refuses some requests, using human or model-generated feedback rather than plain next-token prediction.

Anarchive
: A computational memory that holds no fixed documents but continuously reorganises cultural traces into new generative forms, a term used by Pierre Cassou-Noguès and Gwenola Wagon. Chapter 3 uses it for the latent space of a trained model, where provenance is unstable and meaning is relational rather than documentary.

Attention
: The mechanism in a transformer that lets every element of a sequence look at every other element. It is what allows a model to relate a word at the end of a paragraph to one at the beginning.

Audio–video and auditory–visual
: Audio and video name data, the recorded, transmitted, or generated signal; auditory and visual name perception and processing, whether in a person or in a machine. A film is an audio–video artefact, and watching it is auditory–visual. The book keeps the two apart rather than folding them into a single word that means both.

Autoencoder
: A pair of networks trained together, one compressing an input into a short list of numbers and the other rebuilding the input from it. The short list is a latent representation, and a variational autoencoder shapes that space so that moving through it produces plausible new outputs.

Autoregressive model
: A model that predicts the next element of a sequence given the previous ones, factorising a distribution over sequences into a chain of small predictions. It powers chat models and a good deal of audio and image generation.

Backpropagation
: The procedure that computes how each parameter in a neural network should change to reduce the loss, by propagating the error backwards through the network's layers so that gradient descent has something to act on.

Beat tracking
: Estimating in real time where the pulse of a piece of music falls, so that a listening system can align its own response to it. Musical robots use it to tap along with what they hear.

Belief system
: A collection of behaviours designed into a robot that lets a human partner perceive it as a partner while playing. The claim is about what a person in the room can reasonably believe, not about the robot's inner life.

Bias
: A property of training data, propagated by an averaging process that is working correctly, in which a model becomes best at whatever its data over-represents and blander or worse everywhere else. It is not a bug to be debugged out of the model without changing the data or the objective.

Brief
: A bounded description of a goal, with enough context to make the result checkable and enough constraint to make the work finishable. It is the interface for working with an agent, in place of a single prompt.

C2PA
: A technical specification for signed content credentials that attaches provenance metadata, such as which tools made or edited a file, to a piece of media. It is the most developed attempt at provenance infrastructure as of 2026.

Cellular automaton
: A grid of cells whose states update together at each step according to a rule that looks only at each cell's neighbours. Simple rules can produce elaborate patterns, as in Conway's Game of Life.

Character reference
: An image of a subject used to condition generation so that a model matches an existing appearance rather than reconstructing one from words. It is cheap and needs no training, but drifts under large changes of pose or lighting.

Classifier
: A model that learns a boundary between categories, such as cat and not-cat, as opposed to a generative model, which learns the whole distribution of plausible examples.

Closed model
: A model reached only through a website or an API, whose parameters stay on the provider's servers and can be changed or withdrawn without notice. It is contrasted with an open-weight model.

Co-creation
: Making creative work together with a generative system. Because such systems mostly behave as executors of instructions rather than as collaborators, co-creation asks a person to shift from craftsperson to creative director.

Collecting society
: An organisation that registers works, matches a use to an owner, and distributes royalties on behalf of authors and performers. Its work depends on ownership databases that are incomplete and inconsistent across countries.

Combinational, exploratory, and transformational creativity
: Margaret Boden's three kinds of creativity: combinational puts familiar ideas together in unfamiliar ways, exploratory moves around inside an existing conceptual space, and transformational changes the conceptual space itself so that previously impossible ideas become thinkable.

Conditioning
: Any input besides noise that steers what a generative model produces, such as a text prompt, a reference image, a mask, or a control signal.

Context window
: The maximum number of tokens a model can attend to at once, holding the system instructions, the conversation so far, and its own previous replies. Anything outside it was never seen by the model.

Control signal
: An input such as a pose skeleton, an edge map, or a depth map that conditions the shape and composition of a generated image, sound, or video rather than its content.

ControlNet
: A small network trained to inject a spatial signal, such as a pose or an edge map, into a diffusion model's denoiser. Several can be stacked at once to control composition from more than one source.

Convolutional network
: A network architecture that slides small parameter patches across an image, the dominant approach to computer vision for most of the 2010s.

Data
: What went into a generative system: which material, gathered from whom, with what consent and whose labour. It is the first of the book's five layers, alongside model, interface, practice, and culture.

Data type
: This book's term for a kind of data a model takes in or puts out: text, image, audio, video, 3D geometry, motion data. The field calls the same thing a modality, and a model that takes several data types is a multimodal model.

Data workers
: People, often in low-wage countries, who label images, rank model outputs, and write fine-tuning examples. They are the reason a model behaves the way it does, and some carry the psychological cost of moderating violent or abusive material.

Dataflow programming
: A style of programming in which boxes process data and the connections drawn between them carry it from one box to the next. Audio-specific graphical languages such as Max/MSP and Pure Data work this way, and building in them is usually called patching.

Decolonisation
: In the context of AI, the argument that Western and English-language dominance in training data is not a skewed sample to be corrected but a settled assumption about whose knowledge counts as common. It asks who defines the default rather than how to rebalance a dataset.

Demo reel
: A selected artefact cut from many generation attempts, in which the kept examples are exactly the ones a model happened to get right. It is evidence that a system can sometimes produce a good result, not that it can produce the result you need on demand.

Denoising
: The step-by-step removal of noise that a diffusion model performs to turn a random starting point into a coherent image, sound, or video, usually carried out in a compressed latent space rather than on raw pixels.

Diffusion model
: A generative model trained to remove noise step by step, so that it can turn pure noise into a coherent image, sound, or video.

Distillation
: Training a smaller student model to imitate a larger teacher model, which is how capable models end up small and fast enough to run on a phone.

Distribution
: A way of saying how likely each possible thing is. A generative model implicitly learns a distribution over its training examples and produces new work by sampling from it.

Embedding
: A vector of numbers, learned during training, that stands in for a piece of data such as a voice or a word, placed in a space where similar things sit close together.

Embodiment
: Having a body in a scene, with a height, a reach, and hands that may or may not be one's own. It turns scale from an aesthetic setting into a bodily fact once a person is standing next to a virtual object.

Ethical authorship
: The question of who is the author when a model trained on millions of other people's work assists a maker. It is also the question of what that maker owes the people whose work trained the model, their audience, and themselves in how they describe the result.

Evolutionary algorithm (genetic algorithm)
: A search method that keeps a population of candidate solutions, scores them, and repeatedly makes a new population by copying the better ones with small random changes and recombinations.

Executor and collaborator
: Two ways of framing a generative system: as an executor, which takes a command and returns a finished output, or as a collaborator, which participates in an open-ended process. Agents shift the framing from the first towards the second.

Extended mind
: The philosophical claim, proposed by Clark and Chalmers, that a cognitive process does not stop at the skin. An external resource that is reliably available, readily used, and trusted the way memory is trusted counts as part of the cognitive system rather than an input to it.

Few-shot
: Giving a model two to six worked examples of input and output before the real request, used whenever the format of the answer matters more than what can be stated in adjectives.

Fine-tuning
: Continuing to train a foundation model briefly on a smaller, focused dataset so that it specialises for a task. The cost ranges from a few euros for a lightweight adapter to millions for a full fine-tune of a large model.

Fitness function
: The score an evolutionary algorithm optimises, saying how good a candidate is. When a person supplies the score by choosing favourites instead, the search becomes interactive evolution.

Five layers
: The book's framework for separating what kind of question a claim about a generative system is asking: data, model, interface, practice, and culture.

Flow matching
: A generative method closely related to diffusion but with a simpler training objective, powering several of the strongest image and video models released from 2024 onwards.

Foundation model
: A very large model trained once on broad data and then adapted to many tasks by prompting or fine-tuning.

Gaussian splat
: A scene represented as a very large number of small three-dimensional Gaussians, each with a position, size, orientation, colour, and opacity, optimised until re-rendering it matches a set of input photographs. It renders fast enough to be interactive, but it is a rendering rather than geometry.

Generalisation
: A model's ability to do well on new examples it has never seen. The same mechanism that makes this possible also lets a model produce fluent output that goes beyond what its data actually supports.

Generative adversarial network (GAN)
: A pair of networks trained against each other, a generator producing samples and a discriminator trying to tell them from real data. GANs dominated image generation from 2014 to about 2020 and are now largely retired.

Gesture
: The meaning-bearing part of a movement, the component that communicates something to somebody, as distinct from motion, the measurable displacement a sensor records.

Ghost memory
: Output that feels culturally resonant and quotation-like but cannot be traced to any single source, the moment a generated result feels like a quotation you cannot place.

Guidance scale (CFG)
: A setting, in image and video models, that strengthens the pull of a prompt against the model's own sense of what is plausible. Too high produces rigid, oversaturated results; too low lets the prompt be politely ignored.

H-creativity and P-creativity
: Margaret Boden's distinction between creativity that is historically novel, new to humanity, and creativity that is only psychologically novel, new to the person who produced it.

Hallucination
: A fluent, confident output that is false, a direct consequence of training a model to produce plausible rather than true text.

Human-in-the-loop checkpoint
: A point in an agent's pipeline where it stops and waits for a person, placed where the cost of a wrong decision is high and the cost of asking is low.

In-context learning
: Steering a model's behaviour by writing examples into the prompt rather than by retraining it. It is the mechanism underneath everything marketed as prompt engineering.

Inference
: Using a trained model to produce an output from an input; the parameters do not change.

Inpainting
: Regenerating only a masked region of an image while leaving the rest of the pixels alone, using the same denoising process a diffusion model uses to generate from scratch.

Intentionality
: The question of why a person is making a particular piece of work, since a model can produce many variations cheaply but cannot tell which of them the maker actually meant.

Interactive evolution
: An evolutionary loop in which a person, rather than a written fitness function, selects which candidates survive; used to breed images, shapes, and sounds by eye.

L-system
: A rewriting grammar that repeatedly replaces symbols in a string according to a small set of rules, then reads the result as drawing instructions. It is a common way to generate branching forms such as plants.

Large language model (LLM)
: A transformer trained to predict the next token in text, on which chat, coding, and reasoning behaviours are built.

Latency
: The delay between an action and a system's response. Below about ten milliseconds a response feels caused by the action; beyond it, it feels like a reply, which sets the design budget for anything meant to be played in real time.

Latent space
: A compressed space in which a trained model represents its data, where similar things sit close together. Moving through it produces a variation rather than retrieving a stored record.

Legibility
: The degree to which a person in a room can see what a machine is about to do, such as a limb rising before a robot strikes a surface, which is what lets them play or work alongside it.

Life cycle assessment
: A method for counting the environmental cost of a product or service across its whole life, from the mining and manufacture of hardware through the water and energy used in operation to disposal. It is the wider frame around the energy-per-query figures usually quoted for generative AI.

Live coding
: Writing and changing a program while it runs, so that the sound or image it produces changes with the text. It is performed with the editor projected for the audience, which makes the process of programming part of the work.

LoRA
: A small set of extra weights trained on a handful of images of a subject and layered on top of a frozen open-weight model, so that the subject becomes a word the model knows. It is standard practice for keeping a character consistent across many images.

Loss
: A single number measuring how wrong a model's predictions are on a batch of data. Training repeatedly nudges the model's parameters to reduce it.

Lovelace test
: A test in which a system passes only if it produces an output that its own architects cannot account for, given complete knowledge of its architecture, program, and inputs. It is a demanding bar that most generative systems do not clear.

Mapping and coupling
: An acoustic instrument has a lawful, physically fixed coupling between an action and the sound it produces. An electronic or digital instrument has a mapping instead, an invented link that must have enough continuity for a small change in action to produce a related change in sound, or it cannot be learned by practice.

Markov chain
: A rule-based generative method that draws the next event, such as the next note in a melody, from a table of transition probabilities conditioned on the current state.

Memorisation
: A trained model reproducing something close to a specific training example rather than a general statistical pattern. It is real but rare, and concentrated on examples the training data contained many times over.

MIDI
: A long-standing protocol that carries symbolic musical information, such as which note started, how hard, and what a controller was set to, rather than sound itself. A generative model that produces MIDI writes a score for something else to play, while one that produces audio writes the sound.

Modality
: The field's word for a kind of data a model takes in or puts out, and the word behind multimodal. This book says data type instead, because psychology has long used modality for a human sense, and the two meanings are easy to confuse. Where this book means perception it says sense or sensory modality, or names the sense as auditory, visual, or tactile.

Model
: The trained artefact: a network plus one specific set of parameter values, frozen in a file and published under a family name, a version, and often a size. A model maps an input to an output, and it has no interface, no memory of you, and no data policy of its own.

Model card
: A document a model's creators publish describing what dataset it was trained on, how many parameters it has, what licence it carries, and what limitations they admit to.

Motion and movement
: Movement is the experienced phenomenon, the body travelling through space as felt and perceived. Motion is the measurable version, the physical displacement a sensor records.

Multimodal and multisensory
: Multimodal is the field's name for models and data that take several data types, such as text with images or audio with video. People are multisensory rather than multimodal, since they combine senses rather than data types. Cross-modal correspondences, the reliable matches people make across the senses, keep their established name.

Music question–answering (MQA)
: A machine-learning task in which a system answers questions about a piece of music. Systems that work from audio alone miss what a performance shows, which is why datasets pair audio–video recordings with questions written against both.

Musicking
: Christopher Small's term for music as something people do together rather than as a work to be contemplated. A musicking robot is judged on the same terms, not on an inner musical understanding but on whether a human partner can perceive it, and play with it, as a partner.

Negative prompt
: Text describing what a maker does not want in a generated image, used to suppress recurring failure modes such as blurring or extra fingers. It is often more powerful than expected, and not supported by every tool.

Neural audio codec
: A model that compresses sound into a short sequence of discrete codes, from which a classifier can be trained or a generator can predict new codes to hand to the codec's decoder.

Neural network
: A stack of layers, each of which multiplies its input by a set of parameters, adds a small offset, and passes the result through a simple non-linear function. Stacking this operation many times produces something flexible enough to model very complex patterns.

Neural radiance fields (NeRF)
: A small neural network trained on a set of photographs to predict the colour and density of any point in space seen from any direction, so that a new view is a rendering operation rather than a lookup. It has been mostly superseded for capture work by Gaussian splatting.

Noise field
: A smooth pseudo-random function used to give organic drift to the position, colour, or flow of generated elements, a common building block of procedural generation.

Noisy intermediate-scale quantum (NISQ)
: John Preskill's name for the current era of quantum hardware, in which devices are small and noisy and run without error correction because it would consume most of the qubits they have.

Open-weight model
: A model published as files that can be downloaded and run on one's own machine or servers. Open weights are not the same as open source, since the training data and training code are usually withheld even when the parameters are shared.

Opt-in and opt-out
: Two opposite ways of distributing the burden of consent for training data. Under opt-out every rights holder must find and object to every use; under opt-in every model builder must find and ask every rights holder; either way the burden falls hardest on those with the least capacity to bear it.

Outpainting
: Extending an image beyond its original edges by treating the new area as a masked region for a diffusion model to fill.

Overfitting
: The opposite of generalisation: a model has effectively memorised its training examples and performs poorly on anything else.

Parameters
: The numbers, often billions of them, inside a model that determine which input produces which output. Training adjusts them to reduce a loss, and inference uses them unchanged.

Photogrammetry
: Reconstructing a three-dimensional mesh by matching features across many overlapping photographs and triangulating camera positions from the result. It is a decades-old technique into which machine learning has mostly entered as denoising and feature matching.

Place illusion and plausibility illusion
: Two components of presence in a virtual environment. Place illusion is the feeling of being there, produced by the display responding correctly to how a person moves. Plausibility illusion is the feeling that events are really happening, produced by things responding credibly to the person and to each other.

Presence
: The sensation of being in the place a virtual reality system is showing, decomposed into a place illusion and a plausibility illusion. The strongest evidence for it is behavioural, such as people flinching or keeping away from a virtual edge, rather than what they report believing.

Procedural generation
: Building content such as terrain, levels, textures, or music from an algorithm and a seed rather than authoring every element by hand.

Prompt
: The text (and sometimes images or audio) given to a model to condition its output; the main interface of current generative tools.

Provenance
: A record of where a piece of media came from and how it was made. Because a trained model holds no documents to trace an output back to, provenance has to be supplied by the maker rather than retrieved from the system.

Quantum machine learning
: A research area proposing to run parts of a learning or sampling algorithm on quantum hardware. As of 2026 it has shown no demonstrated advantage for training or running generative models.

Reasoning model
: A model trained to spend extra computation on intermediate steps before answering, of the kind wired into the tool-using loops that carry out agentic tasks over many steps.

Recurrent network
: A network architecture that passes a running summary from one time step to the next, the standard architecture for text and audio until displaced by transformers around 2018.

Recursive subdivision
: Repeatedly splitting a shape, such as a rectangle, into smaller pieces according to a rule, until a stopping condition is reached. It is a classic technique for generating layouts and textures procedurally.

Rule-based system
: A generative or reasoning system whose behaviour is written out by hand as explicit rules, grammars, or constraints rather than learned from data.

Sampler
: The algorithm that walks the denoising path of a diffusion model from noise to a finished result. Different samplers affect both the style of the output and how quickly it settles.

Seed
: The random number that generates a diffusion model's starting noise. The same prompt with the same seed in the same model gives the same result every time, which is what makes controlled comparison possible.

Shot
: The honest unit of video generation in the mid-2020s, since almost every system produces a single continuous take rather than a scene or a film. Cuts between shots are assembled afterwards in an editor.

Spectrogram
: A picture of how a sound's energy is distributed across frequency over time. An analysis system reads one, and a generative system writes one before inverting it back to a waveform.

Stem separation
: Splitting a finished audio mix back into its component parts, such as vocals, drums, and bass, well enough for practical reuse. It is an analysis technique that enables a good deal of remix and post-production work.

Subsumption architecture
: A robot control design in which fast, low-level behaviours run underneath slower, more deliberative ones, so that a machine always has something to do while it works out what to do next.

Supervision
: The reading skill of deciding whether to accept a model's output, spotting what it failed to handle, and judging which of two versions is better. It is the bottleneck in working with generative tools, since a model cannot judge its own work.

Sycophancy
: A model's tendency to agree with or flatter whoever is prompting it rather than to give an accurate or challenging answer, one of the recurring failure modes of language models.

Talking head
: A video of a person, driven from a single photograph or short clip, made to say synthetic speech in that person's likeness. Multilingual versions of the same presenter are a routine feature, and because the technique puts words in an identifiable person's mouth it is a consent and impersonation problem before it is a video problem.

Temperature
: A setting, in text and audio models, that flattens or sharpens the probability distribution before a draw. High temperature makes output more varied and stranger; low temperature makes it safer and more predictable; at zero it stops being random at all.

Text-to-speech
: Converting a piece of text, usually via phonemes, together with a description of a desired voice, into a spoken waveform.

Timbre transfer
: Reconstructing a performance captured in one instrument's or voice's timbre in the learned timbre of another, by encoding the performance into a model's latent space and decoding it back out.

Token
: The unit a language model reads and writes, usually a word piece; Norwegian text uses more tokens than the same text in English.

Tokeniser
: The component that splits text into the tokens a language model reads and writes. Tokenisers are fitted to their training text, so languages far from the dominant training language are chopped into more, smaller, costlier pieces.

Tool (AI product)
: A product built around one or more models, adding an interface, a system prompt, safety filters, and often retrieval, stored memory, or tool calls, together with a data policy and a price. The tool, rather than the model inside it, decides what happens to what you type.

Top-k and top-p
: Settings, in text models, that restrict a draw to the most likely candidates, either the best k of them or the smallest set whose probabilities sum to p. This stops a model from occasionally sampling nonsense from the far tail.

Trace
: The ordered record of what an agent decided, which tool it called, what came back, and what it did next. It is the artefact a person actually supervises, rather than only the agent's final output.

Training
: Repeatedly adjusting a model's parameters to reduce a loss measured on batches of data.

Transformer
: An architecture, introduced in 2017, that lets every element of a sequence look at every other element directly. It became the dominant architecture for language and, soon after, for audio, image, and code.

Version (of a model)
: The label that fixes which trained artefact a claim is about, since a family name is reused across retrainings. A claim about a model's behaviour carries a version or a date, because the same commercial name in March and in October need not name the same model.

Translation between data types
: Carrying a piece of work from one data type into another through a paragraph that describes it, then editing that paragraph and regenerating. It is a working method for using a multimodal model productively rather than only for critique, and the field often calls it cross-modal translation.

Videogram and motiongram
: A videogram is a single still image built by collapsing a video's frame-to-frame pixels into a strip, with one axis as time and the other as space. A motiongram does the same with frame-to-frame differences rather than the original pixels, so that movement shows up as visible bands.

Virtual, augmented, and mixed reality (VR, AR, MR)
: Virtual reality replaces what a person sees and hears with a computed environment. Augmented reality leaves the world in place and adds graphics registered to it. Mixed reality is augmented content that is also aware of the room, able to hide behind real furniture and rest on real surfaces.

Vocoder
: A system that synthesises an audio waveform from a compressed representation of speech. Neural vocoders were an early step in the transformation of text-to-speech quality, later followed by transformer-based systems.

Voice cloning
: Generating speech in a specific person's voice from a short reference recording. Because a convincing copy of a voice can defraud, harass, or impersonate the person it came from, cloning without consent is harmful and, in a growing number of jurisdictions, unlawful.

WebXR
: An open browser standard that lets the same web page run on a phone or in a headset browser and request whatever level of immersion the device can provide, so that a scene built once is viewable across hardware.

World model
: A generative model whose output is a navigable state or environment that responds to input, rather than a single finished artefact, such as a system that infers which parts of a video game's imagery a player's actions caused.

XR (extended reality)
: The umbrella term covering virtual, augmented, and mixed reality, used when the distinction between them does not matter or a single device supports more than one.
```
