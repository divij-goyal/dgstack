# Video Prompt Brain

Use this source set for Sora, Veo, Runway, Pika, Kling, and similar text-to-video
or image-to-video prompt work.

## Core Formula

`Subject + action + environment + camera + lighting + style + timing + constraints`

## What Good Video Prompts Do

- Describe motion, not a still image.
- Control camera behavior: locked-off, dolly, orbit, handheld, macro, aerial.
- Define continuity: single shot, no cuts, same subject, stable identity.
- Specify physical details the model can render: weather, fabric, reflections, shadows.
- Keep one main action per clip unless sequencing is supported.

## Prompt Skeleton

```text
Create a [duration/style] video of [subject] doing [specific action] in
[environment]. The camera [movement/lens/framing]. Lighting is [lighting].
Mood is [emotion]. Maintain [continuity constraints]. Avoid [failure modes].
```

## Sources

See `items.json` for source URLs and extracted pattern notes.
