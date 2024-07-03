# Importa a biblioteca tkinter e suas funcionalidades de messagebox e simpledialog
import tkinter as tk
from tkinter import messagebox, simpledialog

# Classe para representar um sistema de arquivos
class FileSystem:
    # Método de inicialização da classe FileSystem
    def __init__(self, total_blocks):
        # Define o número total de blocos no sistema de arquivos
        self.total_blocks = total_blocks
        # Inicializa o conjunto de blocos livres como todos os blocos disponíveis
        self.free_blocks = set(range(total_blocks))
        # Dicionário para armazenar os blocos alocados com seus respectivos dados
        self.allocated_blocks = {}
        # Dicionário para armazenar os arquivos com seus blocos associados e diretórios
        self.files = {}
        # Dicionário para armazenar os diretórios e os arquivos que eles contêm
        self.directories = {'/': set()}
        # Define o diretório atual como o diretório raiz
        self.current_directory = '/'
        # Dicionário para armazenar os atributos dos arquivos e diretórios
        self.attributes = {}

    # Método para alocar um bloco no sistema de arquivos
    def allocate_block(self):
        # Verifica se há blocos livres disponíveis
        if len(self.free_blocks) == 0:
            raise Exception("Nenhum bloco livre disponível")
        # Remove e retorna um bloco livre para alocação
        block = self.free_blocks.pop()
        # Adiciona o bloco aos blocos alocados sem atribuir dados inicialmente
        self.allocated_blocks[block] = None
        return block

    # Método para liberar um bloco previamente alocado
    def free_block(self, block):
        # Verifica se o bloco está realmente alocado
        if block not in self.allocated_blocks:
            raise Exception("Bloco não está alocado")
        # Remove o bloco dos blocos alocados e o adiciona aos blocos livres
        del self.allocated_blocks[block]
        self.free_blocks.add(block)

    # Método para escrever dados em um bloco alocado
    def write_block(self, block, data):
        # Verifica se o bloco está alocado
        if block not in self.allocated_blocks:
            raise Exception("Bloco não está alocado")
        # Escreve os dados no bloco especificado
        self.allocated_blocks[block] = data

    # Método para ler os dados de um bloco alocado
    def read_block(self, block):
        # Verifica se o bloco está alocado
        if block not in self.allocated_blocks:
            raise Exception("Bloco não está alocado")
        # Retorna os dados do bloco especificado
        return self.allocated_blocks[block]

    # Método para criar um novo arquivo no sistema de arquivos
    def create_file(self, filename, content='', directory=None):
        # Define o diretório atual se nenhum diretório for especificado
        if directory is None:
            directory = self.current_directory
        # Verifica se o diretório especificado existe
        if directory not in self.directories:
            raise Exception("Diretório não existe")
        # Verifica se o arquivo já existe
        if filename in self.files:
            raise Exception("Arquivo já existe")
        # Aloca um bloco para o novo arquivo
        block = self.allocate_block()
        # Adiciona o arquivo ao dicionário de arquivos com seu bloco e diretório associados
        self.files[filename] = (block, directory)
        # Adiciona o arquivo ao diretório especificado
        self.directories[directory].add(filename)
        # Escreve os dados no bloco se houver conteúdo especificado
        if content:
            self.write_block(block, content)

    # Método para visualizar o conteúdo de um arquivo
    def view_file(self, filename):
        # Verifica se o arquivo existe
        if filename not in self.files:
            raise Exception("Arquivo não existe")
        # Obtém o bloco associado ao arquivo e lê seus dados
        block, _ = self.files[filename]
        return self.read_block(block)

    # Método para editar o conteúdo de um arquivo
    def edit_file(self, filename, data):
        # Verifica se o arquivo existe
        if filename not in self.files:
            raise Exception("Arquivo não existe")
        # Obtém o bloco associado ao arquivo e escreve os novos dados
        block, _ = self.files[filename]
        self.write_block(block, data)

    # Método para remover um arquivo do sistema de arquivos
    def remove_file(self, filename):
        # Verifica se o arquivo existe
        if filename not in self.files:
            raise Exception("Arquivo não existe")
        # Obtém o bloco associado ao arquivo e o libera
        block, _ = self.files[filename]
        self.free_block(block)
        # Remove o arquivo dos registros de arquivos e do diretório
        del self.files[filename]
        self.directories[self.current_directory].remove(filename)

    # Método para remover um diretório do sistema de arquivos
    def remove_directory(self, directory):
        # Verifica se o diretório existe
        if directory not in self.directories:
            raise Exception("Diretório não existe")
        # Não permite a remoção do diretório raiz
        if directory == '/':
            raise Exception("Não é possível remover o diretório raiz")
        # Verifica se o diretório está vazio
        if self.list_directory(directory):
            raise Exception("Diretório não está vazio")
        # Remove o diretório dos registros de diretórios e do diretório atual
        del self.directories[directory]
        self.directories[self.current_directory].remove(directory)

    # Método para criar um novo diretório no sistema de arquivos
    def create_directory(self, directory):
        # Verifica se o diretório já existe
        if directory in self.directories:
            raise Exception("Diretório já existe")
        # Verifica se o diretório atual existe
        if self.current_directory not in self.directories:
            raise Exception("Diretório atual não existe")
        # Adiciona o novo diretório aos registros de diretórios
        self.directories[directory] = set()
        self.directories[self.current_directory].add(directory)

    # Método para listar os arquivos e diretórios de um diretório específico
    def list_directory(self, directory=None):
        # Define o diretório atual se nenhum diretório for especificado
        if directory is None:
            directory = self.current_directory
        # Verifica se o diretório especificado existe
        if directory not in self.directories:
            raise Exception("Diretório não existe")
        # Retorna uma lista dos arquivos e diretórios no diretório especificado
        return list(self.directories[directory])

    # Método para navegar para um diretório específico
    def navigate(self, directory):
        # Verifica se o diretório existe
        if directory not in self.directories:
            raise Exception("Diretório não existe")
        # Não permite navegar de volta para o diretório raiz se já estiver no diretório raiz
        if directory == '/' and self.current_directory != '/':
            raise Exception("Não é possível navegar de volta para o diretório raiz")
        # Define o diretório atual como o diretório especificado
        self.current_directory = directory

    # Método para navegar de volta para o diretório pai
    def navigate_back(self):
        # Retorna se o diretório atual já é o diretório raiz
        if self.current_directory == '/':
            return
        # Obtém o diretório pai do diretório atual
        parent_directory = '/'.join(self.current_directory.split('/')[:-1])
        # Define o diretório pai como o diretório atual
        if parent_directory == '':
            parent_directory = '/'
        self.current_directory = parent_directory

    # Método para obter uma representação em bitmap dos blocos alocados no sistema de arquivos
    def get_allocated_blocks_bitmap(self):
        # Cria uma lista de bits representando os blocos alocados ou livres
        bitmap = ['1' if i in self.allocated_blocks else '0' for i in range(self.total_blocks)]
        # Retorna a representação em bitmap como uma string
        return ' '.join(bitmap)


    def set_attribute(self, path, attribute, value):
        if path not in self.files and path not in self.directories:
            raise Exception("Caminho não encontrado")
        if path not in self.attributes:
            self.attributes[path] = {}
        self.attributes[path][attribute] = value
        return f"Atributo '{attribute}' definido para '{path}' com valor '{value}'"

    def get_attribute(self, path, attribute):
        if path in self.attributes and attribute in self.attributes[path]:
            return self.attributes[path][attribute]
        return None

