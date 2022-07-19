# Contexto
O sistema X é um software para RH de grandes empresas com as seguintes características:
- Multi-tenant (mesmo software e infra para todos os clientes)
- Autenticação via JWT
~~~javascript
{
    user_id: string;  ==> employee.id
    company_id: string; ===> employee.company_id
    role: string;
}
~~~

- Banco de dados PostgreSQL
  - Tabelas
    - employee(id, name, manager_id, company_id)
      - manager_id -> employee.id
    - documents(id, type, file, employee_id, company_id)
    - hierarchy(id, manager_id, employee_id)

- APIs REST em Flask/Python

# O Problema
Supondo um usuário que é gestor na empresa, precisamos desenvolver uma API que lista os documentos dos funcionários subordinados a ele. Lembrando que a hierarquia é multinível, então:

- Jorge é um diretor
  - employee (1, Jorge, null)
- Maria é uma gerente, subordinada ao Jorge
  - employee(2, Maria, 1)
- Luiz é um analista, subordinado à Maria
  - employee(3, Luiz, 2)

> Jorge precisa ser capaz de ver os documentos de Maria e Luiz

> Maria precisa ver os documentos de Luiz

# Solução
Proponha uma solução para esse problema, sem desenvolver código, mas com detalhes de como poderia ser feita a implementação.
Por exemplo, se for o caso, detalhe:
- Alterações no banco de dados, se necessário
- Alterações no modelo de autenticação, se necessário
- O que a API precisaria fazer

> Tenha em mente que é um software multi-tenant, então leve em consideração o impacto da proposta em performance

> Você pode sugerir mais de uma abordagem para ser discutida

## Leve em conta
- Segurança (o frontend não pode ser capaz de dar bypass nessa restrição, por exemplo)
- Performance (uma empresa pode ter milhares de funcionários e documentos)
- Tempo de execucao

# Avaliação
Não é necessário escrever código. A avaliação do case será simulando uma reunião de Grooming entre o time, para decidir a estratégia de desenvolvimento da API. Mas é recomendado levar anotações que ajudem a transmitir a sua idéia durante a call com o time. Elas podem estar num markdown, um doc ou até slides. Quanto mais próximo da realidade do dia a dia, melhor.
