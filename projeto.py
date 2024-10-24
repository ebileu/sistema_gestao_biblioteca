from collections import deque
import time

class Livro():
    def __init__(self, titulo, autor, categoria, id_unico):
        self.titulo = titulo
        self.autor = autor 
        self.categoria = categoria
        self.id_unico = id_unico
        self.esquerda = None
        self.direita = None

class Biblioteca():
    def __init__(self):
        self.raiz = None
        self.livros = []
    
    # Função para adicionar um novo livro
    def inserir(self, titulo, autor, categoria, id_unico):
        novo_livro = Livro(titulo.lower(), autor, categoria, id_unico)
        if self.raiz is None:
            self.raiz = novo_livro
        else:
            self._inserir_recursivo(self.raiz, novo_livro)
        self.livros.append(novo_livro.titulo) # Adição dos livros em uma lista que será ser usada para ordenar por título. 

    # Função para inserir o livro no nó correto
    def _inserir_recursivo(self, no_atual, novo_livro):
        if novo_livro.titulo < no_atual.titulo:
            if no_atual.esquerda is None:
                no_atual.esquerda = novo_livro
            else: 
                self._inserir_recursivo(no_atual.esquerda, novo_livro)
        else:
            if no_atual.direita is None:
                no_atual.direita = novo_livro
            else:
                self._inserir_recursivo(no_atual.direita, novo_livro)

    def buscar_por_titulo(self, titulo):
        return self._busca_binaria_titulo(self.raiz, titulo.lower())

    # Função para buscar o livro por titulo
    def _busca_binaria_titulo(self, no_atual, titulo):
        if no_atual is None or no_atual.titulo == titulo:
            return no_atual
        
        if titulo < no_atual.titulo:
            return self._busca_binaria_titulo(no_atual.esquerda, titulo)
        
        return self._busca_binaria_titulo(no_atual.direita, titulo)

    def buscar_por_autor(self, autor):
        livros_encontrados = [] # Ao encontrar o livro por autor, o livro é adicionado a lista para gerenciar melhor os livros do autor.
        self._busca_sequencial_autor(self.raiz, autor, livros_encontrados)
        return livros_encontrados

    # Função para buscar o livro por autor
    def _busca_sequencial_autor(self, no_atual, autor, livros_encontrados):
        if no_atual is None:
            return None
        if no_atual.autor == autor:
            livros_encontrados.append(no_atual) # Ao encontrar o livro por autor, o livro é adicionado a lista para gerenciar melhor os livros do autor.
        self._busca_sequencial_autor(no_atual.esquerda, autor, livros_encontrados)
        self._busca_sequencial_autor(no_atual.direita, autor, livros_encontrados)
        
    def buscar_por_categoria(self, categoria):
        livros_encontrados = [] # Ao encontrar o livro por cateogira, o livro é adicionado a lista para gerenciar melhor os livros por categoria.
        self._busca_sequencial_categoria(self.raiz, categoria, livros_encontrados)
        return livros_encontrados

    # Função para buscar o livro por categoria
    def _busca_sequencial_categoria(self, no_atual, categoria, livros_encontrados):
        if no_atual is None:
            return None
        if no_atual.categoria == categoria:
            livros_encontrados.append(no_atual) # Ao encontrar o livro por categoria, o livro é adicionado a lista para gerenciar melhor os livros por categoria.
        self._busca_sequencial_categoria(no_atual.esquerda, categoria, livros_encontrados)
        self._busca_sequencial_categoria(no_atual.direita, categoria, livros_encontrados)
    
class Emprestimo():
    def __init__(self, usuario, livro):
        self.usuario = usuario
        self.livro = livro

class GerenciadorEmprestimo():
    def __init__(self, acervo_livros):
        self.fila_emprestimo = deque() # Fila para gerenciar os empréstimos
        self.historico = {} # Dicionário para armazenar uma pilha de empréstimos para cada usuário
        self.acervo_livros = acervo_livros # Referência para a árvore de livros

    # Função para verificar se o livro existe na árvore de livros
    def verificar_livro(self, titulo):
        titulo_livro = titulo.lower()
        livro = self.acervo_livros.buscar_por_titulo(titulo_livro)
        if livro is None:
            print(f'Erro, o livro {titulo_livro} não foi encontrado')
            return False
        return True

    # Adicionar um empréstimo na fila, após verificar se o livro existe
    def adicionar_emprestimo(self, usuario, titulo_livro):
        if self.verificar_livro(titulo_livro):
            emprestimo = Emprestimo(usuario, titulo_livro)
            self.fila_emprestimo.append(emprestimo)
            print(f'Empréstimo adicionado: {usuario} requisitou o livro {titulo_livro}.')
        else: 
            print(f'O empréstimo não pode ser adicionado: livro {titulo_livro} não encontrado.')

    # Realizar o empréstimo (remover da fila)
    def realizar_emprestimo(self):
        if self.fila_emprestimo:
            emprestimo = self.fila_emprestimo.popleft() # Remover o primeiro da fila
            if emprestimo.usuario not in self.historico:
                self.historico[emprestimo.usuario] = [] # Criar uma pilha para o usuário se não existir

             # Adicionar o empréstimo ao histórico do usuário
            self.historico[emprestimo.usuario].append(emprestimo)
            print(f"Empréstimo realizado: {emprestimo.usuario} pegou o livro {emprestimo.livro}")
        else:
            print('Nenhum empréstimo pendente')

    # Desfazer o último empréstimo de um usuário
    def desfazer_emprestimo(self, usuario):
        if usuario in self.historico and self.historico[usuario]:
            ultimo_emprestimo = self.historico[usuario].pop() # Remover o último da pilha
            self.fila_emprestimo.appendleft(ultimo_emprestimo)
            print(f'Empréstimo desfeito, {usuario} devolveu o livro {ultimo_emprestimo.livro}')
            return True
        else:
            print(f'Nenhum empréstimo para desfazer para o usuario {usuario}')
            return False

