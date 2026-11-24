# Nuke–ComfyUI Bridge (`nuke-comfyui-bridge`)

A production-oriented bridge connecting **Foundry NukeX 17** with local or headless **ComfyUI** inference servers. Built to bring custom diffusion, ControlNet, and segmentation workflows directly into a feature-film compositing pipeline without breaking 32-bit float or ACES color management.

> **Status:** Active Pre-Alpha / Architecture & API Prototyping  
> **Target Environment:** Foundry NukeX 17.x (Python 3.11+ / PySide6 / VFX Reference Platform)

---

## Motivation
Modern AI/ML tools in ComfyUI offer rapid iteration for clean-plate generation, depth/normal relighting, and generative inpainting, but current workflows force compositors out of Nuke into 8-bit/16-bit sRGB workarounds. This bridge treats ComfyUI as a headless, background ML compute engine controlled natively from Nuke's node graph.

## Core Features (Planned & In-Progress)
- **Non-Blocking PySide6 UI & Gizmo:** Submit frames or sequences to a local/remote ComfyUI server via WebSocket/REST without locking the Nuke UI thread.
- **Color-Managed I/O (ACES 2.0 / OCIO):** Automated pre-inference log/sRGB/linear transforms and post-inference inverse transforms to preserve 32-bit float EXR plate integrity.
- **Multi-Pass Node Routing:** Pass Nuke `rgba`, `depth.Z`, `normal`, and `alpha` channels directly into ComfyUI ControlNet and mask inputs.
- **Headless Workflow Execution:** Load and parameterize exported ComfyUI API `.json` graphs directly inside Nuke node knobs.

## Roadmap
- [x] Standalone Python WebSocket/REST client for ComfyUI API job queuing and progress polling
- [ ] OpenImageIO (OIIO) 32-bit EXR ↔ tensor pre/post-processing pipeline
- [ ] NukeX 17 PySide6 panel and custom `ComfyBridge` Gizmo/Group wrapper
- [ ] Sequence batching and frame-range caching with Nuke's localization system

## License
Distributed under the MIT License. See `LICENSE` for more information.
