# Reflexão sobre o uso de IA no CoronaFlux

## Como usamos a IA

Usamos o Claude durante o desenvolvimento do CoronaFlux para entender a API, organizar as etapas e produzir boa parte do código do projeto. A ajuda incluiu o banco de dados, o script de coleta, o workflow do GitHub Actions, o painel e as correções que surgiram nos testes. Também usamos suas explicações para entender melhor os dados que seriam apresentados.

Lorenzo ficou responsável pela maior parte dos componentes técnicos e pela integração dessas partes. Vitor e Cauan acompanharam o desenvolvimento, deram sugestões e ficaram responsáveis pela documentação e pela apresentação. As decisões sobre o que acrescentar ao painel foram discutidas pelo grupo.

## Onde a IA ajudou

A IA ajudou a transformar a proposta da atividade em uma sequência de trabalho. Ficou mais fácil entender por que era preciso preparar o banco antes de testar a coleta completa e por que o painel deveria ler os dados do Supabase, em vez de consultar a NASA a cada acesso.

Outro apoio foi na compreensão dos dados. No começo, não estava tão claro para nós o que a IPS fornecia e o que precisaria vir de outras fontes. Com as explicações, conseguimos separar os registros de choques das informações complementares de CME, GST e Horizons. Essas fontes permitiram acrescentar velocidades, Kp e posições ao painel.

Na implementação, a geração de código adiantou bastante o trabalho. A IA também propôs recursos que aproveitavam os dados já coletados, como o histórico do pipeline, a ligação entre detecções da mesma CME e a exportação CSV. O grupo avaliou essas sugestões e escolheu incluí-las.

## Onde a IA errou e o que foi ajustado

Um dos erros mais claros foi o intervalo usado na coleta histórica. A primeira versão dividia as consultas da IPS em janelas de 180 dias, mas a API aceitava no máximo 60 dias. A execução gravou alguns eventos e terminou com erro parcial. A partir do retorno da execução real, o problema foi identificado e a IA gerou a correção das janelas. Também foi preciso informar a data inicial para repetir o histórico, porque o banco já tinha alguns registros.

Outro problema foi o gráfico de Kp, que ficou vazio. O script procurava uma propriedade chamada allKpValues, enquanto a resposta real da GST usava allKpIndex. Como o programa interpretava isso como ausência de dados, a execução podia terminar sem acusar esse erro. A correção foi feita na leitura do campo, e a orientação foi executar novamente a carga para preencher os registros antigos.

Esse caso chamou nossa atenção porque os testes simulados não encontraram o problema. Os exemplos de teste usavam o mesmo nome de campo errado do código. Isso mostrou que testar apenas com dados preparados pela própria IA pode confirmar uma suposição incorreta. Foi necessário comparar com a resposta real da API.

Também houve um erro de configuração do nosso lado: uma chave incorreta foi usada no teste da NASA. A orientação da IA ajudou a conferir a chave antes de mudar outras partes do programa. No painel, apareceram problemas de rolagem lateral e sobreposição no celular, que levaram a novos ajustes no layout.

## O que aprendemos

Aprendemos que uma resposta detalhada da IA não garante que o código esteja correto. Os limites das APIs, os nomes dos campos e as permissões precisam ser conferidos no serviço real. Uma execução verde também não significa, por si só, que todos os dados esperados foram preenchidos.

Percebemos ainda que precisamos entender as escolhas feitas no código. Por exemplo, selecionar a CME mais rápida entre as associadas é um critério do projeto. A velocidade média e algumas posições são estimativas. Essas informações precisam ser explicadas na apresentação para que o painel não passe uma ideia de precisão maior do que realmente oferece.

A divisão das tarefas também influenciou nossa experiência. Como Lorenzo concentrou a parte técnica, Vitor e Cauan precisaram acompanhar as explicações e organizar o conteúdo para conseguir documentar e apresentar o funcionamento. A participação de cada integrante foi diferente, mas todos precisaram compreender a relação entre coleta, banco e painel.

## Conclusão

A IA tornou o desenvolvimento mais rápido e ajudou bastante quando encontramos dificuldades. Ao mesmo tempo, os erros nas janelas de consulta e no Kp mostraram que não dava para aceitar tudo sem conferir. O trabalho exigiu configurações, testes, decisões e acompanhamento do grupo.

Para nós, o principal aprendizado foi usar a IA com mais atenção ao resultado real. Além de obter um código que roda, precisamos verificar os dados, entender os critérios e conseguir explicar o que foi construído.