class Operacao():
    def __init__(self, tipo, usuario, livro, intervalo_tempo):
        self.tipo = tipo  # 'Empréstimo', 'Devolução'
        self.usuario = usuario
        self.livro = livro
        self.intervalo_tempo = intervalo_tempo
        self.proximo = None # Próxima operação
    
class HistoricoOperacoes():
    def __init__(self):
        self.inicio = None # Primeiro nó da lista encadeada

    def adicionar_operacao(self, tipo, usuario, livro, intervalo_tempo):
        nova_operaco = Operacao(tipo, usuario, livro, intervalo_tempo)
        if self.inicio is None:
            self.inicio = nova_operaco
        else:
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = nova_operaco

    # Gerar um relatório sobre o total de operações
    def gerar_relatorio_total(self):
        total_operacoes = 0
        tipos = {'Empréstimo': 0, 'Devolução': 0}
        atual = self.inicio
        while atual:
            total_operacoes += 1
            if atual.tipo in tipos:
                tipos[atual.tipo] += 1
            atual = atual.proximo

        relatorio = f"Total de operações realizadas: {total_operacoes}\n"
        for tipo, quantidade in tipos.items():
           relatorio += f"{tipo}: {quantidade}\n"
        print(relatorio)
        gravar_relatorio_em_arquivo('relatorio_total.txt', relatorio)

    # Gerar um relatório de atividades por usuário
    def gerar_relatorio_usuario(self, usuario):
        total_usuario = 0
        tipos_usuario = {'Empréstimo': 0, 'Devolução': 0}
        atual = self.inicio
        while atual:
            if atual.usuario == usuario:
                total_usuario += 1
                tipos_usuario[atual.tipo] += 1
            atual = atual.proximo
        print(f"Total de operações realizados pelo usuário {usuario}: {total_usuario}")
        for tipo, quantidade in tipos_usuario.items():
            print(f'{tipo}: {quantidade}')

class SistemaRelatorio():
    def __init__(self) -> None:
        self.historico_operacoes = HistoricoOperacoes()

    def registrar_operacao(self, tipo, usuario, livro):
        intervalo_tempo = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.historico_operacoes.adicionar_operacao(tipo, usuario, livro, intervalo_tempo)

    # Grava a operações feitas no sistema em arquivo de texto (.txt)
    def relatorio_total(self):
        self.historico_operacoes.gerar_relatorio_total()

    # Grava a quantidade de operações que o usuário fez em um arquivo de texto (.txt)
    def relatorio_por_usuario(self, usuario):
        self.historico_operacoes.gerar_relatorio_usuario(usuario)

    # Grava o histórico de ações do usuário em um arquivo de texto (.txt)
    def imprimir_historico_usuario(self, usuario):
        relatorio = f'Histórico de operações de {usuario.upper()}\n'
        atual = self.historico_operacoes.inicio
        while atual:
            if atual.usuario == usuario:
                relatorio += f'{atual.tipo} - Livro: {atual.livro} - Horário: {atual.intervalo_tempo}\n'
            atual = atual.proximo
        print(relatorio)
        gravar_relatorio_em_arquivo(f'historico_{usuario}.txt', relatorio)


