# Identificação de talhão

Este projeto utiliza uma rede neural para o reconhecimento de talhões em imagens de satélite. 

As imagens baixadas do Sentinel-2 servem como base para o treinamento da rede. A partir de um arquivo shapefile, é possível extrair os valores dos pixels que se sobrepõem 
nas imagens de satélite. As entradas da rede consistem dos pixels extraídos das bandas 02 vermelho, 03 verde, 04 azul e 08 infravermelho, além do valor do NDVI que é um 
número entre -1 e 1 representando os diferentes estados de uma plantação (banda infravermelho - vermelho / banda infravermelho + vermelho).

## Shapefile 


