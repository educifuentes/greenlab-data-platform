| Variable                    | Descripción                                                       | Unidad                       | Lógica de construcción                                         |
| :-------------------------- | :---------------------------------------------------------------- | :--------------------------- | :------------------------------------------------------------- |
| NombreCentral               | Nombre de la central termoeléctrica                               | -                            | Identificador original del CEMS                                |
| Chimenea                    | Nombre de la chimenea asociada a la UGE                           | -                            | Identificador original del CEMS                                |
| UGE                         | Unidad Generadora Eléctrica                                       | -                            | Identificador original del CEMS                                |
| DIA                         | Fecha (agregación diaria)                                         | Fecha (yyyy-mm-dd)           | Derivado de FECHA (sin hora)                                   |
| n_registros_dia             | Número de registros horarios existentes ese día                   | Número entero                | Conteo de filas por UGE y día                                  |
| horas_operativas            | Número de horas con generación positiva                           | Número entero                | Suma de horas donde MWh > 0                                    |
| MWh_dia                     | Energía bruta generada en el día                                  | MWh                          | Suma de POTENCIA_BRUTA_MWH horaria                             |
| MWh_prom_por_hora_operativa | Carga promedio durante horas operativas                           | MWh/h                        | MWh_dia / horas_operativas                                     |
| Flujo_Nm3_dia               | Volumen total diario de gases (base seca normalizada)             | Nm3                          | Suma de FLUJO_GASES_SALIDA_NM3_H                               |
| Consumo_combustible_dia     | Consumo total diario de combustible                               | m3 o ton (según combustible) | Suma de CONSUMO_COMBUSTIBLE                                    |
| NOX_mg_dia_from_mgMWh       | Masa total diaria de NOX calculada desde intensidad mg/MWh        | mg                           | Suma de (CONCENTRACION_NOX_MG_MWH \* MWh)                      |
| SO2_mg_dia_from_mgMWh       | Masa total diaria de SO2 calculada desde intensidad mg/MWh        | mg                           | Suma de (CONCENTRACION_SO2_MG_MWH \* MWh)                      |
| MP_mg_dia_from_mgMWh        | Masa total diaria de MP calculada desde intensidad mg/MWh         | mg                           | Suma de (CONCENTRACION_MP_MG_MWH \* MWh)                       |
| NOX_kg_dia_from_mgMWh       | Masa total diaria de NOX desde intensidad energética              | kg                           | NOX_mg_dia_from_mgMWh / 1e6                                    |
| SO2_kg_dia_from_mgMWh       | Masa total diaria de SO2 desde intensidad energética              | kg                           | SO2_mg_dia_from_mgMWh / 1e6                                    |
| MP_kg_dia_from_mgMWh        | Masa total diaria de MP desde intensidad energética               | kg                           | MP_mg_dia_from_mgMWh / 1e6                                     |
| CO2_ton_dia_from_tonMWh     | Masa total diaria de CO2 desde intensidad energética              | ton                          | Suma de (CONCENTRACION_CO2_TON_MWH \* MWh)                     |
| NOX_mg_dia_from_mgNm3       | Masa total diaria de NOX calculada desde concentración física     | mg                           | Suma de (CONCENTRACION_NOX_MG_NM3 \* FLUJO_GASES_SALIDA_NM3_H) |
| SO2_mg_dia_from_mgNm3       | Masa total diaria de SO2 calculada desde concentración física     | mg                           | Suma de (CONCENTRACION_SO2_MG_NM3 \* FLUJO_GASES_SALIDA_NM3_H) |
| MP_mg_dia_from_mgNm3        | Masa total diaria de MP calculada desde concentración física      | mg                           | Suma de (CONCENTRACION_MP_MG_NM3 \* FLUJO_GASES_SALIDA_NM3_H)  |
| NOX_kg_dia_from_mgNm3       | Masa total diaria de NOX desde concentración física               | kg                           | NOX_mg_dia_from_mgNm3 / 1e6                                    |
| SO2_kg_dia_from_mgNm3       | Masa total diaria de SO2 desde concentración física               | kg                           | SO2_mg_dia_from_mgNm3 / 1e6                                    |
| MP_kg_dia_from_mgNm3        | Masa total diaria de MP desde concentración física                | kg                           | MP_mg_dia_from_mgNm3 / 1e6                                     |
| NOX_mg_MWh_dia              | Intensidad diaria de NOX por energía                              | mg/MWh                       | NOX_mg_dia_from_mgMWh / MWh_dia                                |
| SO2_mg_MWh_dia              | Intensidad diaria de SO2 por energía                              | mg/MWh                       | SO2_mg_dia_from_mgMWh / MWh_dia                                |
| MP_mg_MWh_dia               | Intensidad diaria de MP por energía                               | mg/MWh                       | MP_mg_dia_from_mgMWh / MWh_dia                                 |
| CO2_ton_MWh_dia             | Intensidad diaria de CO2 por energía                              | ton/MWh                      | CO2_ton_dia_from_tonMWh / MWh_dia                              |
| NOX_mg_Nm3_prom_dia         | Concentración promedio diaria de NOX (ponderada por flujo)        | mg/Nm3                       | Promedio ponderado por FLUJO_GASES_SALIDA_NM3_H                |
| SO2_mg_Nm3_prom_dia         | Concentración promedio diaria de SO2 (ponderada por flujo)        | mg/Nm3                       | Promedio ponderado por FLUJO_GASES_SALIDA_NM3_H                |
| MP_mg_Nm3_prom_dia          | Concentración promedio diaria de MP (ponderada por flujo)         | mg/Nm3                       | Promedio ponderado por FLUJO_GASES_SALIDA_NM3_H                |
| NOX_ppm_prom_dia            | Concentración promedio diaria de NOX en ppm (ponderada por flujo) | ppm                          | Promedio ponderado por FLUJO_GASES_SALIDA_NM3_H                |
| SO2_ppm_prom_dia            | Concentración promedio diaria de SO2 en ppm (ponderada por flujo) | ppm                          | Promedio ponderado por FLUJO_GASES_SALIDA_NM3_H                |
| O2_prom_MWh                 | O2 promedio diario ponderado por generación                       | % base seca                  | Promedio ponderado por MWh                                     |
| Humedad_prom_MWh            | Humedad promedio diaria ponderada por generación                  | %                            | Promedio ponderado por MWh                                     |
| Temp_gases_prom_MWh         | Temperatura promedio diaria de gases ponderada por generación     | °C                           | Promedio ponderado por MWh                                     |
| Presion_prom_MWh            | Presión promedio diaria ponderada por generación                  | atm                          | Promedio ponderado por MWh                                     |
| ESTADO_UGE_mas_frecuente    | Estado operativo más frecuente del día                            | -                            | Moda del campo ESTADO_UGE                                      |
| COMBUSTIBLE_mas_frecuente   | Combustible más utilizado en el día                               | -                            | Moda del campo COMBUSTIBLE                                     |
