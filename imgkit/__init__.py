from typing import Literal

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from beartype import beartype



class Imagem:
    """
    Classe feita para operações básicas de imagem da disciplina de Processamento
    de imagens
    """

    @beartype
    def __init__(self, caminho) -> None:
        """
        Inicializa uma nova instância imagem.

        Args:
            caminho (str): Caminho do arquivo da imagem.
        """
        img = cv2.imread(caminho)

        if img is None:
            raise ValueError('Imagem inválida: valor None recebido')

        self.img = img
        self.img1d = np.reshape(self.img, -1)
        self.transformacao = np.array([])
        self.transformacao1d = np.array([])

    def __repr__(self) -> str:
        plt.imshow(self.img)
        plt.show()
        return f'<Imagem: shape={self.img.shape}, dtype={self.img.dtype}>'

    @beartype
    def histograma(self, tipo: Literal['o', 't'] = 'o') -> None:
        """
        Método da classe que plota o histograma das imagens

        Args:
          tipo (Literal["t", "o"]): String que pode ser apenas:
                - "o": para histograma da imagem original
                - "t": para histograma da imagem transformada
        """
        arr = self.img1d if tipo == 'o' else self.transformacao1d

        data = {'intensidade': arr}
        df = pd.DataFrame(data)
        df = df['intensidade'].value_counts().reset_index()
        plt.figure(figsize=(8, 6))
        plt.bar(df['intensidade'], df['count'])
        plt.show()

