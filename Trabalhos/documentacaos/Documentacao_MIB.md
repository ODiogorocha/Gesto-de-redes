
# Documentação da MIB: MINHA-REDE-MIB

## Introdução

Esta MIB (Management Information Base) é projetada para o monitoramento básico de dispositivos em uma rede local. Ela define uma série de objetos que podem ser consultados via SNMP (Simple Network Management Protocol) para obter informações sobre o estado e o desempenho dos dispositivos.

## Estrutura da MIB

A MIB é dividida em várias seções, incluindo importações, definição do módulo e definição de objetos. 

### Importações

```plaintext
IMPORTS
    MODULE-IDENTITY, OBJECT-TYPE, Counter32, Gauge32, Integer32, IpAddress, enterprises
        FROM SNMPv2-SMI;
```
Esta seção importa tipos e definições necessários da MIB SNMPv2-SMI, que são utilizados para criar objetos dentro da MIB.

### Definição do Módulo

```plaintext
moduloMinhaRede MODULE-IDENTITY
    LAST-UPDATED "202410300000Z"
    ORGANIZATION "Minha Empresa de Tecnologia"
    CONTACT-INFO
       
    DESCRIPTION
        "MIB para monitoramento básico de dispositivos em uma rede local."
    ::= { enterprises 99999 }
```

- **LAST-UPDATED**: Data da última atualização da MIB.
- **ORGANIZATION**: Nome da organização responsável pela MIB.
- **CONTACT-INFO**: Informações de contato para suporte técnico.
- **DESCRIPTION**: Uma breve descrição da finalidade da MIB.
- **Identificador**: A MIB é identificada como parte do namespace `enterprises` com o número `99999`.

### Objetos Definidos

Os objetos definidos na MIB são usados para coletar informações específicas dos dispositivos na rede. Cada objeto possui um identificador único e um tipo de dado associado.

#### 1. Status do Dispositivo

```plaintext
statusDispositivo OBJECT-TYPE
    SYNTAX      INTEGER { ativo(1), inativo(2), manutencao(3) }
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Status atual do dispositivo. Valores possíveis:
         - ativo (1): Dispositivo está online.
         - inativo (2): Dispositivo está offline.
         - manutencao (3): Dispositivo em manutenção."
    ::= { objetosMinhaRede 1 }
```
- **Descrição**: Indica se o dispositivo está ativo, inativo ou em manutenção.

#### 2. Contagem de Pacotes Recebidos

```plaintext
contagemPacotesRecebidos OBJECT-TYPE
    SYNTAX      Counter32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Número de pacotes recebidos pelo dispositivo desde o último reinício."
    ::= { objetosMinhaRede 2 }
```
- **Descrição**: Total de pacotes recebidos pelo dispositivo desde o último reinício.

#### 3. Contagem de Pacotes Enviados

```plaintext
contagemPacotesEnviados OBJECT-TYPE
    SYNTAX      Counter32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Número de pacotes enviados pelo dispositivo desde o último reinício."
    ::= { objetosMinhaRede 3 }
```
- **Descrição**: Total de pacotes enviados pelo dispositivo desde o último reinício.

#### 4. Nome do Dispositivo

```plaintext
nomeDispositivo OBJECT-TYPE
    SYNTAX      OCTET STRING (SIZE (0..255))
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Nome de identificação do dispositivo na rede."
    ::= { objetosMinhaRede 4 }
```
- **Descrição**: Nome que identifica o dispositivo na rede, com tamanho máximo de 255 caracteres.

#### 5. Endereço IP do Dispositivo

```plaintext
enderecoIPDispositivo OBJECT-TYPE
    SYNTAX      IpAddress
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Endereço IP do dispositivo."
    ::= { objetosMinhaRede 5 }
```
- **Descrição**: Armazena o endereço IP do dispositivo.

#### 6. Nível de Carga da CPU (em %)

```plaintext
cargaCPU OBJECT-TYPE
    SYNTAX      Gauge32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Nível atual de carga da CPU do dispositivo, expresso em porcentagem."
    ::= { objetosMinhaRede 6 }
```
- **Descrição**: Indica o nível atual de uso da CPU do dispositivo em porcentagem.

#### 7. Temperatura do Dispositivo (em °C)

```plaintext
temperaturaDispositivo OBJECT-TYPE
    SYNTAX      Gauge32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Temperatura atual do dispositivo, medida em graus Celsius."
    ::= { objetosMinhaRede 7 }
```
- **Descrição**: Temperatura atual do dispositivo em graus Celsius.

#### 8. Tempo de Atividade do Dispositivo (em segundos)

```plaintext
tempoAtividadeDispositivo OBJECT-TYPE
    SYNTAX      Integer32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
        "Tempo total de atividade do dispositivo desde o último reinício, em segundos."
    ::= { objetosMinhaRede 8 }
```
- **Descrição**: Tempo total em segundos que o dispositivo esteve ativo desde o último reinício.

## Conclusão

Esta MIB fornece um conjunto de objetos úteis para o monitoramento de dispositivos em uma rede local. Ela pode ser utilizada com ferramentas compatíveis com SNMP para coletar informações e monitorar o estado dos dispositivos, ajudando na manutenção e gerenciamento da rede.

