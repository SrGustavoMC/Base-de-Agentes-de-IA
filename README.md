1. Não se esqueça de clonar em uma pasta local.
2. Crie uma pasta chamada "venv".
3. No terminal escreva e execute as seguintes instruções na ordem exposta:
'''
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

'''    
4. Crie a sua Chave API e cole no arquivo ".env" no lugar indicado.
5. A partir disso o codigo estará 100% funcional. 
6. O que está escrito é um exemplo. Fique a vontade para testar e modificar.
7. Crie agentes como se fossem colaboradores da sua equipe. Crie descrições da forma que você quer que eles sejam dentro da sua respectiva operação. 
DICAS:
1. Peça ajuda a uma IA para fazer a descrição e função. Ela deve ser muito bem detalhada e consisa. 
2. Prefira usar mais agentes, cada um encarregado de uma operação, do que poucos com muitas operações acumuladas.
Pois, as chaves geradas gratuitamente tem restrições de tempo e operações por agentes. 
3. Sugiro que os primeiros agentes devem ser professores, pesquisadores, analistas ou terem uma experiencia profissional com muitos anos em determinada área,
cuja personalidade é curiosa e investigativa. Já os últimos devem ser mais criativos e terem uma liberdade maior dentro do escopo de "assunto" ou operação de entrega.

Exemplo:
# ==============================================================================
# PROJETO: GERADOR DE ATIVIDADES DE PROGRAMAÇÃO v2.0
# DESCRIÇÃO: Um sistema com 5 agentes de IA especialistas que colaboram
#            em uma linha de montagem para criar um exercício de programação.
# ==============================================================================

# ==============================================================================
# PARTE 1: ESTRUTURA E CONFIGURAÇÃO DO FRAMEWORK
# ==============================================================================
import os
import google.generativeai as genai
import textwrap
import time
from dotenv import load_dotenv

# --- Configuração da Chave de API ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    print("✅ Chave de API configurada com sucesso!")
else:
    print("⚠️ Atenção: Chave de API não encontrada no arquivo .env.")
    print("   Crie um arquivo .env e adicione sua chave para o programa funcionar.")

# --- Função Auxiliar de Formatação de Texto ---
def formatar_texto(text: str) -> str:
    """Formata o texto para uma melhor exibição no terminal."""
    if not isinstance(text, str): text = str(text)
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# ==============================================================================
# PARTE 2: O MOLDE DO AGENTE (A CLASSE 'AGENTE')
# (Esta é a base do framework, não precisa ser alterada)
# ==============================================================================
class Agente:
    """Define a estrutura base para um agente de IA."""
    def __init__(self, nome: str, system_instruction: str, model_name: str = "gemini-1.5-flash"):
        self.nome = nome
        self.system_instruction = textwrap.dedent(system_instruction)
        self.model = genai.GenerativeModel(model_name=model_name, system_instruction=self.system_instruction)
        print(f"🤖 Agente '{self.nome}' contratado e pronto para o trabalho!")

    def executar(self, tarefa: str, contexto: str = None) -> str:
        """Executa uma tarefa, opcionalmente usando um contexto."""
        print(f"⏳ Agente '{self.nome}' iniciando tarefa...")
        prompt = f"TAREFA: {tarefa}"
        if contexto:
            prompt = f"CONTEXTO PARA REALIZAR A TAREFA:\n---\n{contexto}\n---\n\n{prompt}"
        try:
            response = self.model.generate_content(prompt)
            print(f"✅ Agente '{self.nome}' concluiu a tarefa!")
            return response.text
        except Exception as e:
            print(f"❌ Erro ao executar o agente '{self.nome}': {e}")
            return f"Erro: Não foi possível completar a tarefa. Motivo: {e}"

# ==============================================================================
# PARTE 3: A FÁBRICA DE AGENTES - A NOVA EQUIPE DE ESPECIALISTAS
# ==============================================================================
print("\n" + "="*80 + "\nINICIANDO A FÁBRICA DE AGENTES...\n" + "="*80)

