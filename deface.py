#!/usr/bin/env python3
"""
DEFACE SIMULATOR - APENAS PARA FINS EDUCACIONAIS
NÃO USE EM SISTEMAS SEM AUTORIZAÇÃO. O USO INDEVIDO É ILEGAL.
Este script simula uma varredura de diretórios e uma tentativa de deface.
Nenhuma ação maliciosa é realmente executada.
"""

import argparse
import requests
import threading
import sys
import time
from colorama import init, Fore, Style

# Inicializa colorama para cores no terminal
init(autoreset=True)

# Wordlist de diretórios e arquivos comuns (pode ser expandida)
WORDLIST = [
    "admin", "administrator", "wp-admin", "wp-login.php", "login.php",
    "user/login", "cpanel", "phpmyadmin", "pma", "upload", "uploads",
    "files", "backup", "backups", "old", "temp", "test", "teste",
    "dev", "private", "restricted", "secure", "config", "configuration",
    ".git", ".env", "shell", "cmd", "exec", "cgi-bin", "xmlrpc.php",
    "wp-content", "wp-includes", "images", "css", "js", "vendor",
    "api", "v1", "v2", "graphql", "server-status", "server-info"
]

# Credenciais padrão para simular ataques de força bruta (apenas simulação)
DEFAULT_CREDS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "123456"),
    ("root", "root"),
    ("user", "user"),
    ("test", "test"),
    ("administrator", "administrator")
]

