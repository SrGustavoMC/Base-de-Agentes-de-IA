# ==============================================================================
# PARTE 1: ESTRUTURA E CONFIGURAÇÃO DO FRAMEWORK
# (Geralmente, você não precisa mudar nada aqui)
# ==============================================================================
import os
import google.generativeai as genai
import textwrap
from dotenv import load_dotenv

# --- Configuração da Chave de API (Preferencialmente use uma chave diferente para cada projeto)---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    print("✅ Chave de API configurada com sucesso!")
else:
    print("⚠️ Atenção: Chave de API não encontrada no arquivo .env.")

# --- Função Auxiliar de Formatação ---
def formatar_texto(text: str) -> str:
    if not isinstance(text, str): text = str(text)
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# ==============================================================================
# PARTE 2: O MOLDE DO AGENTE (A CLASSE 'AGENTE')
# (Esta é a base do framework, não precisa ser alterada)
# ==============================================================================
class Agente:
    def __init__(self, nome: str, system_instruction: str, model_name: str = "gemini-1.5-pro"):
        self.nome = nome
        self.system_instruction = textwrap.dedent(system_instruction)
        self.model = genai.GenerativeModel(model_name=model_name, system_instruction=self.system_instruction)
        print(f"🤖 Agente '{self.nome}' criado e pronto para o trabalho!")

    def executar(self, tarefa: str, contexto: str = None) -> str:
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
            return f"Erro: Não foi possível completar a tarefa."

# ==============================================================================
# PARTE 3: A FÁBRICA DE AGENTES - CRIE SEUS ASSISTENTES AQUI
#
# INSTRUÇÕES:
# 1. Defina um nome claro para seu agente (ex: "Tradutor Inglês-Português").
# 2. Escreva uma 'system_instruction' poderosa. Diga ao agente:
#    - QUEM ELE É (ex: "Você é um tradutor fluente...")
#    - O QUE ELE FAZ (ex: "...especializado em textos de negócios.")
#    - COMO ELE DEVE RESPONDER (ex: "Sua resposta deve ser apenas o texto traduzido, sem comentários.")
# 3. Adicione o agente ao dicionário 'meus_agentes' usando o nome como chave.
# ==============================================================================
print("\n" + "="*80 + "\nINICIANDO A FÁBRICA DE AGENTES...\n" + "="*80)

meus_agentes = {}

# --- MOLDE DE AGENTE 1: TAREFA ESPECÍFICA (Ex: Tradutor) ---
# Descomente e personalize as linhas abaixo para criar seu primeiro agente.
#
# nome_agente_1 = "Tradutor Jurídico"
# instrucao_agente_1 = """
#     Você é um tradutor profissional com 20 anos de experiência na área jurídica.
#     Sua única função é traduzir textos do inglês para o português brasileiro com
#     extrema precisão terminológica. Não adicione nenhuma nota ou explicação,
#     apenas o texto traduzido.
# """
# meus_agentes[nome_agente_1] = Agente(nome=nome_agente_1, system_instruction=instrucao_agente_1)


# --- MOLDE DE AGENTE 2: TAREFA CRIATIVA (Ex: Roteirista) ---
# Descomente e personalize para criar um segundo agente.
#
# nome_agente_2 = "Gerador de Ideias para Negócios"
# instrucao_agente_2 = """
#     Você é um consultor de inovação e empreendedorismo.
#     Com base em um tópico ou problema, seu objetivo é gerar 3 ideias de negócios
#     inovadoras, incluindo um nome para a empresa, o público-alvo e o principal diferencial.
#     Formate a resposta em tópicos.
# """
# meus_agentes[nome_agente_2] = Agente(nome=nome_agente_2, system_instruction=instrucao_agente_2)


# --- ADICIONE QUANTOS AGENTES QUISER SEGUINDO OS MOLDES ACIMA ---


print("\n" + "="*80 + f"\nFÁBRICA CONCLUÍDA: {len(meus_agentes)} agentes criados.\n" + "="*80)


# ==============================================================================
# PARTE 4: A ORQUESTRA - DEFINA O FLUXO DE TRABALHO
#
# INSTRUÇÕES:
# - Aqui você define como os agentes interagem.
# - O resultado de um agente (string) pode ser usado como 'contexto' para o próximo.
# - Descomente um dos exemplos de fluxo abaixo ou crie o seu próprio.
# ==============================================================================

def main():
    """Função principal que executa o fluxo de trabalho dos agentes."""
    
    # Passo 1: Defina a tarefa inicial que dará o pontapé no processo.
    tarefa_inicial = input("❓ Qual a tarefa ou tópico para hoje? ")
    print("-" * 80)
    
    # --- ESCOLHA SEU FLUXO DE TRABALHO ABAIXO ---

    try:
        # EXEMPLO DE FLUXO 1: AGENTE ÚNICO
        # Um único agente executa a tarefa inicial.
        # Descomente as 2 linhas abaixo para usar este fluxo.
        #
        # resultado_final = meus_agentes["Tradutor Jurídico"].executar(tarefa=tarefa_inicial)
        # print(formatar_texto(resultado_final))


        # EXEMPLO DE FLUXO 2: CADEIA DE AGENTES (A -> B)
        # O Agente A faz algo, e o Agente B trabalha em cima do resultado de A.
        # Descomente as 4 linhas abaixo para usar este fluxo.
        #
        # resultado_agente_A = meus_agentes["Gerador de Ideias para Negócios"].executar(tarefa=tarefa_inicial)
        # print("\n--- Resultado do Agente A ---\n")
        # print(formatar_texto(resultado_agente_A))
        #
        # resultado_final = meus_agentes["Roteirista de Vídeo Curto"].executar(
        #     tarefa="Crie um roteiro de vídeo para a primeira ideia de negócio.",
        #     contexto=resultado_agente_A
        # )
        # print("\n--- Resultado do Agente B ---\n")
        # print(formatar_texto(resultado_final))
        
        # Se nenhum fluxo for descomentado, o programa terminará aqui.
        print("✨ Fluxo de orquestração não definido. Personalize a Parte 4 do código para começar.")

    except KeyError as e:
        print(f"❌ ERRO DE ORQUESTRAÇÃO: O agente {e} não foi encontrado!")
        print("   Verifique se o nome do agente na Parte 4 corresponde exatamente ao nome definido na Parte 3.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado durante a orquestração: {e}")

# ==============================================================================
# PARTE 5: PONTO DE PARTIDA DO PROGRAMA
# ==============================================================================
if __name__ == "__main__":
    main()