meus_agentes = {}

# --- AGENTE 1: O ESTRATEGISTA ---
meus_agentes["Analisador de Negócios"] = Agente(
    nome="Analisador de Negócios",
    system_instruction="""
        Você é um analista de negócios sênior. Sua única função é receber uma URL e descrever em um parágrafo conciso:
        1. O modelo de negócio do site.
        2. O público-alvo principal.
        3. O propósito central ou o problema que ele resolve.
        Sua resposta deve ser apenas este parágrafo de análise.
    """
)

# --- AGENTE 2: O ENGENHEIRO DE FRONT-END ---
meus_agentes["Engenheiro de UI/UX"] = Agente(
    nome="Engenheiro de UI/UX",
    system_instruction="""
        Você é um engenheiro de Front-end e especialista em UI/UX. Com base em um conceito de negócio (contexto),
        sua tarefa é listar os 5 a 7 componentes de interface e funcionalidades essenciais que um usuário veria e com os quais interagiria no site.
        Formate a resposta como uma lista de tópicos (bullet points).
    """
)

# --- AGENTE 3: O ARQUITETO DE BACK-END ---
meus_agentes["Arquiteto de Back-End"] = Agente(
    nome="Arquiteto de Back-End",
    system_instruction="""
        Você é um arquiteto de software especializado em Back-end. Com base em uma lista de funcionalidades de front-end (contexto),
        sua tarefa é projetar os recursos de back-end necessários. Descreva:
        1. Os principais modelos de dados (tabelas de banco de dados).
        2. Os 3 ou 4 endpoints de API mais importantes (ex: GET /users, POST /items).
        Seja técnico e direto.
    """
)

# --- AGENTE 4: O CRIADOR DO DESAFIO ---
meus_agentes["Desenvolvedor de Conteúdo Didático"] = Agente(
    nome="Desenvolvedor de Conteúdo Didático",
    system_instruction="""
        Você é um educador de programação. Sua função é receber especificações de front-end e back-end (contexto)
        e transformá-las em um desafio de programação claro e estruturado.
        Organize a atividade em "Parte 1: Front-End" e "Parte 2: Back-End", detalhando as tarefas de forma lógica para um aluno.
        Sua resposta deve ser o rascunho da atividade.
    """
)

# --- AGENTE 5: O REVISOR FINAL ---
meus_agentes["Revisor Pedagógico"] = Agente(
    nome="Revisor Pedagógico",
    system_instruction="""
        Você é um professor experiente com uma didática impecável. Sua tarefa é receber um rascunho de uma atividade de programação (contexto)
        e aprimorá-la. Seu trabalho é:
        1. Simplificar a linguagem para torná-la mais clara e motivadora.
        2. Formatar o texto perfeitamente para um PDF, usando títulos, listas e negrito.
        3. Adicionar uma seção "Conselho do Mestre" ao final de cada parte (Front-end e Back-end) com uma dica útil que não entregue a resposta.
    """
)

print("\n" + "="*80 + f"\nFÁBRICA CONCLUÍDA: {len(meus_agentes)} agentes contratados.\n" + "="*80)

# ==============================================================================
# PARTE 4: A ORQUESTRA - A NOVA LINHA DE MONTAGEM
# ==============================================================================

