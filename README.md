# FLUX (Black Forest Labs) API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/black-forest-labs/flux-schnell?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-badge&utm_term=tier-a)

FLUX is the image model family from Black Forest Labs, the Freiburg lab founded by the researchers behind Stable Diffusion. This package is a Python client for the Black Forest Labs API hosted on Synexa: one `pip install` gives you FLUX.1 [schnell] for fast generation, FLUX 1.1 [pro] for top-quality text-to-image, FLUX.1 Kontext [pro] for instruction-based editing and FLUX.2 [klein] 9B for reference-guided image-to-image, all behind the same `run()` call.

The client offers a blocking `run()` that returns image URLs, a submit-then-poll mode, webhook delivery on completion, and typed errors. Its only dependency is `httpx`. It is aimed at developers who want FLUX output inside an application, a batch job or a notebook without downloading 12-billion-parameter checkpoints or managing GPU servers.

> **Try it now:** [https://synexa.ai/explore/black-forest-labs/flux-schnell](https://synexa.ai/explore/black-forest-labs/flux-schnell?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-top&utm_term=tier-a) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About FLUX (Black Forest Labs)](#about-flux-black-forest-labs)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **The 12B FLUX.1 checkpoints want a 24 GB GPU.** In bf16 the transformer alone is around 24 GB, and even the fp8 path needs a high-end consumer card. The hosted endpoint runs on datacenter hardware; your code calls HTTPS.
- **[pro] models are hosted-only anyway.** FLUX 1.1 [pro] and Kontext [pro] are not distributed as weights, so an API is the only way to use them. This client puts them next to the open [schnell] and [klein] models under one interface.
- **No cold start, no environment drift.** Loading FLUX plus its T5 and CLIP encoders takes minutes on a fresh box and breaks whenever diffusers or PyTorch moves. The hosted models stay warm and versioned.
- **Fractions of a cent per image.** [schnell] is $0.0015 per run, [klein] 9B is $0.01, 1.1 [pro] and Kontext [pro] are $0.02, with no hourly GPU charge.

## Installation

```bash
pip install git+https://github.com/black-forest-labs-dev/flux-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-apikey&utm_term=tier-a)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import flux_api

output = flux_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from flux_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`black-forest-labs/flux-schnell`](https://synexa.ai/explore/black-forest-labs/flux-schnell?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-models&utm_term=tier-a) | text-to-image | The fastest image generation model tailored for local development and personal use | $0.0015 |
| [`black-forest-labs/flux-1.1-pro`](https://synexa.ai/explore/black-forest-labs/flux-1.1-pro?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-models&utm_term=tier-a) | text-to-image | Faster, better FLUX Pro. Text-to-image model with excellent image quality, prompt adherence, and output diversity. | $0.02 |
| [`black-forest-labs/flux-kontext-pro`](https://synexa.ai/explore/black-forest-labs/flux-kontext-pro?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-models&utm_term=tier-a) | text-to-image | A state-of-the-art text-based image editing model that delivers high-quality outputs with excellent prompt following and consistent results for transforming images through natural language | $0.02 |
| [`black-forest-labs/flux-2-klein-9b`](https://synexa.ai/explore/black-forest-labs/flux-2-klein-9b?utm_source=github&utm_medium=ugc&utm_campaign=black-forest-labs-dev&utm_content=readme-models&utm_term=tier-a) | image-to-image | 4-step distilled version of FLUX.2 [klein], a 9B foundation image model offering maximum flexibility and control for fast text-to-image and image-to-image generation. | $0.01 |

The default model is **`black-forest-labs/flux-schnell`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `black-forest-labs/flux-schnell`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `random` | — | Random seed. Set for reproducible generation |
| `prompt` | string | yes | `black forest gateau cake spelling out th…` | — | Text prompt for image generation |
| `go_fast` | boolean | no | `True` | — | Run faster predictions with model optimized for speed (currently fp8 quantized); disable to run in original bf16 |
| `megapixels` | string | no | `1` | 1, 0.25 | Approximate number of megapixels for generated image |
| `num_outputs` | integer | no | `1` | 1, 4 | Number of outputs to generate |
| `aspect_ratio` | string | no | `1:1` | 1:1, 16:9, 21:9, 3:2, 2:3, 4:5, 5:4, 3:4, 4:3, 9:16, 9:21 | Aspect ratio for the generated image |
| `output_format` | string | no | `webp` | webp, jpg, png | Format of the output images |
| `output_quality` | integer | no | `80` | 0, 100 | Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs |
| `num_inference_steps` | integer | no | `4` | 1, 4 | Number of denoising steps. 4 is recommended, and lower number of steps produce lower quality outputs, faster. |
| `disable_safety_checker` | boolean | no | `False` | — | Disable safety checker for generated images. |

### `black-forest-labs/flux-1.1-pro`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `random` | — | Random seed. Set for reproducible generation |
| `width` | integer | no | `1024` | 256, 1440 | Width of the generated image in text-to-image mode. Only used when aspect_ratio=custom. Must be a multiple of 32 (if it's not, it will be rounded to nearest multiple of 32). Note: Ignored in img2img and inpainting modes. |
| `height` | integer | no | `1024` | 256, 1440 | Height of the generated image in text-to-image mode. Only used when aspect_ratio=custom. Must be a multiple of 32 (if it's not, it will be rounded to nearest multiple of 32). Note: Ignored in img2img and inpainting modes. |
| `prompt` | string | yes | `black forest gateau cake spelling out th…` | — | Text prompt for image generation |
| `aspect_ratio` | string | no | `1:1` | custom, 1:1, 16:9, 21:9, 3:2, 2:3, 4:5, 5:4, 3:4, 4:3, 9:… | Aspect ratio for the generated image |
| `image_prompt` | file | no | — | — | Image to use with Flux Redux. This is used together with the text prompt to guide the generation towards the composition of the image_prompt. |
| `output_format` | string | no | `webp` | webp, jpg, png | Format of the output images |
| `output_quality` | integer | no | `80` | 0, 100 | Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs |
| `safety_tolerance` | integer | no | `2` | 1, 6 | Safety tolerance, 1 is most strict and 6 is most permissive |
| `prompt_upsampling` | boolean | no | `False` | — | Automatically modify the prompt for more creative generation |

### `black-forest-labs/flux-kontext-pro`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `random` | — | Random seed. Set for reproducible generation |
| `prompt` | string | yes | `Make this a 90s cartoon` | — | Text description of what you want to generate, or the instruction on how to edit the given image. |
| `input_image` | file | yes | `https://files.synexa.ai/models/black-for…` | — | Input image to start generating from |
| `aspect_ratio` | string | no | `match_input_image` | match_input_image, 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4… | Aspect ratio of the generated image. Use 'match_input_image' to match the aspect ratio of the input image. |
| `output_format` | string | no | `jpg` | jpg, png | Output format for the generated image |

### `black-forest-labs/flux-2-klein-9b`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `change this girl to boy` | — | Text prompt for image generation |
| `input_images` | files | no | `['https://files.synexa.ai/models/black-f…` | — | List of reference images for image-to-image generation (max 5) |
| `seed` | integer | no | `random` | — | Random seed for reproducible generation |
| `steps` | integer | no | `4` | 1, 8 | Number of inference steps |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from flux_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About FLUX (Black Forest Labs)

FLUX is a family of text-to-image and image-editing models from [Black Forest Labs](https://github.com/black-forest-labs/flux), a company founded in 2024 by Robin Rombach and other members of the original Stable Diffusion team. The first generation, FLUX.1, was released in August 2024 as a 12-billion-parameter rectified-flow transformer that combined a T5 text encoder with CLIP, which gave it markedly better prompt adherence, hands and in-image text than the SDXL generation it replaced. It shipped in three tiers: [pro] (API only), [dev] (open weights, non-commercial licence) and [schnell] (open weights, Apache 2.0, distilled to run in one to four steps).

Later releases extended the family. FLUX 1.1 [pro], released in October 2024, is a faster and higher-fidelity successor to the original [pro] tier and adds Redux-style image prompting and optional prompt upsampling. FLUX.1 Kontext, released in 2025, is an in-context editing model: you give it an image and a natural-language instruction ("make the jacket red", "remove the person on the left") and it edits the image while preserving everything else. FLUX.2 is the second generation of the architecture, and FLUX.2 [klein] is its compact line; the 9B variant served here is a 4-step distillation that handles both text-to-image and image-to-image with up to five reference images.

Through this client, `flux-schnell` (default) and `flux-1.1-pro` are text-to-image with a `prompt`; `flux-kontext-pro` additionally requires an `input_image` to edit; `flux-2-klein-9b` accepts up to five `input_images` as references. Every endpoint returns one or more image URLs; the full parameter list for each is in the Parameters section above.

The hosted endpoints used by this client are Black Forest Labs' own models served on Synexa under the `black-forest-labs/*` namespace. The open FLUX.1 [schnell] and [dev] weights and reference inference code are available in the official repository if you prefer to self-host; the [pro] tiers exist only as hosted models.

**Official project:** https://github.com/black-forest-labs/flux

## Use cases

- **High-volume placeholder imagery** — call `run({"prompt": ..., "num_outputs": 4})` on `flux-schnell` at $0.0015 a run to fill a CMS, a mock storefront or a test fixture set.
- **Hero images for landing pages** — switch to `model="black-forest-labs/flux-1.1-pro"` with `prompt_upsampling=True` when quality and typography matter more than cost.
- **Instruction-based photo editing** — send `{"prompt": "replace the sky with a sunset", "input_image": url}` to `flux-kontext-pro` and get the edited image back with the rest of the scene intact.
- **Brand-consistent variations** — pass up to five product shots as `input_images` to `flux-2-klein-9b` with a prompt describing the new scene to keep colours and shapes consistent across a campaign.
- **Reproducible A/B image tests** — fix the `seed` and vary only the prompt so two candidates differ in exactly one variable.
- **Async generation behind a queue** — submit with `wait=False` and a `webhook` from a web request handler and let the callback write the URL to your database.

## FAQ

**Is there a Black Forest Labs (FLUX) API?**

Black Forest Labs runs its own API for the [pro] models, and the open [schnell] and [dev] weights are on GitHub and Hugging Face. This package is an independent Python client for four FLUX endpoints hosted on Synexa, covering the open and the [pro] tiers behind one interface.

**How much does the FLUX API cost?**

Per run on Synexa: `flux-schnell` $0.0015, `flux-2-klein-9b` $0.01, `flux-1.1-pro` $0.02, `flux-kontext-pro` $0.02. Billing is per prediction with no idle GPU charge; new accounts receive a free trial credit.

**Can I run FLUX without a GPU?**

Yes. With this client inference happens on Synexa's GPUs and your code receives image URLs; you need only Python 3.8+ and `httpx`. Self-hosting FLUX.1 needs a CUDA GPU with roughly 24 GB of VRAM for the bf16 weights, and the [pro] models cannot be self-hosted at all.

**Does this client work with the black-forest-labs/flux repo, diffusers or ComfyUI?**

No. It does not load local checkpoints, LoRAs or ComfyUI workflows; it is an HTTP client for the hosted endpoints. Use the official repository or diffusers if you need offline inference or custom fine-tunes.

**What input formats does it accept?**

Input is a JSON object. `prompt` (string) is required on every model. `flux-kontext-pro` also requires `input_image` as a publicly reachable image URL; `flux-2-klein-9b` accepts up to five `input_images` URLs; `flux-1.1-pro` accepts an `image_prompt` URL. Output is one or more image URLs in the requested `output_format` (`webp`, `jpg` or `png` where supported).

**Is this the official FLUX SDK?**

No. This is an independent, MIT-licensed client and is not affiliated with Black Forest Labs. The official project is at https://github.com/black-forest-labs/flux.

## Related

- [black-forest-labs/flux](https://github.com/black-forest-labs/flux) — official repository with the open FLUX.1 weights and reference inference code.
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose client for every model on the platform.
- [black-forest-labs/flux-kontext-pro](https://synexa.ai/explore/black-forest-labs/flux-kontext-pro) — instruction-based image editing, also supported by this client.
- [tongyi/z-image-turbo](https://synexa.ai/explore/tongyi/z-image-turbo) — a 6B few-step text-to-image model with strong bilingual text rendering.
- [bytedance/seedream-5-pro-edit](https://synexa.ai/explore/bytedance/seedream-5-pro-edit) — region-precise editing when you need to change one element and leave the rest untouched.

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of FLUX (Black Forest Labs). Model weights and trademarks belong to their respective owners.

_Last reviewed: 2026-09-22_
