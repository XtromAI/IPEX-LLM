# Ollama CLI Helper
# Usage: .\ollama-cli.ps1 run deepseek-r1:7b
param([Parameter(ValueFromRemainingArguments)]$Args)

$OllamaPath = "C:\Users\creks\Documents\IPEX-LLM\ollama-portable"
$env:PATH = "$OllamaPath;$env:PATH"

& "$OllamaPath\ollama.exe" @Args
