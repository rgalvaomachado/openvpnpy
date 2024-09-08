import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
import subprocess

# Caminho para o arquivo JSON que armazenará o caminho do .ovpn
CONFIG_FILE = 'openvpn_config.json'
# Diretório onde os arquivos .ovpn importados serão armazenados
OVPN_DIR = 'ovpn_configs'

# Certifique-se de que o diretório de configuração existe
if not os.path.exists(OVPN_DIR):
    os.makedirs(OVPN_DIR)

# Função para carregar o arquivo JSON
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Função para salvar o caminho do arquivo .ovpn no JSON
def save_config(config_data):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config_data, file)

# Função para importar o arquivo .ovpn
def import_ovpn():
    file_path = filedialog.askopenfilename(filetypes=[("OVPN files", "*.ovpn")])
    if file_path:
        # Copia o arquivo para o diretório do projeto
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(OVPN_DIR, file_name)
        shutil.copy(file_path, dest_path)

        # Salva o caminho no arquivo de configuração
        config_data['ovpn_file'] = dest_path
        save_config(config_data)
        update_status()
        messagebox.showinfo("Sucesso", "Arquivo OVPN importado com sucesso!")

# Função para atualizar o status do arquivo importado
def update_status():
    # Lista as sessões OpenVPN ativas
    try:
        result = subprocess.run(['openvpn3', 'sessions-list'], stdout=subprocess.PIPE, check=True, text=True)
        output = result.stdout

        # Procura pelo caminho da sessão ativa
        session_path = None
        for line in output.splitlines():
            if 'Path: ' in line:
                session_path = line.split('Path: ')[1].strip()
                break

        if session_path:
            vpn_status_label.config(text="Conectado")
            update_vpn_status("Conectado")
        else:
            vpn_status_label.config(text="Desconectado")
            update_vpn_status("Desconectado")

        ovpn_file = config_data.get('ovpn_file')
        if ovpn_file:
            status_label.config(text=f"Arquivo OVPN importado")
        else:
            status_label.config(text="Nenhum arquivo OVPN importado.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Falha ao verificar o status da VPN.")

# Função para conectar usando o arquivo OVPN importado
def connect_vpn():
    ovpn_file = config_data.get('ovpn_file')
    if ovpn_file:
        try:
            # Lista as sessões OpenVPN ativas
            result = subprocess.run(['openvpn3', 'sessions-list'], stdout=subprocess.PIPE, check=True, text=True)
            output = result.stdout

            # Procura pelo caminho da sessão ativa
            session_path = None
            for line in output.splitlines():
                if 'Path: ' in line:
                    session_path = line.split('Path: ')[1].strip()
                    break

            if session_path:
                # Desconecta a sessão ativa
                subprocess.run(['openvpn3', 'session-manage', '--session-path', session_path, '--disconnect'], check=True)

            # Conecta à VPN usando o arquivo .ovpn
            subprocess.run(['openvpn3', 'session-start', '--config', ovpn_file], check=True)
            messagebox.showinfo("Conectado", "Conectado à VPN com sucesso.")
            update_vpn_status("Conectado")
            vpn_status_label.config(text="Conectado")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erro", "Falha ao conectar à VPN.")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo OVPN importado.")

# Função para desconectar a VPN
def disconnect_vpn():
    try:
        # Lista as sessões OpenVPN ativas
        result = subprocess.run(['openvpn3', 'sessions-list'], stdout=subprocess.PIPE, check=True, text=True)
        output = result.stdout

        # Procura pelo caminho da sessão ativa
        session_path = None
        for line in output.splitlines():
            if 'Path: ' in line:
                session_path = line.split('Path: ')[1].strip()
                break

        if session_path:
            # Desconecta a sessão ativa
            subprocess.run(['openvpn3', 'session-manage', '--session-path', session_path, '--disconnect'], check=True)
            messagebox.showinfo("Desconectado", "Desconectado da VPN com sucesso.")
            update_vpn_status("Desconectado")
            vpn_status_label.config(text="Desconectado")
        else:
            messagebox.showinfo("Desconectado", "Nenhuma sessão VPN ativa encontrada.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Falha ao desconectar da VPN.")

# Função para verificar o status da VPN e atualizar a bolinha
def update_vpn_status(status):
    if status == "Conectado":
        vpn_status_canvas.itemconfig(vpn_status, fill="green")
    else:
        vpn_status_canvas.itemconfig(vpn_status, fill="red")

# Carregar a configuração ao iniciar
config_data = load_config()

# Criar a interface gráfica
root = tk.Tk()
root.title("OpenVpn")

# Label para mostrar o status do arquivo importado
vpn_status_title = tk.Label(root, text="Status VPN")
vpn_status_title.pack(pady=5)

# Canvas para mostrar o status da VPN
vpn_status_canvas = tk.Canvas(root, width=50, height=50)
vpn_status = vpn_status_canvas.create_oval(10, 10, 30, 30, fill="red")  # Vermelho indica desconectado
vpn_status_canvas.pack(pady=10)

vpn_status_label = tk.Label(root, text="")
vpn_status_label.pack(pady=5)

# Botão para conectar à VPN
connect_button = tk.Button(root, text="Conectar VPN", command=connect_vpn)
connect_button.pack(pady=10)

# Botão para desconectar da VPN
disconnect_button = tk.Button(root, text="Desconectar VPN", command=disconnect_vpn)
disconnect_button.pack(pady=10)

# Label para mostrar o status do arquivo importado
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Botão para importar o arquivo OVPN
import_button = tk.Button(root, text="Importar OVPN", command=import_ovpn)
import_button.pack(pady=10)

# Atualiza o status ao iniciar o programa
update_status()

# Iniciar o loop da interface gráfica
root.mainloop()
