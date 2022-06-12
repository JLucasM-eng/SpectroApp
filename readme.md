# EspectroApp

## Introdução

O processamento e análise acústica da voz humana é uma atividade importante tanto para
a identificação de disfunções vocais quanto para realização de perícia trabalhista e criminal.
Nesse sentido, falta hoje para os profissionais um software intuitivo, com interface amigável
e com a apresentação de um espectrograma de boa qualidade para a análise visual. Nesse
sentido, este projeto propõe o desenvolvimento de um software acessível, de baixo custo, para
processamento e análise acústica de voz que utilize técnicas de processamento de sinais comuns
na engenharia biomédica tais como a transformada de Fourier. Temos, pois, uma aplicação capaz de
receber e gravar áudios para análise e apresentar como resultado principal um espectrograma para
auxiliar na análise acústica da voz, além da possibilidade de visualização do detector de pitch.
Os gráficos gerados possuem uma resolução satisfatória, podendo apresentar uma performance
ainda maior para áudios gravados em ambientes com poucos ou nenhum ruido. 

Avaliando algumas opções de linguagens e bibliotecas para desenvolvimento de software
tanto back-end e front-end, identificou-se no Python uma linguagem que oferece uma gama enorme de bibliotecas e funcionalidades voltadas para a área de tratamento de sinais. Além disso
optou-se por utilizar o Streamlit, que é um framework de código aberto que utiliza linguagem
Python. Este, além de ser gratuito e acessível é de fácil desenvolvimento e manutenção, uma vez
que foi criado justamente para ajudar cientistas de dados a colocarem em produção seus projetos
sem a necessidade de conhecer ferramentas de front-end ou de deploy de aplicações.

Para geração das visualizações, foi utilizado a biblioteca <a href="https://parselmouth.readthedocs.io/en/stable/">Parselmouth</a>. Essa biblioteca
baseia-se na base de código do famoso software Praat, que implementa uma variedade enorme
de algoritmos de processamento de fala e fonética. Muitas dessas funções podem ser acessadas
através do Parselmouth. Para isso, Parselmouth utiliza a biblioteca pybind11 , o que permite
expor a funcionalidade C/C++ do Praat como uma interface Python.

## Bibliotecas e pacotes necessários

No arquivo *requirements.txt* você encontrará todas as bibliotecas utilizadas nesta aplicação. Realize previamente a instalação destas bibliotecas, se possivel atentando-se também para a versão apresentada.

## Executando o projeto

Após o clone do projeto, a partir da pasta raiz da aplicação, execute o script python *app.py*, ou execute o seguinte comando no terminal: *python -u "caminhoParaProjeto\...\app.py".
O retorno deste comando será um comando *streamlit run*. Em seguida você deverá executar este comando apresentado no terminal.

Ao executar o *streamlit run "...\app.py"*, o Streamlit automaticamente irá executar o seu projeto em um servidor local e informar o endereço para acesso a nivel de desenvolvimento.

PS. Todos os prints ou comandos semelhantes poderam ser vistos pelo terminal onde está rodando o servidor Streamlit.

