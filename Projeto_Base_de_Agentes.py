# ==============================================================================
# PARTE 1: ESTRUTURA E CONFIGURAÇÃO DO FRAMEWORK
# (Geralmente, você não precisa mudar nada aqui)
# ==============================================================================
import os
import google.generativeai as genai
import textwrap
from dotenv import load_dotenv
import time ### NOVO: Importa a biblioteca para controle de tempo ###

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
    def __init__(self, nome: str, system_instruction: str, model_name: str = "gemini-1.5-flash"):
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

# --- AGENTE 1: Gerador de Ideias ---
nome_agente_1 = "Gerador de Ideias para Negócios"
instrucao_agente_1 = """
    Você é um consultor de inovação e empreendedorismo.
    Com base em um tópico ou problema, seu objetivo é gerar 3 ideias de negócios
    inovadoras, incluindo um nome para a empresa, o público-alvo e o principal diferencial.
    Formate a resposta em tópicos.
"""
meus_agentes[nome_agente_1] = Agente(nome=nome_agente_1, system_instruction=instrucao_agente_1)


# --- AGENTE 2: Roteirista ---
# Para que o fluxo de exemplo funcione, criei este agente que faltava no seu código original.
nome_agente_2 = "Roteirista de Vídeo Curto"
instrucao_agente_2 = """
    Você é um roteirista criativo, especializado em criar vídeos curtos e virais para
    plataformas como TikTok e Reels. Sua tarefa é pegar uma ideia de negócio e transformá-la
    em um roteiro de 30 segundos, descrevendo as cenas, o áudio e o texto que aparece na tela.
    Seja direto e cativante.
"""
meus_agentes[nome_agente_2] = Agente(nome=nome_agente_2, system_instruction=instrucao_agente_2)


# --- ADICIONE QUANTOS AGENTES QUISER SEGUINDO OS MOLDES ACIMA ---
# Exemplo de outro agente que você pode habilitar:
#
# nome_agente_3 = "Tradutor Jurídico"
# instrucao_agente_3 = """
#     Você é um tradutor profissional com 20 anos de experiência na área jurídica.
#     Sua única função é traduzir textos do inglês para o português brasileiro com
#     extrema precisão terminológica. Não adicione nenhuma nota ou explicação,
#     apenas o texto traduzido.
# """
# meus_agentes[nome_agente_3] = Agente(nome=nome_agente_3, system_instruction=instrucao_agente_3)


print("\n" + "="*80 + f"\nFÁBRICA CONCLUÍDA: {len(meus_agentes)} agentes criados.\n" + "="*80)


# ==============================================================================
# PARTE 4: A ORQUESTRA - DEFINA O FLUXO DE TRABALHO
#
# INSTRUÇÕES:
# - Aqui você define como os agentes interagem.
# - O resultado de um agente (string) pode ser usado como 'contexto' para o próximo.
# ==============================================================================

def main():
    """Função principal que executa o fluxo de trabalho dos agentes."""
    
    # Passo 1: Defina a tarefa inicial que dará o pontapé no processo.
    tarefa_inicial = input("❓ Qual a tarefa ou tópico para hoje? ")
    print("-" * 80)
    
    # --- FLUXO DE TRABALHO ATIVO: CADEIA DE AGENTES (A -> B) ---
    # O Agente A faz algo, e o Agente B trabalha em cima do resultado de A.

    try:
        # --- Execução do Agente A ---
        resultado_agente_A = meus_agentes["Gerador de Ideias para Negócios"].executar(tarefa=tarefa_inicial)
        print("\n--- Resultado do Agente A [Gerador de Ideias] ---")
        print(formatar_texto(resultado_agente_A))

        ### NOVO: Bloco de pausa antes do próximo agente ###
        print("\n" + "="*80)
        print("⏳ Pausa! Aguardando 10 segundos antes de iniciar o próximo agente...")
        time.sleep(10) # Pausa a execução por 10 segundos
        print("⏰ Tempo esgotado! Continuando o fluxo...")
        print("="*80 + "\n")
        ### FIM DO BLOCO DE PAUSA ###

        # --- Execução do Agente B ---
        resultado_final = meus_agentes["Roteirista de Vídeo Curto"].executar(
            tarefa="Crie um roteiro de vídeo curto para a primeira ideia de negócio apresentada.",
            contexto=resultado_agente_A
        )
        print("\n--- Resultado do Agente B [Roteirista] ---")
        print(formatar_texto(resultado_final))
        
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
