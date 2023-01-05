import numpy as np
import skfuzzy as fuzz 
from skfuzzy import control as ctrl

#Antecedente: entrada para um sistema
#Consequente: saida do sistema

sujeira = ctrl.Antecedent(np.arange(0,100,1),'sujeira')
#Declara a entrada do preco indo de 40000 ate 100000, o 1 representa o passo e por fim declara o rotulo no caso o "preco"

qualidade_sujeira = ctrl.Antecedent(np.arange(0,100,1),'qualidade_sujeira')
#Declara a entrada do consumo indo de 11 ate 18, o 1 representa o passo e por fim declara o rotulo no caso o "consumo"

tempo_de_lavar=ctrl.Consequent(np.arange(0,1,0.1), 'tempo_de_lavar')
#Declarar a saida do beneficio indo de 0 a 11, tendo 0.5 como passo

sujeira.automf(number=3, names=['gorduroso','medio','sem gordura'])
#Insere os nomes dos níveis dependendo dos valores

qualidade_sujeira.automf(number=3, names=['baixo','medio','alto'])

sujeira.view()
#Mostrar o grafico em relacao ao preco
qualidade_sujeira.view()
#Mostrar o grafico em relacao ao consumo

#Definir as classificacoes dos niveis
tempo_de_lavar['muito curto'] = fuzz.trimf(tempo_de_lavar.universe, [0, 0.1, 0.2])
#Sera baixo, ao começar com 0 até o ponto médio 2.5 e vai por fim no 5
tempo_de_lavar['curto'] = fuzz.trimf(tempo_de_lavar.universe, [0.2, 0.3, 0.4])
tempo_de_lavar['medio'] = fuzz.trimf(tempo_de_lavar.universe, [0.4, 0.5, 0.6])
tempo_de_lavar['longo'] = fuzz.trimf(tempo_de_lavar.universe, [0.6, 0.7, 0.8])
tempo_de_lavar['muito longo'] = fuzz.trimf(tempo_de_lavar.universe, [0.8, 0.9, 1.0])

tempo_de_lavar.view()

regra1 = ctrl.Rule(qualidade_sujeira['baixo'] and sujeira['gorduroso'], tempo_de_lavar['longo'])
#Na regra 1, caso o preco for baixo OU consumo baixo seu beneficio vai ser alto
regra2 = ctrl.Rule(qualidade_sujeira['medio'] and sujeira['gorduroso'], tempo_de_lavar['longo'])
regra3 = ctrl.Rule(qualidade_sujeira['alto'] and sujeira['gorduroso'], tempo_de_lavar['muito longo'])
regra4 = ctrl.Rule(qualidade_sujeira['baixo'] and sujeira['medio'], tempo_de_lavar['medio'])
regra5 = ctrl.Rule(qualidade_sujeira['medio'] and sujeira['medio'], tempo_de_lavar['medio'])
regra6 = ctrl.Rule(qualidade_sujeira['alto'] and sujeira['medio'], tempo_de_lavar['medio'])
regra7 = ctrl.Rule(qualidade_sujeira['baixo'] and sujeira['sem gordura'], tempo_de_lavar['muito curto'])
regra8 = ctrl.Rule(qualidade_sujeira['medio'] and sujeira['sem gordura'], tempo_de_lavar['medio'])
regra9 = ctrl.Rule(qualidade_sujeira['alto'] and sujeira['gorduroso'], tempo_de_lavar['muito curto'])

recomendacao_tempo = ctrl.ControlSystem([regra1, regra2, regra3, regra4,
                                          regra5, regra6, regra7, regra8,
                                          regra9])
#Vai simular uma execução do programa usando as regras que foram inseridas anteriormente
recomendacao=ctrl.ControlSystemSimulation(recomendacao_tempo)

recomendacao.input['sujeira']=50
recomendacao.input['qualidade_sujeira'] = 25
recomendacao.compute()

print(recomendacao.output['tempo_de_lavar'])
tempo_de_lavar.view(sim=recomendacao)
