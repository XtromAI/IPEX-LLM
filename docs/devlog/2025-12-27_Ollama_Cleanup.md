# DevLog: Post-Ollama Cleanup and Auto-Start

**Date:** December 27, 2025  
**Status:** ✅ Cleanup plan captured and executed  
**Context:** After moving to Intel's Ollama Portable build (see 2025-12-26 entry), we removed every leftover Python/IPEX artifact and documented how to keep the repo lean.

## Objectives
- Make Ollama Portable the *only* supported inference path.
- Remove legacy scripts/tests/config targeting the conda/IPEX flow.
- Add quality-of-life automation to start the server at logon.
- Capture a plan for DLL/runtime cleanup outside of `ollama-portable/`.

## Actions Completed
1. **Legacy script purge**
   - Deleted `scripts/debug_dll.py`, `dump_deps.py`, `verify_env.py`, `run-inference.py`, `setup-env.ps1`, and `start-ollama.ps1`.
   - Removed `tests/test_setup.py`, which enforced the conda env.
2. **Engine + config rewrite**
   - `src/config.py` now models the Ollama REST options (model, host, generation settings, env overrides).
   - `src/engine.py` is a simple HTTP client for `/api/generate` with health-check and error handling.
   - Updated specs/contracts/tests to match the new architecture.
3. **Docs realignment**
   - `specs/001-core-inference-setup/spec.md` + `quickstart.md` now reference the portable workflow only.
4. **Autostart utility**
   - Added `scripts/register-ollama-autostart.ps1` to create/remove a Scheduled Task that launches `start-ollama-server.ps1` at user logon.
5. **DLL/runtime clean instructions**
   - Documented that only DLLs inside `ollama-portable/` are needed; remove any manually copied Intel runtimes or PATH tweaks left over from the Python/IPEX experiments.

## Cleanup Plan (for historical reference)
| Area | Action |
|------|--------|
| Scripts/tests | delete all conda/IPEX tooling and verification logic |
| Engine/config | rewrite around Ollama REST defaults and env overrides |
| Specs/docs | ensure every onboarding doc references `setup-ollama-portable.ps1` and `start-ollama-server.ps1` |
| Automation | provide a supported way to auto-launch Ollama via Windows Task Scheduler |
| DLL hygiene | remove stray DLL installs outside `ollama-portable/`; rely entirely on Intel's bundled runtime |

## Next Steps
- Optional: add a small REST client sample (Python or PowerShell) to show how apps should interact with the running Ollama server.
- Periodically audit the repo for large binaries or DLLs outside `ollama-portable/` and keep `.gitignore` up to date.
- Monitor Intel’s Ollama releases for newer builds and refresh the setup script when a stable tag is available.
