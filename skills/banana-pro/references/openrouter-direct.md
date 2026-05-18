# OpenRouter Direct Reference

Use this reference when a user asks for raw OpenRouter payloads or integration details for Banana Pro / Nano Banana 2.

## Model

Use:

```text
google/gemini-3.1-flash-image-preview
```

OpenRouter labels this model as `Google: Nano Banana 2 (Gemini 3.1 Flash Image Preview)`. It is the Banana Pro target for this skill.

## Endpoint

```text
POST https://openrouter.ai/api/v1/chat/completions
```

OpenRouter image generation uses Chat Completions or Responses. For Gemini-style models that output image and text, send `modalities: ["image", "text"]`.

## Minimal Payload

```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": "Generate a cinematic 16:9 product hero image..."
    }
  ],
  "modalities": ["image", "text"],
  "stream": false,
  "image_config": {
    "aspect_ratio": "16:9",
    "image_size": "2K"
  }
}
```

## Reference Image Payload

Use mixed message content with text plus image URLs. URLs may be public HTTPS URLs or data URLs.

```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Use Image 1 as the product reference and Image 2 as the scene reference. Keep the product identity, color, structure, and proportions unchanged. Generate a 16:9 commercial hero frame..."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/product-reference.png"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,..."
          }
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "stream": false,
  "image_config": {
    "aspect_ratio": "16:9",
    "image_size": "2K"
  }
}
```

## Response Parsing

Generated images are returned on the assistant message. Prefer this path:

```text
choices[0].message.images[].image_url.url
```

Values may be base64 data URLs. Some responses may also include text content; keep the image URL as the generated image artifact and use text only as secondary metadata or notes.

## Supported Image Config

Common aspect ratios:

```text
1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
```

The model page and docs also list extended ratios for `google/gemini-3.1-flash-image-preview`, including very tall or wide ratios such as `1:4`, `4:1`, `1:8`, and `8:1`.

Image size:

```text
0.5K, 1K, 2K, 4K
```

Default to `2K` for this skill unless the user asks for faster/lower-cost drafts or highest-resolution output.

## Headers

Required:

```http
Authorization: Bearer $OPENROUTER_API_KEY
Content-Type: application/json
```

Optional:

```http
HTTP-Referer: https://your-site.example
X-Title: Your App Name
```

## Source Links

- OpenRouter model page: https://openrouter.ai/google/gemini-3.1-flash-image-preview
- OpenRouter image generation docs: https://openrouter.ai/docs/guides/overview/multimodal/image-generation
