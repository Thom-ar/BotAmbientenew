import os
import random
from datetime import time, timezone

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv


load_dotenv()

DICAS = [
    "Desligue aparelhos da tomada quando não estiverem em uso.",
    "Prefira iluminação natural sempre que puder.",
    "Feche a torneira enquanto escova os dentes.",
    "Separe recicláveis e mantenha-os limpos e secos.",
    "Evite comprar produtos com embalagens descartáveis.",
    "Troque sacolas plásticas por sacolas reutilizáveis.",
    "Use garrafas reutilizáveis em vez de descartáveis.",
    "Reutilize potes de vidro para armazenar alimentos.",
    "Doe roupas e objetos que não utiliza mais.",
    "Prefira transporte coletivo, bicicleta ou caminhada.",
    "Reduza o desperdício de comida planejando as refeições.",
    "Composte restos de frutas, verduras e folhas.",
    "Use o verso de folhas de papel antes de reciclar.",
    "Conserte aparelhos e roupas antes de substituí-los.",
    "Procure um ponto de coleta adequado para pilhas e eletrônicos.",
]


def criar_embed(titulo: str, descricao: str) -> discord.Embed:
    embed = discord.Embed(
        title=titulo,
        description=descricao,
        color=discord.Color.green(),
    )
    embed.set_footer(text="Bot Ecoconsciência - cuide do planeta todos os dias")
    return embed


class EcoBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()
        dica_automatica.start()


bot = EcoBot()


@bot.event
async def on_ready() -> None:
    print(f"Bot conectado como {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="o planeta ficar mais verde",
        )
    )


@bot.tree.command(name="dica", description="Receba uma dica para ajudar o meio ambiente.")
async def dica(interacao: discord.Interaction) -> None:
    await interacao.response.send_message(
        embed=criar_embed("Dica ecológica", random.choice(DICAS))
    )


@bot.tree.command(name="desafio", description="Receba um desafio ambiental para hoje.")
async def desafio(interacao: discord.Interaction) -> None:
    desafios = [
        "Hoje, economize água tomando banhos mais curtos.",
        "Passe o dia sem usar copos descartáveis.",
        "Separe pelo menos um item reciclável corretamente.",
        "Alimente-se sem desperdiçar nenhum alimento.",
        "Use um meio de transporte mais sustentável.",
        "Encontre um objeto em casa que possa ser reutilizado.",
    ]
    await interacao.response.send_message(
        embed=criar_embed("Desafio do dia", random.choice(desafios))
    )


@bot.tree.command(name="sobre", description="Conheça o objetivo deste bot.")
async def sobre(interacao: discord.Interaction) -> None:
    mensagem = (
        "Sou um bot criado para compartilhar dicas simples de sustentabilidade.\n"
        "Use `/dica` para receber uma sugestão ou `/desafio` para aceitar "
        "uma ação ecológica para o dia."
    )
    await interacao.response.send_message(
        embed=criar_embed("Sobre o Ecoconsciência", mensagem),
        ephemeral=True,
    )


@tasks.loop(time=time(hour=9, minute=0, tzinfo=timezone.utc))
async def dica_automatica() -> None:
    canal_id = os.getenv("CANAL_DICAS_ID")
    if not canal_id:
        return

    canal = bot.get_channel(int(canal_id))
    if canal is not None:
        await canal.send(embed=criar_embed("Dica ecológica do dia", random.choice(DICAS)))


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError(
            "Defina DISCORD_TOKEN no arquivo .env ou nas variáveis de ambiente."
        )

    bot.run(token)