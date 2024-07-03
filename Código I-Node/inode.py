# Importa o módulo tkinter como tk
import tkinter as tk
# Importa simpledialog e messagebox do tkinter
from tkinter import simpledialog, messagebox
# Importa os módulos os e io
import os
import io

# Define a classe INode para representar um nó no sistema de arquivos
class INode:
    # Inicializa um nó com nome e indica se é um diretório
    def __init__(self, name, is_directory=False):
        self.name = name  # Nome do nó
        self.is_directory = is_directory  # Se é um diretório
        self.children = [] if is_directory else None  # Filhos (para diretórios)
        self.content = None if is_directory else io.StringIO()  # Conteúdo (para arquivos)

    # Adiciona um filho ao nó (apenas para diretórios)
    def add_child(self, child):
        if self.is_directory:
            self.children.append(child)

# Define a classe FileSystem para gerenciar o sistema de arquivos
class FileSystem:
    # Inicializa o sistema de arquivos com um diretório raiz
    def __init__(self):
        self.root = INode("/", True)

    # Encontra um nó no caminho especificado
    def find_node(self, path):
        print(f"find_node: Finding node at path: {path}")
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        current_node = self.root
        for part in parts:
            if current_node.is_directory:
                found = False
                for child in current_node.children:
                    if child.name == part:
                        current_node = child
                        found = True
                        break
                if not found:
                    return None
            else:
                return None
        return current_node

    # Adiciona um nó ao caminho especificado
    def add_node(self, path, name, is_directory=False):
        print(f"add_node: Adding node '{name}' at path '{path}', is_directory={is_directory}")
        parent_node = self.find_node(path)
        if parent_node and parent_node.is_directory:
            new_node = INode(name, is_directory)
            parent_node.add_child(new_node)
            return new_node
        return None

    # Lista o conteúdo de um diretório
    def list_directory(self, path):
        print(f"list_directory: Listing directory at path: {path}")
        node = self.find_node(path)
        if node and node.is_directory:
            content = []
            for child in node.children:
                if child.is_directory:
                    content.append(f"[D] {child.name}")
                else:
                    content.append(f"[F] {child.name}")
            return content
        return None

    # Cria um arquivo com conteúdo especificado
    def create_file(self, path, name, content):
        print(f"create_file: Creating file '{name}' at path '{path}' with content: {content}")
        node = self.add_node(path, name, False)
        if node:
            node.content.write(content)
            return f"Arquivo {name} criado com sucesso."
        return f"Erro ao criar o arquivo {name}."

    # Lê o conteúdo de um arquivo
    def read_file(self, path):
        print(f"read_file: Reading file at path: {path}")
        node = self.find_node(path)
        if node and not node.is_directory:
            node.content.seek(0)
            return node.content.read()
        return "Erro ao ler o arquivo."

    # Edita o conteúdo de um arquivo
    def edit_file(self, path, new_content):
        print(f"edit_file: Editing file at path: {path} with new content: {new_content}")
        node = self.find_node(path)
        if node and not node.is_directory:
            node.content = io.StringIO(new_content)
            return f"Arquivo {path} editado com sucesso."
        return "Erro ao editar o arquivo."

    # Deleta um nó no caminho especificado
    def delete_node(self, path):
        print(f"delete_node: Deleting node at path: {path}")
        parts = path.strip("/").split("/")
        if len(parts) == 1:
            return "Erro: Não é possível remover o diretório raiz."
        parent_path = "/" + "/".join(parts[:-1])
        node_name = parts[-1]
        parent_node = self.find_node(parent_path)
        if parent_node and parent_node.is_directory:
            for child in parent_node.children:
                if child.name == node_name:
                    parent_node.children.remove(child)
                    return f"Arquivo ou diretório {node_name} removido com sucesso."
        return "Erro ao remover o arquivo ou diretório."

    # Obtém o valor de um atributo de um nó
    def get_attribute(self, path, attribute):
        print(f"get_attribute: Getting attribute '{attribute}' at path: {path}")
        node = self.find_node(path)
        if node:
            return getattr(node, attribute, None)
        return None

    # Define o valor de um atributo de um nó
    def set_attribute(self, path, attribute, value):
        print(f"set_attribute: Setting attribute '{attribute}' to '{value}' at path: {path}")
        node = self.find_node(path)
        if node:
            setattr(node, attribute, value)
            return f"Atributo '{attribute}' definido como '{value}' para o nó em '{path}'."
        return "Erro ao definir atributo: nó não encontrado."

