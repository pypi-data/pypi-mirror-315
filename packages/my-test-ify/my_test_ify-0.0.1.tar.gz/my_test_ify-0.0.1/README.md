# my-test-ify - Micro-Framework de Testes, Modular e Funcional

### Descrição

my-test-ify é a evolução do Test.py, projetado para ser um test-if de testes modular e extensível, criado com o objetivo de atender a uma variedade de cenários de teste sem a necessidade de dependências ou configurações complexas. Inspirado pelo feedback e pela prática contínua, o my-test-ify utiliza o paradigma funcional para criar uma estrutura minimalista, de fácil adaptação e com foco em modularidade.

### Propósito

Após uma avaliação do Test.py, surgiu a necessidade de criar um framework mais flexível, que pudesse servir de referência para estudos e ser adaptado conforme a necessidade. A ideia central é fornecer uma estrutura minimalista onde o usuário possa adicionar novos tipos de teste com simplicidade, evitando dependências adicionais e mantendo uma curva de aprendizado baixa.

### Escolha pelo Paradigma Funcional

A decisão de implementar o my-test-ify no paradigma funcional foi motivada pelo desejo de explorar esse paradigma em situações práticas. Além de oferecer uma oportunidade de aprendizado, a abordagem funcional favorece a modularidade e a criação de testes isolados e de fácil reutilização. Caso a solução funcional não atendesse às expectativas de extensibilidade, há um plano de transição para POO, com uso de padrões como Strategy e Template Method.

### Funcionalidades e Estrutura Modular

- Funções de Teste Modulares: Cada teste é uma função independente que retorna um valor booleano e uma mensagem personalizada. Isso permite adicionar novos tipos de teste facilmente.
- Relatório e Resumo: my-test-ify inclui funções para exibir o resultado de cada teste, uma pilha de erros (stack trace) detalhada e um resumo final.
- Gerenciamento Centralizado de Testes: O núcleo do my-test-ify organiza e disponibiliza as informações dos testes, mantendo um baixo acoplamento entre as funções de teste e o módulo principal.
- Facilidade para Adicionar Novos Testes: Novos testes podem ser adicionados como funções independentes e registradas no núcleo, mantendo o sistema simples e de fácil manutenção.

### Exemplo de Uso

O código a baixo esta no arquivo `main.py`, que esta na raiz do projeto:

```python
from my_test_ify import my_test_ify

# Inicialização das funções do módulo testify
core, report = my_test_ify()

# O teste de igualdade é implicitamente chamado quando o quarto parâmetro de core é omitido.
core(1, 1, "Testando igualdade de inteiros")
core("Hello", "Hello", "Testando igualdade de strings")
core(4.0, 4.0, "Testando igualdade de números com ponto flutuante")

from my_test_ify.assertive import (greater_than, less_than, not_equals,
                                   raises_exception)
from my_test_ify.exceptions import TestFunctionError

core(1, 3, "Testando desigualdade de inteiros", not_equals)
core(3, 2, "Testando se é maior que", greater_than)
core(2, 3, "Testando se é menor que", less_than)

def func (a: int):
    raise TestFunctionError("Teste de exceção")

# O quinto parâmetro de core é uma lista de argumentos que são passados pela função testada. Neste caso, a função `func`.
core(TestFunctionError, func, "test8", raises_exception, [1])


print(report.report()) # Imprime o relatório de testes
print(report.failure_stack()[0]) # Imprime o stack da primeira falha, caso haja falhas. Se não houver falhas, imprime "No failures".
print(report.summary()) # Imprime o resumo dos testes

```

### Principais Desafios

Um dos principais desafios foi a adaptação ao paradigma funcional, incluindo o uso de funções puras e a manipulação de variáveis no escopo de função, simulando o encapsulamento sem modificadores de visibilidade. Essa prática trouxe aprendizado valioso, com especial atenção para funções puras e encapsulamento através de variáveis locais.

### Futuro do Projeto

O my-test-ify ainda está em fase inicial e poderá ser aplicado a futuros projetos. Com a modularidade alcançada, o próximo passo é validar sua flexibilidade e extensibilidade.

Pretendo continuar a evolução do my-test-ify, adicionando recursos e melhorias ao longo do tempo, mas mantendo a simplicidade, a facilidade e modularidade. Crescer mantendo a filosofia minimalista é o desafio.

## Licença

Este projeto está licenciado sob a licença MIT. Para mais detalhes, veja o arquivo [LICENSE](./LICENSE).

### instalação

Para instalar o my-test-ify, siga estas etapas:

1. Abra o terminal
2. Execute o comando:

```bash
pip install my-test-ify
```

---

Desenvolvido com muito café e curiosidade! ☕😄
