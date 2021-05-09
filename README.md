# trader_ccxt

En este algoritmo se usara el calculo de probabilidades
y se coorelacionara los datos obtenidos de los observadores 
para refinar la precision y aumentar el porcentaje de ganancia por trade
asi como reducir el riesgo por compra.

Calculo de probabilidades: Estimacion de porcentajes de perdida y ganancia, 
estimacion del rango de accion de compra y venta (5 - 10%) variable, calculo 
de velocidades de venta estimada. Todo esto en vivo.

Coorelacion de datos de observadores: Se dispondran 2 observadores externos
y un tercero enfocado en las probabilidades mas altas y mejor desempenho. 
Estos datos de coorelacionaran y filtraran para automatizar la tarea de 
elegir los activos que mas dinamismo y amplitud de subida y bajada tienen

El Trader se encargara de comprar y vender con la aprobacion de las 
estimaciones del observador y el corrector

El corrector se encargara de buscar las probabilidades mas arriesgadas y 
declarar alertas enviadas por telegram al usuario, asi como darle al ejecutor
los datos de estas alertas para poder detener alguna compra o venta. 
En su defecto agregar o quitar caracteristicas de la comprao venta