# Classe para uma interface gráfica de usuário para o sistema de arquivos
class FileSystemGUI:
    # Método de inicialização da classe FileSystemGUI
    def __init__(self, master):
        # Define a janela principal da interface gráfica
        self.master = master
        self.master.title("Sistema de Arquivos GUI")
        # Cria uma instância do sistema de arquivos com 100 blocos
        self.file_system = FileSystem(100)
        # Define o diretório atual como o diretório raiz
        self.current_directory = '/'
        # Cria um rótulo para exibir o diretório atual
        self.current_path_label = tk.Label(master, text="Diretório Atual: " + self.current_directory)
        self.current_path_label.pack()
        # Cria uma caixa de listagem para exibir os diretórios
        self.directory_listbox = tk.Listbox(master, height=10, width=50)
        self.directory_listbox.pack()
        # Cria uma caixa de listagem para exibir os arquivos no diretório atual
        self.file_listbox = tk.Listbox(master, height=10, width=50)
        self.file_listbox.pack()
        # Cria botões para navegar, criar diretório, criar arquivo, visualizar arquivo, editar arquivo, remover arquivo,
        # remover diretório e visualizar blocos alocados
        self.navigate_button = tk.Button(master, text="Abrir Diretório", command=self.open_directory)
        self.navigate_button.pack()
        self.navigate_back_button = tk.Button(master, text="Voltar", command=self.go_back)
        self.navigate_back_button.pack()
        self.create_directory_button = tk.Button(master, text="Criar Diretório", command=self.create_directory)
        self.create_directory_button.pack()
        self.create_file_button = tk.Button(master, text="Criar Arquivo", command=self.create_file)
        self.create_file_button.pack()
        self.view_file_button = tk.Button(master, text="Visualizar Arquivo", command=self.view_file)
        self.view_file_button.pack()
        self.edit_file_button = tk.Button(master, text="Editar Arquivo", command=self.edit_file)
        self.edit_file_button.pack()
        self.remove_file_button = tk.Button(master, text="Remover Arquivo", command=self.remove_file)
        self.remove_file_button.pack()
        self.remove_directory_button = tk.Button(master, text="Remover Diretório", command=self.remove_directory)
        self.remove_directory_button.pack()
        self.view_allocated_blocks_button = tk.Button(master, text="Visualizar Blocos Ocupados", command=self.view_allocated_blocks)
        self.view_allocated_blocks_button.pack()
        self.set_attr_button = tk.Button(master, text="Definir Atributo", command=self.set_attr)
        self.set_attr_button.pack()
        self.get_attr_button = tk.Button(master, text="Obter Atributo", command=self.get_attr)
        self.get_attr_button.pack()
        # Atualiza a caixa de listagem de diretórios
        self.update_directory_listbox()

    # Método para abrir um diretório selecionado na caixa de listagem de diretórios
    def open_directory(self):
        # Obtém o índice do diretório selecionado
        selected_directory_index = self.directory_listbox.curselection()
        # Exibe um erro se nenhum diretório foi selecionado
        if not selected_directory_index:
            messagebox.showerror("Erro", "Nenhum diretório selecionado")
            return
        # Obtém o nome do diretório selecionado
        selected_directory = self.directory_listbox.get(selected_directory_index)
        # Navega para o diretório selecionado no sistema de arquivos
        self.file_system.navigate(selected_directory)
        # Atualiza o diretório atual e a caixa de listagem de diretórios
        self.current_directory = self.file_system.current_directory
        self.update_directory_listbox()

    # Método para navegar de volta para o diretório pai
    def go_back(self):
        # Navega para o diretório pai no sistema de arquivos
        self.file_system.navigate_back()
        # Atualiza o diretório atual e a caixa de listagem de diretórios
        self.current_directory = self.file_system.current_directory
        self.update_directory_listbox()

    # Método para criar um novo diretório
    def create_directory(self):
        # Solicita o nome do diretório ao usuário
        directory_name = simpledialog.askstring("Criar Diretório", "Nome do Diretório:")
        # Cria o diretório no sistema de arquivos e atualiza a caixa de listagem de diretórios
        if directory_name:
            try:
                self.file_system.create_directory(directory_name)
                self.update_directory_listbox()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    # Método para criar um novo arquivo
    def create_file(self):
        # Solicita o nome do arquivo ao usuário
        filename = simpledialog.askstring("Criar Arquivo", "Nome do Arquivo:")
        # Cria o arquivo no sistema de arquivos e atualiza a caixa de listagem de arquivos
        if filename:
            try:
                self.file_system.create_file(filename)
                self.update_file_listbox()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    # Método para visualizar o conteúdo de um arquivo
    def view_file(self):
        # Obtém o índice do arquivo selecionado
        selected_file_index = self.file_listbox.curselection()
        # Exibe um erro se nenhum arquivo foi selecionado
        if not selected_file_index:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado")
            return
        # Obtém o nome do arquivo selecionado
        selected_file = self.file_listbox.get(selected_file_index)
        # Exibe o conteúdo do arquivo em uma caixa de mensagem
        try:
            content = self.file_system.view_file(selected_file)
            messagebox.showinfo("Conteúdo do Arquivo", content)
        # Exceção se o arquivo não puder ser encontrado
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Método para editar o conteúdo de um arquivo
    def edit_file(self):
        # Obtém o índice do arquivo selecionado
        selected_file_index = self.file_listbox.curselection()
        # Exibe um erro se nenhum arquivo foi selecionado
        if not selected_file_index:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado")
            return
        # Obtém o nome do arquivo selecionado
        selected_file = self.file_listbox.get(selected_file_index)
        try:
            # Obtém o conteúdo atual do arquivo
            current_content = self.file_system.view_file(selected_file)
            # Solicita o novo conteúdo ao usuário
            new_content = simpledialog.askstring("Editar Arquivo", "Novo Conteúdo:", initialvalue=current_content)
            # Atualiza o conteúdo do arquivo se o novo conteúdo for fornecido
            if new_content is not None:
                self.file_system.edit_file(selected_file, new_content)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Método para remover um arquivo
    def remove_file(self):
        # Obtém o índice do arquivo selecionado
        selected_file_index = self.file_listbox.curselection()
        # Exibe um erro se nenhum arquivo foi selecionado
        if not selected_file_index:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado")
            return
        # Obtém o nome do arquivo selecionado
        selected_file = self.file_listbox.get(selected_file_index)
        try:
            # Remove o arquivo do sistema de arquivos e atualiza a caixa de listagem de arquivos
            self.file_system.remove_file(selected_file)
            self.update_file_listbox()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Método para remover um diretório
    def remove_directory(self):
        # Obtém o índice do diretório selecionado
        selected_directory_index = self.directory_listbox.curselection()
        # Exibe um erro se nenhum diretório foi selecionado
        if not selected_directory_index:
            messagebox.showerror("Erro", "Nenhum diretório selecionado")
            return
        # Obtém o nome do diretório selecionado
        selected_directory = self.directory_listbox.get(selected_directory_index)
        try:
            # Remove o diretório do sistema de arquivos e atualiza a caixa de listagem de diretórios
            self.file_system.remove_directory(selected_directory)
            self.update_directory_listbox()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Método para atualizar a caixa de listagem de diretórios
    def update_directory_listbox(self):
        # Limpa a caixa de listagem de diretórios
        self.directory_listbox.delete(0, tk.END)
        # Obtém a lista de diretórios no diretório atual
        directories = self.file_system.list_directory()
        # Adiciona os diretórios à caixa de listagem
        for directory in directories:
            self.directory_listbox.insert(tk.END, directory)
        # Atualiza o rótulo do diretório atual
        self.current_path_label.config(text="Diretório Atual: " + self.current_directory)
        # Atualiza a caixa de listagem de arquivos
        self.update_file_listbox()

    # Método para atualizar a caixa de listagem de arquivos no diretório atual
    def update_file_listbox(self):
        # Limpa a caixa de listagem de arquivos
        self.file_listbox.delete(0, tk.END)
        # Obtém a lista de arquivos no diretório atual
        files = self.file_system.list_directory()
        # Adiciona os arquivos à caixa de listagem
        for filename in files:
            if filename in self.file_system.files:
                self.file_listbox.insert(tk.END, filename)

    # Método para visualizar os blocos alocados no sistema de arquivos
    def view_allocated_blocks(self):
        # Obtém a representação em bitmap dos blocos alocados
        bitmap = self.file_system.get_allocated_blocks_bitmap()
        # Exibe a representação em bitmap em uma caixa de mensagem
        messagebox.showinfo("Blocos Ocupados", bitmap)
 
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