def main():
    """Função principal que executa o fluxo de trabalho dos agentes."""
    print("\n--- INICIANDO ORQUESTRADOR DE AGENTES v2.0 ---")
    tarefa_inicial = input("❓ Qual a URL do site que vamos usar como base para a atividade? (ex: https://www.airbnb.com)\n> ")
    print("-" * 80)
    
    # Pausa entre agentes para não sobrecarregar a API e facilitar a leitura.
    PAUSA_ENTRE_AGENTES = 10 

    try:
        # ETAPA 1: O Analisador de Negócios define o conceito.
        contexto_conceito = meus_agentes["Analisador de Negócios"].executar(tarefa=f"Analise a URL: {tarefa_inicial}")
        print("\n---  концепт ETAPA 1: CONCEITO DE NEGÓCIO ---")
        print(formatar_texto(contexto_conceito))
        time.sleep(PAUSA_ENTRE_AGENTES)

        # ETAPA 2: O Engenheiro de UI/UX lista as funcionalidades.
        contexto_frontend = meus_agentes["Engenheiro de UI/UX"].executar(tarefa="Liste os componentes de UI/UX.", contexto=contexto_conceito)
        print("\n--- 🎨 ETAPA 2: ESPECIFICAÇÕES DE FRONT-END ---")
        print(formatar_texto(contexto_frontend))
        time.sleep(PAUSA_ENTRE_AGENTES)

        # ETAPA 3: O Arquiteto de Back-End projeta a API e o DB.
        contexto_backend = meus_agentes["Arquiteto de Back-End"].executar(tarefa="Projete a API e os modelos de dados.", contexto=contexto_frontend)
        print("\n--- ⚙️ ETAPA 3: ESPECIFICAÇÕES DE BACK-END ---")
        print(formatar_texto(contexto_backend))
        time.sleep(PAUSA_ENTRE_AGENTES)

        # ETAPA 4: O Desenvolvedor Didático monta o rascunho da atividade.
        contexto_para_desafio = f"Especificações de Front-End:\n{contexto_frontend}\n\nEspecificações de Back-End:\n{contexto_backend}"
        contexto_rascunho = meus_agentes["Desenvolvedor de Conteúdo Didático"].executar(tarefa="Crie o desafio de programação.", contexto=contexto_para_desafio)
        print("\n--- 📝 ETAPA 4: RASCUNHO DA ATIVIDADE ---")
        print(formatar_texto(contexto_rascunho))
        time.sleep(PAUSA_ENTRE_AGENTES)

        # ETAPA 5: O Revisor Pedagógico dá o toque final.
        atividade_final = meus_agentes["Revisor Pedagógico"].executar(tarefa="Revise e formate esta atividade.", contexto=contexto_rascunho)
        print("\n" + "="*80)
        print("✨🎉 ATIVIDADE FINAL REVISADA (Pronta para os Alunos!) 🎉✨")
        print("="*80)
        print(formatar_texto(atividade_final))

    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado durante a orquestração: {e}")

# ==============================================================================
# PARTE 5: PONTO DE PARTIDA DO PROGRAMA
# ==============================================================================
if __name__ == "__main__":
    main()
Resultado: 
# Desafio de Programação: Construindo um Site B2B para a IBM!

Neste desafio, vamos criar um site B2B para a IBM, simulando um projeto real!  Dividiremos o trabalho em duas partes: **Front-end** (a parte visual que o usuário vê) e **Back-end** (os bastidores que fazem tudo funcionar).  Use as tecnologias que você domina (React, Node.js, MongoDB são ótimas opções, mas a criatividade é bem-vinda!).  O foco é criar um código limpo e organizado, fácil de entender e manter.


## Parte 1: Front-end - Criando a Interface

**Objetivo:**  Construir a interface do usuário (UI) do site.  Imagine que você está criando a "cara" do site, incluindo busca, navegação e apresentação das informações.  Nesta etapa, não precisamos nos conectar ao back-end; usaremos dados falsos (mockados) para testar tudo.

**Tarefas:**

1. **Busca e Filtragem Inteligente (25%):** Crie uma barra de busca com autocompletar e filtros poderosos!  Use dados mockados de pelo menos 20 soluções IBM (cada uma com indústria e tecnologias diferentes).  A busca deve filtrar por nome da solução, indústria e tecnologia.  Os filtros devem ser:

    * **Setor:** (Finanças, Saúde, Manufatura, etc.)
    * **Tamanho da Empresa:** (Pequena, Média, Grande)
    * **Orçamento:** (Baixo, Médio, Alto)
    * **Tecnologia:** (Cloud, IA, Blockchain, etc.)

    Os filtros devem funcionar juntos (combinando várias opções).

