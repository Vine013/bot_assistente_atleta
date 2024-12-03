from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Função para iniciar o bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Olá! Eu sou seu assistente de treino e dieta. Escolha uma opção:\n"
        "/dieta - Para receber uma dieta personalizada.\n"
        "/treino - Para receber uma rotina de treino personalizada."
    )

# Função para processar a dieta
async def dieta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Inicia o fluxo de perguntas para dieta
    await update.message.reply_text("Qual seu peso atual?")

    # Salva o estado atual como 'dieta_peso'
    context.user_data["state"] = "dieta_peso"

# Função para processar o treino
async def treino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Inicia o fluxo de perguntas para treino
    await update.message.reply_text("Qual seu peso atual?")
    context.user_data["state"] = "treino_peso"

# Função para lidar com as mensagens e fluxos de perguntas
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtém a mensagem enviada pelo usuário
    user_input = update.message.text

    # Verifica qual estado o usuário está (dieta ou treino)
    state = context.user_data.get("state")

    # Fluxo para dieta
    if state == "dieta_peso":
        context.user_data["peso"] = user_input
        await update.message.reply_text("Qual o seu objetivo? (emagrecer ou ganhar massa)")
        context.user_data["state"] = "dieta_objetivo"

    elif state == "dieta_objetivo":
        objetivo = user_input.lower()
        peso = context.user_data.get("peso")
        if objetivo == "emagrecer":
            resposta = (
                f"Dieta para emagrecer baseada no seu peso atual ({peso}kg):\n"
                "✅ Café da manhã: Omelete de claras e suco verde.\n"
                "✅ Almoço: Salada, peito de frango grelhado e arroz integral.\n"
                "✅ Lanches: Frutas e oleaginosas.\n"
                "✅ Jantar: Sopa de legumes.\n"
                "Coma 5 refeições leves ao longo do dia."
            )
        elif objetivo == "ganhar massa":
            resposta = (
                f"Dieta para ganhar massa baseada no seu peso atual ({peso}kg):\n"
                "✅ Café da manhã: Panqueca de aveia, ovos e banana.\n"
                "✅ Almoço: Carne magra, batata doce e legumes.\n"
                "✅ Lanches: Frutas, iogurte e pasta de amendoim.\n"
                "✅ Jantar: Filé de salmão e arroz integral.\n"
                "Coma 6 refeições bem distribuídas ao longo do dia."
            )
        else:
            resposta = "Objetivo inválido. Por favor, escolha entre 'emagrecer' ou 'ganhar massa'."
        await update.message.reply_text(resposta)
        context.user_data["state"] = None  # Reseta o estado
        await update.message.reply_text("Deseja criar uma rotina de treino? Use /treino.")

    # Fluxo para treino
    elif state == "treino_peso":
        context.user_data["peso"] = user_input
        await update.message.reply_text("Qual o seu objetivo? (condicionamento ou hipertrofia)")
        context.user_data["state"] = "treino_objetivo"

    elif state == "treino_objetivo":
        objetivo = user_input.lower()
        peso = context.user_data.get("peso")
        if objetivo == "condicionamento":
            resposta = (
                f"Treino de condicionamento baseado no seu peso atual ({peso}kg):\n"
                "🏋️ Segunda: Corrida leve por 30 minutos + alongamento.\n"
                "🏋️ Terça: Treino de musculação com foco em membros superiores.\n"
                "🏋️ Quarta: Circuito funcional de 40 minutos.\n"
                "🏋️ Quinta: Treino de musculação com foco em membros inferiores.\n"
                "🏋️ Sexta: Bicicleta ergométrica por 45 minutos.\n"
                "Treine 3 vezes por semana, com duração média de 1 hora."
            )
        elif objetivo == "hipertrofia":
            resposta = (
                f"Treino de hipertrofia baseado no seu peso atual ({peso}kg):\n"
                "🏋️ Segunda: Peito e tríceps.\n"
                "🏋️ Terça: Costas e bíceps.\n"
                "🏋️ Quarta: Pernas e glúteos.\n"
                "🏋️ Quinta: Ombros e abdômen.\n"
                "🏋️ Sexta: Corpo inteiro (treino funcional).\n"
                "Treine 5 vezes por semana, com duração média de 1h30min."
            )
        else:
            resposta = "Objetivo inválido. Por favor, escolha entre 'condicionamento' ou 'hipertrofia'."
        await update.message.reply_text(resposta)
        context.user_data["state"] = None  # Reseta o estado
        await update.message.reply_text("Deseja criar uma dieta personalizada? Use /dieta.")

    else:
        # Mensagem padrão caso o comando não seja reconhecido
        await update.message.reply_text("Por favor, escolha entre /dieta ou /treino.")

# Configuração do bot
def main() -> None:
    application = Application.builder().token("7772461182:AAHPF6HS_06fbsf0zG5AKJ7dsgWPqS0XcYk").build()

    # Adiciona os comandos e handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dieta", dieta))
    application.add_handler(CommandHandler("treino", treino))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia o bot
    application.run_polling()

if __name__ == "__main__":
    main()