def menu_funcoes(menu):
    while menu not in ('1', '2', '3', '4', '5', '6'):
        print('-=' * 30)
        print('Comando indisponível, digite um dos comandos abaixo: ')
        print("1 - Inserir livro\n"
          "2 - Buscar livro\n"
          "3 - Ordernar livros\n"
          "4 - Gerenciar empréstismos\n"
          "5 - Relatório de desempenho\n"
          "6 - Sair do sistema\n")
        menu = input("Digite outro comando: ").strip()
    if menu == '1':
        inserir_livro()
    elif menu == '2':
        print('Você tem a opção de buscar por: '
        '1 - Titulo \n'
        '2 - Autor \n'
        '3 - Categoria \n')
        opcao = input().strip()

        while opcao not in ['1', '2', '3']:
            print('Comando inexistente, por favor, escolha somente as seguintes opções: ')
            print('1 - Titulo \n'
            '2 - Autor \n'
            '3 - Categoria \n')
            opcao = input().strip()
        
        buscar_livro(opcao)
    elif menu == '3':
        mergesort(biblioteca.livros) 
        imprimir_em_ordem(biblioteca.livros)
    elif menu == '4':
        nome_usuario = input('Digite o seu nome: ').title()

        print(f"Olá {nome_usuario}, o que você deseja fazer: 1 - Realizar Empréstimo, 2 - Desfazer seu último empréstimo?\n")
        opcao = input().strip()

        while opcao not in ['1', '2']:
            print('Comando indisponível')
            print('1 - Realizar Empréstimo, 2 - Desfazer seu último empréstimo?\n')
            opcao = input().strip()

        if opcao == '1':
            livro_titulo = input('Digite o titulo do livro na qual deseja realizar a operação: ').title()
            gerenciador.adicionar_emprestimo(nome_usuario, livro_titulo) # Adiciona a fila de emprestimo do usuário
            if gerenciador.fila_emprestimo: # Verifica se foi adicionado a fila
                gerenciador.realizar_emprestimo() # Realiza o emprestimo
                relatorio_sistema.registrar_operacao('Empréstimo', nome_usuario, livro_titulo) # Registra a ação no relatório
        elif opcao == '2':
            if nome_usuario in gerenciador.historico and gerenciador.historico[nome_usuario]:
                ultimo_livro = gerenciador.historico[nome_usuario][-1].livro
                gerenciador.desfazer_emprestimo(nome_usuario) # Desfaz o último empréstimo do usuário
                relatorio_sistema.registrar_operacao('Devolução', nome_usuario, ultimo_livro) # Registra a ação no relatório
            else:
               print(f"Erro, o usuário {nome_usuario} não tem empréstimos registrados para desfazer.")
    elif menu == '5':
        print('De qual usuário deseja gerar um relatório?')
        usuario = input(' \n').strip().title()

        relatorio_sistema.relatorio_total()

        relatorio_sistema.imprimir_historico_usuario(usuario)
        
def inserir_livro():
    titulo = input('Escreva o nome do livro: \n')
    autor = input('Escreva o autor do livro: \n')
    categoria = input('Qual a categoria do livro: \n')
    id_unico = int(input('Qual o ID do livro: \n'))
    biblioteca.inserir(titulo, autor, categoria, id_unico)

def buscar_livro(opcao):
    if opcao == '1':
            busca = input('Qual livro deseja buscar: ')
            busca_encontrada = biblioteca.buscar_por_titulo(busca)
            if busca_encontrada:
                print(f"Livro: {busca_encontrada.titulo} | Autor: {busca_encontrada.autor} |  Categoria: {busca_encontrada.categoria}")
    elif opcao == '2':
        busca = input('Qual autor deseja buscar: ')
        busca_encontrada = biblioteca.buscar_por_autor(busca)
        if busca_encontrada:
            print(f'Livros do autor: {busca}')
            for i in busca_encontrada:
                print(f'{i.titulo} | {i.categoria}')
    elif opcao == '3': 
        busca = input('Qual categoria deseja buscar: ') 
        busca_encontrada = biblioteca.buscar_por_categoria(busca)       
        if busca_encontrada:
            print(f"Livros da categoria: {busca}")
            for i in busca_encontrada:
                print(f'{i.titulo} | {i.autor}')

def mergesort(lista, inicio = 0, fim = None):
    if fim is None:
        fim = len(lista)
    if (fim - inicio > 1):
        meio = (fim + inicio) // 2
        mergesort(lista, inicio, meio)
        mergesort(lista, meio, fim)
        merge(lista, inicio, meio, fim)

def merge(lista, inicio, meio, fim):
    left = lista[inicio:meio]
    right = lista[meio:fim]
    top_left, top_right = 0, 0
    for k in range(inicio, fim):
        if top_left >= len(left):
            lista[k] = right[top_right]
            top_right = top_right + 1
        elif top_right >= len(right):
            lista[k] = left[top_left]
            top_left = top_left + 1
        elif left[top_left].titulo < right[top_right].titulo:
            lista[k] = left[top_left]
            top_left = top_left + 1
        else:
            lista[k] = right[top_right]
            top_right = top_right + 1
    # imprimir_em_ordem(lista)

def imprimir_em_ordem(livros):
    print("Imprimindo livros ordenados por Título: ")
    for livro in livros:
        print(f"Livro: {livro.titulo} | Autor: {livro.autor} | Categoria: {livro.categoria}")

def gravar_relatorio_em_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, 'a') as arquivo:
        arquivo.write(conteudo + '\n')


biblioteca = Biblioteca()
gerenciador = GerenciadorEmprestimo(biblioteca)
relatorio_sistema = SistemaRelatorio()

running = True
while running: 
    print("BEM-VINDO A NOSSA BIBLIOTECA")
    print('-=' * 30)
    print("Diante das opções a seguir, escolha o que deseja fazer: ")
    print("1 - Inserir livro\n"
          "2 - Buscar livro\n"
          "3 - Ordernar livros\n"
          "4 - Gerenciar empréstismos\n"
          "5 - Relatório de desempenho\n"
          "6 - Sair do sistema\n")
    
    menu = input().strip()
    
    if menu == '6':
        print("O SISTEMA IRÁ SER FECHADO")
        running = False
    else:
        menu_funcoes(menu)

