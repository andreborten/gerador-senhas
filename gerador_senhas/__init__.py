"""Geração local de senhas com aleatoriedade criptográfica."""
from .core import gerar_senha

from .forca import Avaliacao, avaliar_configuracao

__all__ = ["gerar_senha", "Avaliacao", "avaliar_configuracao"]