2. **Páginas por Indústria (15%):**  Crie páginas separadas para pelo menos 3 setores (ex: Finanças, Saúde, Manufatura).  Cada página mostrará as soluções relevantes para aquele setor, usando os seus dados mockados, com um breve resumo de cada solução.

3. **Cards de Soluções (20%):**  Desenvolva um componente "Card" para exibir cada solução de forma concisa:

    * Ícone (pode ser um placeholder)
    * Título
    * Descrição curta dos benefícios
    * Botão "Saiba Mais" (por enquanto, pode mostrar um alerta no console)

    Os cards devem se adaptar a diferentes tamanhos de tela (responsividade).

4. **Recursos Downloadáveis (15%):**  Crie uma seção para mostrar recursos (dados mockados, como títulos, descrições e URLs fictícios), organizados por categoria (White Papers, Ebooks, Webinars).

5. **Navegação (15%):**  Implemente uma navegação clara e intuitiva. Use menus e, se possível, "breadcrumbs" (aquelas migalhas de pão que mostram onde você está no site) para facilitar a navegação entre seções.

6. **Central de Suporte/FAQ (10%):** Crie uma seção com perguntas frequentes (dados mockados).  Use um acordeão (accordion) ou uma lista simples para exibir as perguntas e respostas.


**Conselho do Mestre:** Pense na experiência do usuário!  Como você tornaria a navegação o mais intuitiva possível, mesmo para quem nunca viu o site antes?  Lembre-se que um bom design é fundamental para um site de sucesso.


## Parte 2: Back-end - Os Bastidores

**Objetivo:** Criar a API (interface de programação) RESTful para o site.  Esta é a parte que "alimenta" o front-end com dados e processa as informações.

**Tarefas:**

1. **Banco de Dados (15%):** Configure um banco de dados (MongoDB, PostgreSQL, etc.) com tabelas para: Soluções, Indústrias, Recursos,  e as relações entre Soluções e Indústrias e Soluções e Tecnologias. Importe os dados mockados da parte 1.

2. **Endpoints da API (60%):**  Crie os seguintes endpoints RESTful:

    * `/solutions`:  Listar soluções (com paginação).  Incluir busca e filtragem.
    * `/solutions/{id}`:  Detalhes de uma solução específica.
    * `/resources`: Listar recursos (com paginação).
    * `/contact`: Receber informações de contato (nome, email, mensagem).  Um log simples dos dados recebidos é suficiente.  Não precisa integrar com email ou CRM.

3. **Documentação da API (15%):**  Documente sua API claramente, incluindo exemplos de requisições e respostas para cada endpoint.  Swagger ou Postman são ótimas ferramentas para isso.

4. **Tratamento de Erros (10%):**  Trate os erros adequadamente, retornando códigos HTTP apropriados e mensagens informativas em caso de falhas.


**Conselho do Mestre:**  Ao projetar seus endpoints, pense na eficiência.  Como você pode minimizar o tempo de resposta e o uso de recursos do servidor?  Lembre-se que uma API bem-projetada é a base de um site responsivo e performático.


## Entrega

* Código-fonte completo do Front-end e Back-end.
* Documentação da API.
* Descrição da arquitetura utilizada (tecnologias, escolhas de design).
* Instruções claras de como executar o projeto.

## Critérios de Avaliação

* Funcionalidade correta.
* Clareza, organização e legibilidade do código.
* Eficiência e performance.
* Qualidade da documentação.
* Boas práticas de desenvolvimento.

Boa sorte e divirta-se construindo seu site B2B para a IBM!
