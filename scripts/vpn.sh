#!/bin/bash

# Verifica o valor do primeiro parâmetro usando case
case "$1" in
	status)
		# Executa o comando para listar as sessões
		output=$(openvpn3 sessions-list)

		# Extrai o caminho do session-path
		session_path=$(echo "$output" | grep -oP '(?<=Path: )/net/openvpn/v3/sessions/\S+')

		# Verifica se o caminho foi encontrado
		if [ -n "$session_path" ]; then
			echo "VPN Ativa"
		else
			echo "VPN desconectada"
		fi
		;;

	conectar)
		# Executa o comando para listar as sessões
		output=$(openvpn3 sessions-list)

		# Extrai o caminho do session-path
		session_path=$(echo "$output" | grep -oP '(?<=Path: )/net/openvpn/v3/sessions/\S+')

		# Verifica se o caminho foi encontrado
		if [ -n "$session_path" ]; then
			echo "Session path encontrado: $session_path"
			
			# Executa o comando de desconexão usando o session_path encontrado
			openvpn3 session-manage --session-path "$session_path" --disconnect
			
			if [ $? -eq 0 ]; then
				echo "VPN desconectada"
			else
				echo "Falha ao desconectar a VPN"
			fi
		else
			echo "Nenhuma VPN encontrada"
		fi

		# Inicia a nova sessão
		output=$(openvpn3 session-start --config config.ovpn)
		echo "VPN conectada."
		;;

	desconectar)
		# Executa o comando para listar as sessões
		output=$(openvpn3 sessions-list)

		# Extrai o caminho do session-path
		session_path=$(echo "$output" | grep -oP '(?<=Path: )/net/openvpn/v3/sessions/\S+')

		# Verifica se o caminho foi encontrado
		if [ -n "$session_path" ]; then
			echo "Session path encontrado: $session_path"

			# Executa o comando de desconexão usando o session_path encontrado
			output=$(openvpn3 session-manage --session-path "$session_path" --disconnect)
			
			if [ $? -eq 0 ]; then
				echo "VPN desconectada"
			else
				echo "Falha ao desconectar a sessão"
			fi
		else
			echo "Nenhuma VPN encontrada"
		fi
		;;

	*)
		echo "Parâmetro inválido ou nenhum parâmetro fornecido. Use 'status', 'conectar' ou 'desconectar'."
		;;
esac

