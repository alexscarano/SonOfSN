# SonOfSN — Bot de Monitoramento de Bitcoin (Discord)

Um bot em **Python (discord.py)** que monitora o preço do **Bitcoin (BTC)** em tempo real, envia **notificações automáticas** quando o preço ultrapassa limites definidos, gera **gráficos de variação** e realiza **conversões entre BTC, USD e BRL**.

## Funcionalidades

**Monitoramento automático**
- O bot verifica o preço periodicamente e envia mensagens.

 **Gráfico de preço (24h / 7d / 1m / 6m)**
- Gera um gráfico com base em dados do **CoinGecko** mostrando a variação de preço.
- O gráfico é enviado como imagem no embed do Discord.

**Conversão de moedas**
- Converte o valor de **BTC → USD** e **BTC → BRL**, com base no preço atual.
- Pode ser usado em tempo real via comando.

## Tecnologias utilizadas

- **Python 3.11+**
- **discord.py** (para integração com o Discord)
- **requests** (para comunicação com APIs externas)
- **matplotlib** (para geração dos gráficos)
- **CoinGecko API** (para dados de mercado)
