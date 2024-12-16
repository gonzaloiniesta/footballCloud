
class DataTransformer:
    
    def __init__(self):
        self.transformations = {
            'team': {
                'Ataques': self._transform_team_attack,
                'Disciplina': self._transform_team_discipline,
                'Clasico': self._transform_team_classic,
                'Defensiva': self._transform_team_defensive,
                'Eficiencia': self._transform_team_efficiency,
            },
            'tlayer': {
                'Ataques': self._transform_player_attack,
                'Disciplina': self._transform_player_discipline,
                'Clasico': self._transform_player_classic,
                'Defensiva': self._transform_player_defensive,
                'Eficiencia': self._transform_player_efficiency,
            }
        }

    def transform(self, k: dict, v: dict):
        """Transform the Kafka data based on the key (k) and the data (v)."""
        data_type = k.get('team', k.get('player'))
        category = k.get('stats')
        
        if not data_type or not category:
            raise ValueError("Invalid key format. 'team' or 'player' and 'stats' are required.")

        if 'team' in k:
            data_type = 'team'
        elif 'player' in k:
            data_type = 'player'
        else:
            raise ValueError("Key must contain 'team' or 'player'.")

        if data_type in self.transformations and category in self.transformations[data_type]:
            return self.transformations[data_type][category](v)
        else:
            raise ValueError(f"No transformation available for type '{data_type}' and category '{category}'")


    def _transform_team_attack(self, data: dict):
        return {
            'nombre': data.get('NOMBRE', '').title(),
            'equipo': data.get('EQUIPO', '').title(),
            'tiros': data.get('T', '0'),
            'disparos_a_puerto': data.get('DAP', '0'),
            'asistencias': data.get('ASI', '0'),
            'regates_con_exito': data.get('RE', '0'),
            'regates_fallidos': data.get('RF', '0'),
            'goles': data.get('G', '0'),
            'goles_desde_dentro_area': data.get('GDDA', '0'),
            'goles_desde_fuera_area': data.get('GFDA', '0'),
            'goles_pierna_izq': data.get('GCPI', '0.00'),
            'goles_pierna_der': data.get('GCPD', '0.00'),
            'goles_penalti': data.get('GDP', '0'),
            'goles_cabeza': data.get('CG', '0.00'),
            'goles_balon_parado': data.get('GBP', '0'),
            'goles_propia_puerta': data.get('GPP', '0'),
        }

    def _transform_team_discipline(self, data: dict):
        return {
            'equipo': data.get('EQUIPO', '').title(),
            'tarjetas_amarillas': data.get('TA', '0'),
            'tarjetas_rojas': data.get('TR', '0'),
            'segundas_amarillas': data.get('SA', '0'),
            'fueras_de_juego': data.get('FDJ', '0'),
            'faltas_recibidas': data.get('FR', '0'),
            'faltas_cometidas': data.get('FC', '0'),
            'penaltis_recibidos': data.get('PR', '0'),
            'penaltis_cometidos': data.get('PCOM', '0'),
            'manos': data.get('FPM', '0'),
            'faltas_por_tarjeta': data.get('FPT', '0.00'),
        }
    def _transform_team_classic(self, data: dict):
        return {
            'EQUIPO': data.get('EQUIPO', '').title(),
            'partidos_ganados': data.get('PG', '0'),
            'partidos_perdidos': data.get('PP', '0'),
            'partidos_empatados': data.get('PE', '0'),
            'tarjetas_amarillas': data.get('TA', '0'),
            'tarjetas_rojas': data.get('TR', '0'),
            'segundas_amarillas': data.get('SA', '0'),
            'goles_a_favor': data.get('G', '0'),
            'penaltis_recibidos': data.get('PR', '0'),
            'goles_propia_puerta': data.get('GPP', '0'),
            'goles_en_contra': data.get('GE', '0'),
        }

    def _transform_team_defensive(self, data: dict):
        return {
            'equipo': data.get('EQUIPO', '').title(),
            'bloqueos': data.get('BLOQ', '0'),
            'intercepciones': data.get('INTER', '0'),
            'recuperaciones': data.get('R', '0'),
            'despejes': data.get('D', '0'),
            'entradas_con_exito': data.get('EE', '0'),
            'entradas_fallidas': data.get('EF', '0'),
            'jugadas_como_ultimo_hombre': data.get('JUH', '0'),
            'duelos_con_exitos': data.get('DE', '0'),
            'duelos_fallidos': data.get('DF', '0'),
            'duelos_aereos_con_exito': data.get('DAE', '0'),
            'duelos_aereos_fallidos': data.get('DAF', '0'),
        }

    def _transform_team_efficiency(self, data: dict):
        return {
            'equipo': data.get('EQUIPO', '').title(),
            'corners_lanzados': data.get('C L', '0'),
            'entradas': data.get('ENT', '0'),
            'duelos': data.get('DUE', '0'),
            'duelos_cuerpo_a_cuerpo': data.get('D', '0'),
            'duelos_aereos': data.get('DA', '0'),
            'pases': data.get('PC', '0'),
            'pases_cortos': data.get('PCC', '0'),
            'pases_largos': data.get('PLC', '0'),
            'pases_al_hueco': data.get('PH', '0'),
            'goles_por_tiro': data.get('GPT', '0.00'),
            'goles_por_tiro_fuera_del_area': data.get('GPTFA', '0.00'),
            'goles_por_tiro_dentro_del_area': data.get('GPTDA', '0.00'),
            'goles_con_la_pierna_izq': data.get('GCPI', '0.00'),
            'goles_con_la_pierna_der': data.get('GCPD', '0.00'),
            'goles_de_cabeza': data.get('CG', '0.00'),
            'goles_balon_parado': data.get('GABP', '0.00'),
        }

    def _transform_player_attack(self, data: dict):
        return {
            'nombre': data.get('NOMBRE', '').title(),
            'equipo': data.get('EQUIPO', '').title(),
            'tiros': data.get('T', '0'),
            'disparos_a_puerto': data.get('DAP', '0'),
            'asistencias': data.get('ASI', '0'),
            'regates_con_exito': data.get('RE', '0'),
            'regates_fallidos': data.get('RF', '0'),
            'goles': data.get('G', '0'),
            'goles_desde_dentro_area': data.get('GDDA', '0'),
            'goles_desde_fuera_area': data.get('GFDA', '0'),
            'goles_pierna_izq': data.get('GCPI', '0.00'),
            'goles_pierna_der': data.get('GCPD', '0.00'),
            'goles_penalti': data.get('GDP', '0'),
            'goles_cabeza': data.get('CG', '0.00'),
            'goles_balon_parado': data.get('GBP', '0'),
            'goles_propia_puerta': data.get('GPP', '0'),
        }

    def _transform_player_discipline(self, data: dict):
        return {
            'nombre': data.get('NOMBRE', '').title(),
            'equipo': data.get('EQUIPO', '').title(),
            'tarjetas_amarillas': data.get('TA', '0'),
            'tarjetas_rojas': data.get('TR', '0'),
            'segundas_amarillas': data.get('SA', '0'),
            'fueras_de_juego': data.get('FDJ', '0'),
            'faltas_recibidas': data.get('FR', '0'),
            'faltas_cometidas': data.get('FC', '0'),
            'penaltis_recibidos': data.get('PR', '0'),
            'penaltis_cometidos': data.get('PCOM', '0'),
            'manos': data.get('FPM', '0'),
            'faltas_por_tarjeta': data.get('FPT', '0.00'),
        }

    def _transform_player_classic(self, data: dict):
        return {
            'nombre': data.get('NOMBRE', '').title(),
            'equipo': data.get('EQUIPO', '').title(),
            'minutos_jugados': data.get('MJ', '0'),
            'partidos_jugados': data.get('PJ', '0'),
            'partidos_completos': data.get('PC', '0'),
            'partidos_titular': data.get('PT', '0'),
            'partidos_sustituidos': data.get('PS', '0'),
            'tarjetas_amarillas': data.get('TA', '0'),
            'tarjetas_rojas': data.get('TR', '0'),
            'segundas_amarillas': data.get('SA', '0'),
            'goles': data.get('G', '0'),
            'penaltis_recibidos': data.get('PR', '0'),
            'goles_propia_puerta': data.get('GPP', '0'),
            'goles_en_contra': data.get('GE', '0'),
        }

    def _transform_player_defensive(self, data: dict):
        return {
            'nombre': data.get('NOMBRE', '').title(),
            'equipo': data.get('EQUIPO', '').title(),
            'bloqueos': data.get('BLOQ', '0'),
            'intercepciones': data.get('INTER', '0'),
            'recuperaciones': data.get('R', '0'),
            'despejes': data.get('D', '0'),
            'entradas_con_exito': data.get('EE', '0'),
            'entradas_fallidas': data.get('EF', '0'),
            'jugadas_como_ultimo_hombre': data.get('JUH', '0'),
            'duelos_con_exitos': data.get('DE', '0'),
            'duelos_fallidos': data.get('DF', '0'),
            'duelos_aereos_con_exito': data.get('DAE', '0'),
            'duelos_aereos_fallidos': data.get('DAF', '0'),
        }

    def _transform_player_efficiency(self, data: dict):
        return {
            'nombre': data.get('NOMBRE', '').title(),
            'equipo': data.get('EQUIPO', '').title(),
            'corners_lanzados': data.get('C L', '0'),
            'entradas': data.get('ENT', '0'),
            'duelos': data.get('DUE', '0'),
            'duelos_cuerpo_a_cuerpo': data.get('D', '0'),
            'duelos_aereos': data.get('DA', '0'),
            'pases': data.get('PC', '0'),
            'pases_cortos': data.get('PCC', '0'),
            'pases_largos': data.get('PLC', '0'),
            'pases_al_hueco': data.get('PH', '0'),
            'goles_por_tiro': data.get('GPT', '0.00'),
            'goles_por_tiro_fuera_del_area': data.get('GPTFA', '0.00'),
            'goles_por_tiro_dentro_del_area': data.get('GPTDA', '0.00'),
            'goles_con_la_pierna_izq': data.get('GCPI', '0.00'),
            'goles_con_la_pierna_der': data.get('GCPD', '0.00'),
            'goles_de_cabeza': data.get('CG', '0.00'),
            'goles_balon_parado': data.get('GABP', '0.00'),
        }