# Define a classe FileSystemApp para a interface gráfica
class FileSystemApp:
    # Inicializa a interface gráfica
    def __init__(self, root):
        self.root = root
        self.root.title("File System Interface")

        self.file_system = FileSystem()  # Instancia o sistema de arquivos
        self.current_path = "/"  # Caminho atual
        self.previous_paths = []  # Lista para armazenar os caminhos visitados

        # Menu
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir Diretório", command=self.change_directory)
        self.file_menu.add_command(label="Diretório Anterior", command=self.go_to_previous_directory)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=root.quit)

        # Rótulos para exibir o caminho atual
        self.path_label = tk.Label(root, text="Caminho Atual:")
        self.path_label.pack()

        self.path_display = tk.Label(root, text=self.current_path, fg="blue")
        self.path_display.pack()

        # Botões para criar, visualizar, editar e remover arquivos e diretórios
        self.create_file_button = tk.Button(root, text="Criar Arquivo", command=self.create_file)
        self.create_file_button.pack()

        self.view_file_button = tk.Button(root, text="Visualizar Arquivo", command=self.view_file)
        self.view_file_button.pack()

        self.edit_file_button = tk.Button(root, text="Editar Arquivo", command=self.edit_file)
        self.edit_file_button.pack()

        self.delete_file_button = tk.Button(root, text="Remover Arquivo", command=self.delete_file)
        self.delete_file_button.pack()

        self.create_dir_button = tk.Button(root, text="Criar Diretório", command=self.create_directory)
        self.create_dir_button.pack()

        self.delete_dir_button = tk.Button(root, text="Remover Diretório", command=self.delete_directory)
        self.delete_dir_button.pack()

        self.list_dir_button = tk.Button(root, text="Listar Diretório", command=self.list_directory)
        self.list_dir_button.pack()

        # Botões para definir e obter atributos
        self.set_attr_button = tk.Button(root, text="Definir Atributo", command=self.set_attr)
        self.set_attr_button.pack()

        self.get_attr_button = tk.Button(root, text="Obter Atributo", command=self.get_attr)
        self.get_attr_button.pack()

    # Atualiza o rótulo de exibição do caminho atual
    def update_path_display(self):
        self.path_display.config(text=self.current_path)

    # Muda o diretório atual
    def change_directory(self):
        new_directory = simpledialog.askstring("Abrir Diretório", "Digite o caminho do diretório:")
        if new_directory and self.file_system.find_node(new_directory):
            self.previous_paths.append(self.current_path)  # Adiciona o diretório atual à lista de caminhos visitados
            self.current_path = new_directory
            self.update_path_display()
        else:
            messagebox.showerror("Erro", "Diretório não encontrado.")

    # Vai ao diretório anterior
    def go_to_previous_directory(self):
        if self.previous_paths:
            previous_directory = self.previous_paths.pop()  # Remove o último caminho visitado da lista
            self.current_path = previous_directory
            self.update_path_display()
        else:
            messagebox.showinfo("Diretório Anterior", "Nenhum diretório anterior disponível.")

    # Cria um arquivo
    def create_file(self):
        file_name = simpledialog.askstring("Criar Arquivo", "Nome do arquivo (com extensão):")
        if file_name:
            content = simpledialog.askstring("Conteúdo do Arquivo", "Digite o conteúdo do arquivo:")
            message = self.file_system.create_file(self.current_path, file_name, content)
            messagebox.showinfo("Criar Arquivo", message)

    # Visualiza o conteúdo de um arquivo
    def view_file(self):
        file_name = simpledialog.askstring("Visualizar Arquivo", "Nome do arquivo (com extensão):")
        if file_name:
            path = os.path.join(self.current_path, file_name).replace("\\", "/")
            content = self.file_system.read_file(path)
            messagebox.showinfo("Conteúdo do Arquivo", content)

    # Edita o conteúdo de um arquivo
    def edit_file(self):
        file_name = simpledialog.askstring("Editar Arquivo", "Nome do arquivo:")
        if file_name:
            path = os.path.join(self.current_path, file_name).replace("\\", "/")
            content = simpledialog.askstring("Novo Conteúdo do Arquivo", "Digite o novo conteúdo do arquivo:")
            message = self.file_system.edit_file(path, content)
            messagebox.showinfo("Editar Arquivo", message)

    # Remove um arquivo
    def delete_file(self):
        file_name = simpledialog.askstring("Remover Arquivo", "Nome do arquivo:")
        if file_name:
            path = os.path.join(self.current_path, file_name).replace("\\", "/")
            if self.file_system.find_node(path):
                message = self.file_system.delete_node(path)
                messagebox.showinfo("Remover Arquivo", message)
            else:
                messagebox.showerror("Erro", "Arquivo não encontrado.")

    # Cria um diretório
    def create_directory(self):
        dir_name = simpledialog.askstring("Criar Diretório", "Nome do diretório:")
        if dir_name:
            new_dir = self.file_system.add_node(self.current_path, dir_name, True)
            if new_dir:
                messagebox.showinfo("Criar Diretório", f"Diretório {dir_name} criado com sucesso.")
            else:
                messagebox.showerror("Erro", "Erro ao criar o diretório.")

    # Remove um diretório
    def delete_directory(self):
        dir_name = simpledialog.askstring("Remover Diretório", "Nome do diretório:")
        if dir_name:
            path = os.path.join(self.current_path, dir_name).replace("\\", "/")
            if self.file_system.find_node(path):
                message = self.file_system.delete_node(path)
                messagebox.showinfo("Remover Diretório", message)
            else:
                messagebox.showerror("Erro", "Diretório não encontrado.")

    # Lista o conteúdo de um diretório
    def list_directory(self):
        contents = self.file_system.list_directory(self.current_path)
        if contents is not None:
            content_text = "\n".join(contents)
            messagebox.showinfo("Conteúdo do Diretório", content_text)
        else:
            messagebox.showerror("Erro", "Erro ao listar o diretório.")

    # Define o valor de um atributo
    def set_attr(self):
        path = simpledialog.askstring("Definir Atributo", "Digite o caminho do nó:")
        attribute = simpledialog.askstring("Definir Atributo", "Digite o nome do atributo:")
        value = simpledialog.askstring("Definir Atributo", "Digite o valor do atributo:")
        if path and attribute and value:
            message = self.file_system.set_attribute(path, attribute, value)
            messagebox.showinfo("Definir Atributo", message)
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

    # Obtém o valor de um atributo
    def get_attr(self):
        path = simpledialog.askstring("Obter Atributo", "Digite o caminho do nó:")
        attribute = simpledialog.askstring("Obter Atributo", "Digite o nome do atributo:")
        if path and attribute:
            value = self.file_system.get_attribute(path, attribute)
            if value is not None:
                messagebox.showinfo("Valor do Atributo", f"O valor do atributo '{attribute}' em '{path}' é '{value}'.")
            else:
                messagebox.showerror("Erro", "Erro ao obter o valor do atributo.")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

# Define a classe LoginApp para a interface de login
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        # Dicionário para armazenar usuários e senhas
        self.users = {"admin": "admin123", "user": "user123"} 
        
        # Elementos da interface de login
        self.username_label = tk.Label(root, text="Usuário:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        
        self.password_label = tk.Label(root, text="Senha:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()
        
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="Registrar", command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.root.destroy()  # Fecha a janela de login
            main_app()  # Abre a aplicação principal
        else:
            messagebox.showerror("Login", "Usuário ou senha incorretos.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users:
            messagebox.showerror("Erro", "Usuário já existe!")
        elif username and password:
            self.users[username] = password
            messagebox.showinfo("Registro", "Usuário registrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Usuário e senha não podem estar vazios!")

# Função para iniciar a aplicação principal
def main_app():
    root = tk.Tk()
    app = FileSystemApp(root)
    root.mainloop()

# Executa a aplicação de login se este arquivo for executado como script principal
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginApp(login_root)
    login_root.mainloop()