# Método para obter o valor de um atributo
    def get_attr(self):
        path = simpledialog.askstring("Obter Atributo", "Digite o caminho do nó (a partir do diretório atual):")
        attribute = simpledialog.askstring("Obter Atributo", "Digite o nome do atributo:")
        if path and attribute:
            value = self.file_system.get_attribute(path, attribute)
            if value is not None:
                messagebox.showinfo("Valor do Atributo", f"O valor do atributo '{attribute}' em '{path}' é '{value}'.")
            else:
                messagebox.showerror("Erro", f"O atributo '{attribute}' em '{path}' não foi encontrado.")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
# Classe para uma aplicação de login
class LoginApp:
    # Método de inicialização da classe LoginApp
    def __init__(self, master):
        # Define a janela principal da aplicação
        self.master = master
        self.master.title("Login")
        # Dicionário para armazenar os usuários e senhas
        self.users = {}
        # Cria rótulos e entradas para nome de usuário e senha
        self.username_label = tk.Label(master, text="Nome de usuário:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()
        self.password_label = tk.Label(master, text="Senha:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()
        # Cria botões para login e registro
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()
        self.register_button = tk.Button(master, text="Registrar", command=self.register)
        self.register_button.pack()

    # Método para realizar o login
    def login(self):
        # Obtém o nome de usuário e senha digitados pelo usuário
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Verifica se o nome de usuário e senha correspondem a um usuário registrado
        if username in self.users and self.users[username] == password:
            # Exibe uma mensagem de login bem-sucedido e abre a interface gráfica do sistema de arquivos
            messagebox.showinfo("Login bem-sucedido", "Bem-vindo, " + username + "!")
            self.master.destroy()
            main_window = tk.Tk()
            FileSystemGUI(main_window)
            main_window.mainloop()
        else:
            # Exibe uma mensagem de erro se o login falhar
            messagebox.showerror("Erro de login", "Nome de usuário ou senha inválidos")

    # Método para registrar um novo usuário
    def register(self):
        # Obtém o nome de usuário e senha digitados pelo usuário
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Verifica se o nome de usuário já está em uso
        if username in self.users:
            messagebox.showerror("Erro de registro", "Nome de usuário já está em uso")
        else:
            # Registra o novo usuário e exibe uma mensagem de registro bem-sucedido
            self.users[username] = password
            messagebox.showinfo("Registro bem-sucedido", "Usuário registrado com sucesso")

# Cria a janela principal da aplicação de login
root = tk.Tk()
# Inicializa a aplicação de login
app = LoginApp(root)
# Inicia o loop principal da interface gráfica
root.mainloop()