## 🚩 Nesse tutorial vamos criar, testar e "deployar" um contrato escrito em `Vyper` usando o framework `ApeWorx`.

---

## 💾 Tecnologias que vamos usar:

- `Vyper`: linguagem para criar o contrato
- `Pyteste`: _framework_ de testes para linguagem `Python`
- `ApeWorX`: _framework_ de "_workflow_" para construir contratos usando a linguagem `Python`

**⚠️ Referências**
**[Repositório Flipper](https://github.com/olivmath/flipper)**
**[Documentação do Ganache](https://trufflesuite.com/docs/ganache/)**
**[Documentação do ApeWorX](https://docs.apeworx.io/ape/stable/)**
**[_Academy_ do ApeWorX](https://academy.apeworx.io)**

---

## 🔄 Comparações

![teorema de tales](https://web3dev-forem-production.s3.amazonaws.com/uploads/articles/6sm3j26w78687qv1v6da.png)

- [teorema de tales](<https://pt.wikipedia.org/wiki/Teorema_de_Tales_(interseção)>)

> `Solidity` está para o `Vyper` assim como o `HardHat` está para o `ApeWorX`
>
> `Jest` está para o `Pytest` assim como o `JavaScript` está para o `Python`

Brincadeiras a partes, o _workflow_ para escrever contratos é mesmo independente da _stack_:

1. Escrever o contrato.
2. Testar de forma automatizada.
3. Fazer deploy local >> testnet >> mainnet.

O contrato consiste apenas em salvar um variável "boolena" que tem a possibilidade de trocar de estato ou seja "flipar" quando alguém chama uma função do contrato. Portanto nosso contrato terá apenas uma variável um evento e uma função.

---

## 🌳 Ambiente:

**[🚨 Instale o Python antes](https://www.python.org/downloads/)**
**[🚨 Instale também o Ganache](https://github.com/trufflesuite/ganache)**

Instale o `ApeWorX`:

```
pip install eth-ape
```

ou

```
poetry add eth-ape
```

E o plugin do `Vyper`:

```
ape plugins install vyper
```

Crie um pasta vazia e "rode":

```
ape init
```

O terminal vai te pedir o nome do projeto, em seguida "dê _enter_".
O `ape` vai criar uma estrutura de diretórios pra você:

```
contracts/
interfaces/
scripts/
tests/
ape-config.yaml
```

Por fim precisamos adicionar um plugin para que o `ape` baixe o compilador do `Vyper`, por padrão ele tem apenas o compilador do `Solidity`.
Abra o arquivo `ape-config.yaml` e adicione o seguinte:

```yaml
name: flipper
plugins:
  - name: vyper
```

---

## 🐍 Contrato: `Vyper`

Crie um arquivo dentro do diretório `contracts` chamado `Flipper.vy`.
**🚨 Você pode trocar os nomes, se souber o que está fazendo**

### Crie a váriavel `flip`.

```py
flip: public(bool)
```

- As variáveis globais do contrato são declaradas no início e depois acessadas com `self.nome_da_variável`, nesse caso: `self.flip`.
- O `Vyper` gera um `getter` automaticamente quando a declaração da variável usa o `public`.

### Crie o evento `Fliped`.

```py
event Fliped:
    state: bool
```

- Evento é um recurso que possibilita o envio de dados em tempo real apartir de um full-node para um cliente qualquer.
- Aqui ele será usado para notificar quando o estato do `flip` for alterado.

### Crie o construtor `__init__`:

```py
@external
def __init__():
    self.flip = True
```

- O [decorator](https://realpython.com/primer-on-python-decorators/#syntactic-sugar) `external` restringe a função a ser chamada apenas via transação ou por outro contrato e não pode ser chamada internamente.
- `__init__` é o construtor _default_ do Python.
- `self` aqui indica que a variável "é do próprio contrato", `self` é o mesmo que `this` em outras linguagens.
- Um contrato em `Vyper` é como criar uma classe em `Python`.

### Crie a função `flipping`:

```py
@external
def flipping() -> bool:
  self.flip = not self.flip
  log Fliped(self.flip)
  return self.flip
```

- A função `flipping` acessa o `flip` por meio do `self` e "flipa" o valor dela, se for `true` "vira" `false` e o inverso.
- Depois envia o evento `Fliped` para notificar que o estado do contrato foi alterado.
- Por fim retorna o novo estado do contrato.

### 🏁 Contrato completo

```py
# @version ^0.3.0

flip: public(bool)

event Fliped:
  state: bool

@external
def __init__():
  self.flip = True

@external
def flipping() -> bool:
  self.flip = not self.flip
  log Fliped(self.flip)
  return self.flip
```

---

## 🧪 Testes: `Ape` + `Python` + `Pytest`

Agora vamos testar o contrato pra saber se ele se comporta como esparamos, pra isso vamos usar o `Ape`, `Pytest` e `Python`.
**🚨 Você pode usar outro _framework_, se souber o que está fazendo**

- `Python` é a linguagem de programação, assim como o `JavaScript`.
- `Pytest` é o mais maduro _framework_ de teste do ambiente `Python`, assim como o `Jest`.
- `ApeWorX` é um _framework_ escrito em `Python` para compilar, testar, e implantar contratos, assim como o `HardHat`.

Dentro do diretório `tests` crie dois arquivos:

```
tests/
    conftest.py
    test_flipper.py
```

- `conftest.py` é o primeiro arquivo que o `Pytest` vai procurar para iniciar os testes, nele vamos configurar nossas [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), **não mude o nome desse arquivo**.
- `test_flipper.py` é onde vamos escrever os testes do contrato, **pode trocar por qualquer nome que comece com `test_*.py` ou termine com `*_test.py`**.

### Crie as `fixtures` em `conftest.py`

```py
from pytest import fixture

@fixture
def owner(accounts):
    return accounts[0]

@fixture
def another(accounts):
    return accounts[1]

@fixture
def flipper(project, owner):
    return owner.deploy(project.Flipper)
```

- `Fixture` é um tema massa por si só, de forma simples, são funções que vão ser executadas antes dos testes pricipais e que podemos usar seu retorno dentro dos testes.
- `owner` gera um endereço aleatório que vamos usar para "deployar" o contrato.
- `another` gera um endereço aleatório que vamos usar "chamar" com o contrato.
- `flipper` é a instancia do contrato depois de "deployar".

### Crie os testes em `test_flipper.py`

**✅ Teste o estado inicial do contrato**

```py
def test_flipper_initial(flipper):
    assert flipper.flip() == True
```

- Aqui vamos validar se o contrato realmente inicia com o valor de `flip` como `true`.

**✅ Teste o estado do contrato depois de um `flipping`**

```py
def test_change_flip(flipper, another):
    flipper.flipping(sender=another)
    assert flipper.flip() == False
```

- Depois de `another` "flipar" nosso contrato o estato deve inverter para `false`.

**✅ Teste se o contrato emite um evento depois de ser "flipado"**

```py
def test_get_fliped_event(flipper, another):
    tx = flipper.flipping(sender=another)
    event_list = tx.decode_logs(flipper.Fliped)
    event = event_list[0].event_arguments

    assert event == {"state": False}
```

- Depois de `another` "flipar" nosso contrato armazenamos o retorno em `tx`.
- `tx` contém os logs do momento que a transação `flipping` foi feita.
- Então precisamos fazer o _decode_ do nosso evento.
- Por fim, pegamos o primeiro evento e comparamos se ele tem a chave `state` e o valor `false`.

---

## 🚀 Deploy

Por fim vamos fazer o deploy em uma rede local usando o `ganache`.

Coloque no arquivo `ape-config.yaml`:

```yaml
geth:
  ethereum:
    mainnet:
      uri: http://127.0.0.1:8545
```

Agora precisamos de uma carteira que tenha ETH para fazer o deploy.
Inicie o `ganache` que ele irá gerar algumas.

```
ganache -s "SEED"
```

**⚠️ Usando o `-s` podemos passar um valor qualquer para que o ganache crie carteiras de forma determinística**

Pegue uma chave privada do `ganache` e **⚠️ abra outro terminal** para importar ela no `ape`:

```
ape accounts import my_wallet
Enter Private Key: COLE_A_CHAVE_PRIVADA_AQUI
Create Passphrase: CRIE_UMA_SENHA
Repeat for confirmation: CRIE_UMA_SENHA
SUCCESS: A new account 'SEU_ENDEREÇO_AQUI' has been added with the id 'my_wallet'
```

Por último coloque no arquivo `scripts/deploy.py` o conteúdo do deploy:

```py
def main():
    from ape import project, accounts

    owner = accounts.load("my_wallet")
    owner.deploy(project.Flipper)
```

Para "deployar" o contrato "rode" no terminal:

```
ape run deploy --network ::geth
```

**⚠️ Lembrando que o `ganache` precisa estar "rodando"**

## ⏭ Próximos passos

- Interagir com seu contrato pelo console.
- Lançar o contrato em uma testnet.
