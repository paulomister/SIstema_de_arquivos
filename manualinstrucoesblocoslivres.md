# Manual do Usuário para Sistema de Arquivos GUI

## Introdução

Este manual descreve como utilizar a interface gráfica de um sistema de arquivos implementado em Python usando a biblioteca `tkinter`. O sistema permite a criação, visualização, edição e remoção de arquivos e diretórios, além de outras funcionalidades como navegação e gerenciamento de atributos.

## Início

### Requisitos

- Python instalado (versão 3.x recomendada).
- Biblioteca `tkinter` instalada (normalmente vem com a instalação padrão do Python).

### Execução

Para executar o programa, salve o código fornecido em um arquivo Python (`sistema_de_arquivos.py`) e execute-o com o comando:

```sh
python sistema_de_arquivos.py
```

## Funcionalidades

### Login e Registro

Ao iniciar a aplicação, a janela de login será exibida.

- **Login:** Digite seu nome de usuário e senha e clique em "Login".
- **Registro:** Para registrar um novo usuário, digite um novo nome de usuário e senha e clique em "Registrar".

### Interface Principal

Após o login bem-sucedido, a interface principal do sistema de arquivos será exibida.

#### Diretório Atual

Um rótulo no topo da janela mostra o diretório atual.

#### Listagem de Diretórios

Uma caixa de listagem exibe os diretórios disponíveis no diretório atual.

#### Listagem de Arquivos

Uma caixa de listagem exibe os arquivos disponíveis no diretório atual.

### Navegação

- **Abrir Diretório:** Selecione um diretório na listagem de diretórios e clique em "Abrir Diretório".
- **Voltar:** Clique em "Voltar" para navegar para o diretório pai.

### Gerenciamento de Diretórios

- **Criar Diretório:** Clique em "Criar Diretório", digite o nome do novo diretório e confirme.
- **Remover Diretório:** Selecione um diretório na listagem de diretórios e clique em "Remover Diretório".

### Gerenciamento de Arquivos

- **Criar Arquivo:** Clique em "Criar Arquivo", digite o nome do novo arquivo e confirme.
- **Visualizar Arquivo:** Selecione um arquivo na listagem de arquivos e clique em "Visualizar Arquivo" para ver seu conteúdo.
- **Editar Arquivo:** Selecione um arquivo na listagem de arquivos, clique em "Editar Arquivo", edite o conteúdo e confirme.
- **Remover Arquivo:** Selecione um arquivo na listagem de arquivos e clique em "Remover Arquivo".

### Blocos Ocupados

- **Visualizar Blocos Ocupados:** Clique em "Visualizar Blocos Ocupados" para ver a representação em bitmap dos blocos alocados.

### Atributos

- **Definir Atributo:** Clique em "Definir Atributo", digite o caminho do arquivo/diretório, o nome do atributo e seu valor.
- **Obter Atributo:** Clique em "Obter Atributo", digite o caminho do arquivo/diretório e o nome do atributo para ver seu valor.

## Descrição dos Botões

- **Abrir Diretório:** Navega para o diretório selecionado.
- **Voltar:** Navega para o diretório pai.
- **Criar Diretório:** Cria um novo diretório.
- **Criar Arquivo:** Cria um novo arquivo.
- **Visualizar Arquivo:** Exibe o conteúdo do arquivo selecionado.
- **Editar Arquivo:** Edita o conteúdo do arquivo selecionado.
- **Remover Arquivo:** Remove o arquivo selecionado.
- **Remover Diretório:** Remove o diretório selecionado.
- **Visualizar Blocos Ocupados:** Exibe a representação em bitmap dos blocos alocados.
- **Definir Atributo:** Define um atributo para um arquivo ou diretório.
- **Obter Atributo:** Obtém o valor de um atributo de um arquivo ou diretório.

## Mensagens de Erro

- **Erro ao abrir diretório:** Nenhum diretório selecionado.
- **Erro ao criar diretório:** Diretório já existe ou nome inválido.
- **Erro ao criar arquivo:** Arquivo já existe ou nome inválido.
- **Erro ao visualizar arquivo:** Arquivo não existe.
- **Erro ao editar arquivo:** Arquivo não existe.
- **Erro ao remover arquivo:** Arquivo não existe.
- **Erro ao remover diretório:** Diretório não existe ou não está vazio.
- **Erro ao definir atributo:** Caminho, atributo ou valor inválido.
- **Erro ao obter atributo:** Caminho ou atributo inválido.

## Fim

Este manual cobre as funcionalidades básicas da interface gráfica do sistema de arquivos. Em caso de dúvidas, verifique o código fonte para entender melhor o funcionamento interno.