class DefaceSimulator:
    def __init__(self, target, index_file):
        self.target = target.rstrip('/')
        self.index_file = index_file
        self.found_urls = []
        self.lock = threading.Lock()
        self.threads = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def print_banner(self):
        print(Fore.CYAN + """
        ╔══════════════════════════════════════════╗
        ║     DEFACE SIMULATOR - EDUCACIONAL       ║
        ║  Uso exclusivo para aprendizado e testes ║
        ║       autorizados. Respeite a lei.       ║
        ╚══════════════════════════════════════════╝
        """)

    def check_directory(self, path):
        """Verifica se um diretório/arquivo existe no alvo."""
        url = f"{self.target}/{path}"
        try:
            response = self.session.get(url, timeout=5, allow_redirects=False)
            with self.lock:
                if response.status_code == 200:
                    print(Fore.GREEN + f"[ENCONTRADO] {url} (200 OK)")
                    self.found_urls.append(("200", url, path))
                elif response.status_code == 403:
                    print(Fore.YELLOW + f"[PROIBIDO] {url} (403 - Possível diretório restrito)")
                    self.found_urls.append(("403", url, path))
                elif response.status_code in [301, 302]:
                    print(Fore.BLUE + f"[REDIRECIONAMENTO] {url} ({response.status_code})")
                    self.found_urls.append((str(response.status_code), url, path))
                else:
                    # Não exibe todos os códigos para não poluir
                    pass
        except requests.exceptions.RequestException as e:
            with self.lock:
                print(Fore.RED + f"[ERRO] {url} - {e}")

    def scan(self):
        """Executa a varredura usando múltiplas threads."""
        self.print_banner()
        print(Fore.WHITE + f"\nAlvo: {self.target}")
        print(Fore.WHITE + f"Arquivo de índice local: {self.index_file}")
        print(Fore.WHITE + f"Iniciando varredura com {len(WORDLIST)} entradas...\n")

        start_time = time.time()

        # Cria threads
        for path in WORDLIST:
            thread = threading.Thread(target=self.check_directory, args=(path,))
            thread.start()
            self.threads.append(thread)
            # Pequena pausa para não sobrecarregar
            time.sleep(0.1)

        # Aguarda todas as threads terminarem
        for thread in self.threads:
            thread.join()

        elapsed = time.time() - start_time
        print(Fore.MAGENTA + f"\nVarredura concluída em {elapsed:.2f} segundos.")
        self.analyze_results()

    def analyze_results(self):
        """Analisa os resultados e simula exploração."""
        if not self.found_urls:
            print(Fore.RED + "Nenhum diretório ou arquivo interessante encontrado.")
            return

        print(Fore.CYAN + "\n========== RESULTADOS ENCONTRADOS ==========")
        for status, url, path in self.found_urls:
            print(f"[{status}] {url}")

        print(Fore.CYAN + "\n========== SIMULAÇÃO DE EXPLORAÇÃO ==========")

        # Procura por possíveis painéis de admin
        admin_pages = [url for _, url, path in self.found_urls if 'admin' in path or 'login' in path]
        if admin_pages:
            print(Fore.YELLOW + "\n[!] Possíveis painéis administrativos detectados:")
            for url in admin_pages:
                print(f"    - {url}")
                self.simulate_admin_bruteforce(url)

        # Procura por diretórios de upload
        upload_dirs = [url for _, url, path in self.found_urls if 'upload' in path or 'files' in path]
        if upload_dirs:
            print(Fore.YELLOW + "\n[!] Diretórios de upload encontrados (possível upload de arquivo):")
            for url in upload_dirs:
                print(f"    - {url}")
                self.simulate_upload_exploit(url)

        # Simula tentativa de deface no primeiro diretório raiz que encontrar (se houver)
        root_index = f"{self.target}/index.html"
        try:
            r = self.session.get(root_index, timeout=5)
            if r.status_code == 200:
                print(Fore.GREEN + f"\n[*] Página inicial encontrada em {root_index}")
                self.simulate_deface(root_index)
        except:
            pass

    def simulate_admin_bruteforce(self, admin_url):
        """Simula um ataque de força bruta em um painel admin."""
        print(Fore.LIGHTBLUE_EX + f"    [*] Simulando tentativa de login com credenciais padrão em {admin_url}")
        for user, pwd in DEFAULT_CREDS:
            # Simula um POST de login (apenas simulação, não envia realmente)
            print(f"        Testando {user}:{pwd} ... ", end="")
            time.sleep(0.2)  # simula latência
            # Simulação: suponha que admin/admin funciona
            if user == "admin" and pwd == "admin":
                print(Fore.GREEN + "SUCESSO (SIMULADO)")
                print(Fore.LIGHTGREEN_EX + f"        [!] Credencial válida encontrada! Acesso como admin.")
                break
            else:
                print(Fore.RED + "Falha")
        else:
            print(Fore.LIGHTRED_EX + "    Nenhuma credencial padrão funcionou (simulação).")

    def simulate_upload_exploit(self, upload_url):
        """Simula upload de arquivo malicioso."""
        print(Fore.LIGHTBLUE_EX + f"    [*] Simulando upload de {self.index_file} para {upload_url}")
        # Simula envio de arquivo (sem realmente enviar)
        time.sleep(0.5)
        print(Fore.GREEN + f"    [*] Upload simulado com sucesso! (apenas simulação)")
        print(Fore.LIGHTGREEN_EX + f"    [!] Arquivo pode estar acessível em {upload_url}/index.html")

    def simulate_deface(self, index_url):
        """Simula a substituição da página inicial."""
        print(Fore.LIGHTBLUE_EX + f"\n[*] Tentando substituir {index_url} pelo conteúdo local...")
        time.sleep(1)
        print(Fore.GREEN + f"[*] DEFACE SIMULADO! A página {index_url} foi alterada (apenas simulação).")
        print(Fore.LIGHTYELLOW_EX + f"    Conteúdo do arquivo local {self.index_file} seria inserido.")

def main():
    parser = argparse.ArgumentParser(description="Simulador de Deface (educacional)")
    parser.add_argument("-t", "--target", required=True, help="URL alvo (ex: http://exemplo.com)")
    parser.add_argument("-d", "--index", default="index.html", help="Arquivo HTML local para simular deface (padrão: index.html)")
    args = parser.parse_args()

    # Aviso legal
    print(Fore.RED + Style.BRIGHT + """
    ATENÇÃO: Este script é apenas para fins educacionais e testes autorizados.
    O uso não autorizado contra sistemas de terceiros é ilegal e antiético.
    Certifique-se de ter permissão antes de testar qualquer sistema.
    Pressione Ctrl+C para cancelar ou Enter para continuar...
    """)
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.")
        sys.exit(0)

    simulator = DefaceSimulator(args.target, args.index)
    simulator.scan()

if __name__ == "__main__":
    main()