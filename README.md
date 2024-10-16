Aqui está um exemplo de README voltado para a matéria de **Gestão de Redes** do curso de **Sistemas de Informação**. Esse README está estruturado para o primeiro trabalho da disciplina, focado em uma ferramenta de descoberta de dispositivos de rede.

---

# Gestão de Redes - Sistemas de Informação

Este repositório contém os trabalhos desenvolvidos ao longo da disciplina de **Gestão de Redes** no curso de **Sistemas de Informação** da **Universidade Federal de Santa Maria (UFSM)**. A disciplina explora conceitos e práticas de redes de computadores, com ênfase na gestão e monitoramento de redes.

## Trabalho 1: Ferramenta de Descoberta de Dispositivos na Rede

O primeiro trabalho consiste no desenvolvimento de uma ferramenta capaz de realizar a descoberta de dispositivos em uma rede local. A ferramenta deve manter um histórico das varreduras, registrar novos dispositivos e dispositivos que ficaram offline, além de exibir informações detalhadas como IP, MAC, fabricante e horário da descoberta.

### Objetivos do Trabalho

- **Descobrir dispositivos** conectados à rede local.
- **Classificar dispositivos** entre roteador e hosts.
- **Registrar histórico** de varreduras, armazenando mudanças como novos dispositivos e dispositivos offline.
- **Utilizar Python** e a biblioteca Nmap para realizar o escaneamento de rede.

### Requisitos

- Linguagem de Programação: **Python**
- Bibliotecas Utilizadas: 
  - `python-nmap` para realizar os scans de rede.
  - `json` para manipulação do histórico.
  - Outras bibliotecas nativas do Python (`socket`, `struct`, `datetime`).

### Estrutura do Projeto

```text
.
├── monitoramento_rede.py  # Código principal para monitoramento de rede
├── historico.json         # Arquivo gerado automaticamente para salvar histórico de dispositivos
└── README.md              # Arquivo de documentação do projeto
```

### Funcionalidades

1. **Descoberta de Dispositivos**:
   - Utiliza o `Nmap` para escanear a rede e listar os dispositivos conectados.
   - Exibe informações de IP, MAC, fabricante e o horário da primeira descoberta.

2. **Classificação de Dispositivos**:
   - Identifica o roteador (gateway da rede) e o diferencia dos outros dispositivos (hosts).

3. **Histórico de Dispositivos**:
   - Mantém um histórico de todos os dispositivos descobertos, salvando-o em um arquivo JSON.
   - Detecta novos dispositivos e aqueles que ficaram offline ao longo do tempo.

4. **Relatórios de Mudanças**:
   - Informa sempre que houver um novo dispositivo ou quando algum dispositivo desconectar-se da rede.

### Como Executar

1. **Instalação do Nmap**:

   Certifique-se de que o Nmap está instalado no seu sistema:

   ```bash
   sudo apt install nmap  # No Ubuntu
   ```

2. **Instalação das Dependências**:

   Execute o seguinte comando para instalar a biblioteca `python-nmap`:

   ```bash
   pip install python-nmap
   ```

3. **Execução do Monitoramento**:

   Após clonar o repositório, execute o script principal:

   ```bash
   python monitoramento_rede.py
   ```

   O script irá escanear a rede local e exibir os dispositivos encontrados. Ele continuará rodando, repetindo o escaneamento a cada 60 segundos.

### Exemplo de Saída

```bash
Escaneando a rede 192.168.1.0/24...
Gateway (roteador) da rede: 192.168.1.1
Novos dispositivos detectados:
IP: 192.168.1.5, MAC: AA:BB:CC:DD:EE:FF, FABRICANTE: Desconhecido, PRIMEIRA DESCOBERTA: 2024-10-16 10:30:00
Dispositivos offline:
IP: 192.168.1.10, MAC: 11:22:33:44:55:66, FABRICANTE: XYZ Corp, PRIMEIRA DESCOBERTA: 2024-10-16 09:25:00
```

### Estrutura de Dados

O histórico é salvo no arquivo `historico.json`, que contém a seguinte estrutura:

```json
[
  {
    "ip": "192.168.1.5",
    "mac": "AA:BB:CC:DD:EE:FF",
    "fabricante": "Desconhecido",
    "primeira_descoberta": "2024-10-16 10:30:00",
    "tipo": "Host"
  },
  ...
]
```

## Proposta da Disciplina

Ao longo da disciplina de **Gestão de Redes**, diversos trabalhos práticos serão desenvolvidos para entender e aplicar conceitos de gerenciamento e monitoramento de redes. O objetivo é familiarizar os alunos com as ferramentas e práticas utilizadas no gerenciamento de redes, preparando-os para enfrentar desafios reais no mercado de trabalho.

Este repositório será atualizado com os próximos trabalhos à medida que a disciplina avançar.

## Como Contribuir

Contribuições para melhorias são bem-vindas! Para enviar sugestões ou correções:

1. Faça um **fork** deste repositório.
2. Crie uma **branch** com a sua modificação (`git checkout -b minha-modificacao`).
3. Realize suas mudanças e faça o **commit** (`git commit -m 'Descrição das mudanças'`).
4. Envie as mudanças para o seu **fork** (`git push origin minha-modificacao`).
5. Abra um **Pull Request** para este repositório.

---

**Professor:** Carlos Raniery P. dos Santos  
**Disciplina:** Gestão de Redes  
**Departamento:** Computação Aplicada, Centro de Tecnologia - UFSM

**Aluno(s):** Nome(s) do(s) aluno(s) do grupo

---

Esse README proporciona uma explicação completa para o primeiro trabalho da disciplina, apresentando objetivos, estrutura do projeto, requisitos e como executá-lo.