'''
O arquivo gera o código de um microserviço.
'''

import os
import yaml

def gerar_arquivo_microservico(servico, opcionais, services_file="sources/services.yaml", sources_dir="sources", build_dir="build"):
    def parse_base_file(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = {"Imports": "", "Tabela querry": "", "Código próprio": "", "Serviço": ""}
        current_section = None

        for line in content.splitlines():
            line_stripped = line.strip()
            if line_stripped.startswith("#"):
                if "Imports" in line_stripped:
                    current_section = "Imports"
                elif "Tabela querry" in line_stripped:
                    current_section = "Tabela querry"
                elif "Código próprio" in line_stripped:
                    current_section = "Código próprio"
                elif "Serviço" in line_stripped:
                    current_section = "Serviço"
            elif current_section:
                sections[current_section] += line + "\n"

        return sections

    try:
        with open(services_file, "r", encoding="utf-8") as file:
            services_config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{services_file}' não encontrado.")
        return

    if servico not in services_config:
        print(f"❌ Serviço '{servico}' não encontrado em {services_file}")
        return

    base_file = os.path.join(sources_dir, "services", f"{servico}.base")
    if not os.path.exists(base_file):
        print(f"⚠️  Ignorando '{servico}': arquivo base '{base_file}' não encontrado.")
        return

    config = services_config[servico]
    bd = config.get("bd", servico)
    port = config.get("port", "5000")
    db_config = {
        "host": config.get("host", "localhost"),
        "user": config.get("user", "root"),
        "password": config.get("password", "")
    }

    sections = parse_base_file(base_file)

    codigo_proprio = sections['Código próprio'].strip()

    for service in services_config:
        if f"{{{service}_port}}" in codigo_proprio:
            codigo_proprio = codigo_proprio.strip().replace(f"{{{service}_port}}", str(services_config[f"{service}"]['port']))

    final_code = (
        f"# Código gerado automaticamente pela linha de produto de software para o microserviço '{servico}'\n\n"
        f"import mysql.connector\n"
        f"{sections['Imports'].strip()}\n\n"
        f"opcionais = {repr(opcionais)}\n\n"
        f"def connect_{bd}():\n"
        f"    return mysql.connector.connect(user='{db_config['user']}', password='{db_config['password']}', "
        f"host='{db_config['host']}', port=\"3306\", database=\"{bd}_db\")\n\n"
        f"def criar_banco_{bd}():\n"
        f"    conn = mysql.connector.connect(\n"
        f"    host='{db_config['host']}',\n"
        f"    user='{db_config['user']}',\n"
        f"    password='{db_config['password']}'\n"
        f"    )\n"
        f"    cursor = conn.cursor()\n"
        f"    cursor.execute(\"CREATE DATABASE IF NOT EXISTS {bd}_db\")\n"
        f"    conn.close()\n\n"
        f"def criar_tabela_{bd}():\n"
        f"    db = connect_{bd}()\n"
        f"    cursor = db.cursor()\n"
        f"    cursor.execute(\"CREATE TABLE IF NOT EXISTS {bd} {sections['Tabela querry'].strip()}\")\n"
        f"    db.commit()\n"
        f"    db.close()\n\n"
        f"{codigo_proprio}\n"
    )

    os.makedirs(build_dir, exist_ok=True)
    output_path = os.path.join(build_dir, f"{servico}.py")

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(final_code)

    server = sections['Serviço'].strip()

    main_service_template = """
if __name__ == "__main__":
    print("Serviço do microserviço {servico} iniciado!")
    app.run(host="0.0.0.0", port={port})
"""

    final_serice = (
        f"# Código de serviço gerado automaticamente pela linha de produto de software para o microserviço '{servico}'\n\n"
        f"{server}\n\n"
        f"{main_service_template.strip().format(port=port, servico=servico)}"
    )

    output_path = os.path.join(build_dir, f"{servico}_service.py")

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(final_serice)

    print(f"✅ Serviço do microserviço '{servico}_service' gerado em {output_path}")

def gerar_gui(features, build_dir="build"):
    gui_code = (
        "# Código do GUI gerado automaticamente pela linha de produto de software\n"
        "import tkinter as tk\n"
        "from tkinter import ttk\n"
    )

    for feature in features:
        gui_code += f"from {feature} import criar_banco_{feature}, criar_tabela_{feature}, {feature}_app\n"

    gui_code += "\n\nclass main_gui:\n"
    gui_code += "    def __init__(self, root):\n"
    gui_code += "        self.root = root\n"
    gui_code += "        self.root.title(\"E-commerce SPL - GUI Principal\")\n"
    gui_code += "        self.notebook = ttk.Notebook(self.root)\n"
    gui_code += "        self.notebook.pack(expand=True, fill=\"both\")\n\n"

    for feature in features:
        gui_code += f"        {feature}_frame = ttk.Frame(self.notebook)\n"
        gui_code += f"        self.notebook.add({feature}_frame, text=\"{feature.capitalize()}\")\n"
        gui_code += f"        {feature}_app({feature}_frame)\n\n"

    gui_code += "\n\ndef gerenciar_database():\n"
    for feature in features:
        gui_code += f"    criar_banco_{feature}()\n"
        gui_code += f"    criar_tabela_{feature}()\n"
    gui_code += "\n"

    gui_code += "\nif __name__ == \"__main__\":\n"
    gui_code += "    gerenciar_database()\n"
    gui_code += "    root = tk.Tk()\n"
    gui_code += "    app = main_gui(root)\n"
    gui_code += "    root.mainloop()\n"

    output_path = os.path.join(build_dir, f"gui.py")

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(gui_code)

    print(f"✅ Gerado o GUI em {output_path}")