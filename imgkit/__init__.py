from typing import Literal

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from beartype import beartype

import imgkit.transformations as tfm


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

    @beartype
    def expansao_de_contraste(
        self, limite_L: int, limite_H: int, hist: bool = False
    ) -> None:
        """
        Método utilizado para expandir o contraste da imagem do objeto

        Args:
            self: Instância da classe que contém os atributos:
            - transformacao (np.ndarray): Imagem resultante de alguma
                  transformação aplicada.
              - transformacao1d (np.ndarray): Array 1D da imagem resultante de
                  alguma transformação aplicada.
            limite_L (int): (Low Limit) limite inferior da intensiade de pixels da
              imagem.
            limite_H (int): (Hight Limit) limite superior da intensidade de pixels
              da imagem.
            hist (bool): Se True, retorna a figure do histograma do array da imagem
              transformada.

        Returns:
            None.
        """
        aux_arr = []

        for pixel in self.img1d:
            args = {'pixel': pixel, 'limite_L': limite_L, 'limite_H': limite_H}
            novo_pixel = int(tfm.expansao_de_pixel(**args))
            aux_arr.append(novo_pixel)

        img_transform = np.array(aux_arr)

        self.transformacao = np.reshape(img_transform, (256, 256, 3))
        self.transformacao1d = np.array(aux_arr)

        if hist:
            self.histograma(tipo='t')

    def comparacao(self) -> None:
        """
        Exibe a imagem original e a imagem transformada lado a lado para
        facilitar a comparação visual.

        Args:
            self: Instância da classe que contém os atributos:
                - img (np.ndarray): Imagem original.
                - transformacao (np.ndarray): Imagem resultante de alguma
                  transformação aplicada.

        Returns:
            None
        """
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        axs[0].imshow(self.img, cmap='gray')
        axs[0].set_title('Original')
        axs[0].axis('off')

        axs[1].imshow(self.transformacao, cmap='gray')
        axs[1].set_title('Transformada')
        axs[1].axis('off')

        plt.show()
