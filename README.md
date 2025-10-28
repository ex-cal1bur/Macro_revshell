# Macro_revshell

> Herramienta de automatización para generación de macros VBA con reverse shell

## 📋 Descripción

**Macro_revshell** genera macros VBA maliciosas que establecen reverse shells mediante PowerShell y Powercat. Incluye servidor web integrado para servir payloads.

## 🚀 Características

- 🔄 Generación automática de macros con reverse shell
- 🌐 Servidor web integrado 
- 🔐 Codificación Base64 UTF-16LE
- 🎯 Detección automática de IP
- 📊 División inteligente de payloads

## 🛠️ Uso Rápido

```bash
# 1. Preparar powercat.ps1 en el directorio
wget https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1

# 2. Ejecutar script
python macro_revshell.py

# 3. Iniciar listener (en otra terminal)
nc -lvnp 4444

# 4. Copiar macro generada en Word
