# BOP

Mesmo não se tendo
pensado em nenhum significado antes da escolha do nome, **BOP**, foi escolhido
manter ele como trocadilho. Alem disso, ele é fácil escrever porque tem três
letras e é de fácil pronúncia.

## Estrutura de Diretorios

* ExpertsBO: Contém uma lista de diretorios com os nomes dos mesmo sendo o
             do principal indicador que aquele sistema usa. Sistemas com
             multiplos indicadores irao no sub-diretorio complexos.
* Includes: Contém arquivos que os expert advisors podem incluir.
* Logs: Resultados das execuções realizadas dos advisor em CSV. O periodo
        da analise é sempre de Janeiro/1980 ate Setembro/2017 e os advisor
        executam sempre em M1.

### Como instalar no meta trader 4?

Simplesmente, mova os arquivos em Includes para a pasta Include no diretorio
MQL4 e a pasta do ExpertsBO mova-a para a pasta de Experts no MQL4.

Cabe salientar que os experts advisors sendo disponibilizados não constituem
em hipotese alguma recomendação de investimento. A única pessoa responsável
pelo que é seu é você.
