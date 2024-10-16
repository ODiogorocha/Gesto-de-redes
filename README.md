
# 🚀 Ferramenta de Monitoramento de Rede - Gestão de Redes

Bem-vindo ao repositório do projeto de **Gestão de Redes** desenvolvido para o curso de **Sistemas de Informação** da **Universidade Federal de Santa Maria (UFSM)**. Este projeto faz parte de uma série de trabalhos práticos voltados para o gerenciamento eficiente de redes, com foco na descoberta de dispositivos, monitoramento em tempo real e análise de mudanças em redes locais.

## 📋 Visão Geral

Este projeto implementa uma **ferramenta de descoberta de dispositivos** na rede local, com funcionalidades avançadas que permitem o monitoramento contínuo e detalhado dos dispositivos conectados. Além disso, ele mantém um histórico dos dispositivos e destaca mudanças na rede, como a adição de novos dispositivos ou a desconexão de dispositivos existentes.

### Funcionalidades Principais:

- 🔍 **Descoberta de Dispositivos**: Identifica todos os dispositivos ativos na rede, exibindo informações como endereço IP, endereço MAC e fabricante.
- 💾 **Histórico de Varreduras**: Armazena os resultados de varreduras anteriores, permitindo detectar mudanças na rede.
- ⚡ **Detecção de Mudanças**: Monitora novos dispositivos conectados e identifica dispositivos que se desconectaram.
- 🏷️ **Classificação de Dispositivos**: Diferencia entre **roteador** e **hosts**.
- 📅 **Primeira Descoberta**: Registra o horário da primeira descoberta de cada dispositivo.

## 🎯 Objetivo do Projeto

O principal objetivo deste projeto é oferecer uma solução prática e modular para monitoramento de redes locais, permitindo que administradores de rede e estudantes da área identifiquem de maneira eficiente a presença e a atividade de dispositivos conectados. Esta ferramenta também oferece insights em tempo real sobre mudanças e eventos de rede, ajudando a garantir o controle e a segurança do ambiente.

## 🔧 Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Nmap**: Ferramenta de código aberto para descoberta de rede e auditoria de segurança.
- **Bibliotecas**:
  - `python-nmap`: Para integração com o Nmap.
  - `json`: Para armazenar e manipular o histórico de dispositivos.
  - `socket`, `struct`: Para obtenção do gateway da rede.
  - `datetime`: Para registrar o horário da descoberta.

## 🚀 Como Usar

### Pré-requisitos:

- **Instale o Nmap** no seu sistema:
  ```bash
  sudo apt install nmap
  ```
- **Instale as dependências Python**:
  ```bash
  pip install python-nmap
  ```

### Executando a Ferramenta:

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/rede-monitoramento.git
   cd rede-monitoramento
   ```

2. Execute o script principal:
   ```bash
   python monitoramento_rede.py
   ```

3. O programa irá escanear a rede local e exibir informações sobre os dispositivos conectados, atualizando a cada 60 segundos. 

### Exemplo de Saída:

```bash
Escaneando a rede 192.168.1.0/24...
Gateway (roteador) da rede: 192.168.1.1
Novos dispositivos detectados:
IP: 192.168.1.10, MAC: AA:BB:CC:DD:EE:FF, FABRICANTE: Apple, PRIMEIRA DESCOBERTA: 2024-10-16 12:30:00
Dispositivos offline:
IP: 192.168.1.5, MAC: 11:22:33:44:55:66, FABRICANTE: Samsung, PRIMEIRA DESCOBERTA: 2024-10-16 11:25:00
```

## 🌐 Estrutura de Arquivos

```text
.
├── monitoramento_rede.py  # Código principal da ferramenta
├── historico.json         # Histórico de dispositivos descobertos (gerado automaticamente)
└── README.md              # Documentação do projeto
```

## 🛠️ Funcionalidades Técnicas

1. **Descoberta e Exibição de Dispositivos**:
   - Através do Nmap, a ferramenta escaneia a rede e identifica dispositivos.
   - Exibe informações detalhadas como IP, MAC e fabricante.

2. **Histórico de Mudanças na Rede**:
   - Armazena as informações de cada varredura em um arquivo JSON.
   - Detecta novos dispositivos e aqueles que se desconectaram, informando as mudanças em tempo real.

3. **Classificação entre Roteador e Hosts**:
   - O gateway (roteador) é automaticamente identificado e diferenciado dos demais dispositivos.

4. **Monitoramento Contínuo**:
   - A ferramenta roda em loop, repetindo o escaneamento a cada minuto, garantindo que a rede seja constantemente monitorada.

## 📈 Benefícios

- **Visibilidade em Tempo Real**: Monitore sua rede com atualizações a cada 60 segundos.
- **Segurança**: Identifique rapidamente novos dispositivos que se conectam à sua rede.
- **Modularidade**: A ferramenta pode ser adaptada para outros trabalhos e funcionalidades no futuro.
- **Histórico de Atividades**: Mantenha um registro detalhado de todos os dispositivos que já foram conectados à rede.

## 💡 Próximos Passos

Este projeto é a base para trabalhos futuros na disciplina de Gestão de Redes, onde mais funcionalidades serão adicionadas, como:

- Monitoramento de tráfego em tempo real.
- Detecção de possíveis intrusões.
- Análises de performance da rede.

## 📚 Sobre a Disciplina

A disciplina de **Gestão de Redes** faz parte da grade curricular do curso de **Sistemas de Informação** da UFSM, focando no desenvolvimento de habilidades práticas para monitoramento, configuração e manutenção de redes de computadores.

**Departamento:** Computação Aplicada - Centro de Tecnologia - UFSM
