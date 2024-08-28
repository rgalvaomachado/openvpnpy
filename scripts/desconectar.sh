#!/bin/bash

# Executa o script status.sh e armazena o resultado em uma variável
output=$(./status.sh)

# Extrai o caminho do session-path
session_path=$(echo "$output" | grep -oP '(?<=Path: )/net/openvpn/v3/sessions/\S+')

# Verifica se o caminho foi encontrado
if [ -n "$session_path" ]; then
  echo "Session path encontrado: $session_path"
  
  # Executa o comando de desconexão usando o session_path encontrado
  openvpn3 session-manage --session-path "$session_path" --disconnect
  
  if [ $? -eq 0 ]; then
    echo "VPN desconectada."
  else
    echo "Falha ao desconectar a VPN."
  fi
else
  echo "Session path não encontrado."
fi
