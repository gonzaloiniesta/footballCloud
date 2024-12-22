
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
            'player': {
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

    # Team Transformations
    def _transform_team_attack(self, data: dict):
        return {
            'name': data.get('NOMBRE', '').title(),
            'team': data.get('EQUIPO', '').title(),
            'shots': int(data.get('T', '0')),
            'shots_on_target': int(data.get('DAP', '0')),
            'assists': int(data.get('ASI', '0')),
            'successful_dribbles': int(data.get('RE', '0')),
            'failed_dribbles': int(data.get('RF', '0')),
            'goals': int(data.get('G', '0')),
            'goals_inside_box': int(data.get('GDDA', '0')),
            'goals_outside_box': int(data.get('GFDA', '0')),
            'left_foot_goals': float(data.get('GCPI', '0.00')),
            'right_foot_goals': float(data.get('GCPD', '0.00')),
            'penalty_goals': int(data.get('GDP', '0')),
            'header_goals': float(data.get('CG', '0.00')),
            'set_piece_goals': int(data.get('GBP', '0')),
            'own_goals': int(data.get('GPP', '0')),
        }

    def _transform_team_discipline(self, data: dict):
        return {
            'team': data.get('EQUIPO', '').title(),
            'yellow_cards': int(data.get('TA', '0')),
            'red_cards': int(data.get('TR', '0')),
            'second_yellows': int(data.get('SA', '0')),
            'offsides': int(data.get('FDJ', '0')),
            'fouls_suffered': int(data.get('FR', '0')),
            'fouls_committed': int(data.get('FC', '0')),
            'penalties_won': int(data.get('PR', '0')),
            'penalties_committed': int(data.get('PCOM', '0')),
            'handballs': int(data.get('FPM', '0')),
            'fouls_per_card': float(data.get('FPT', '0.00')),
        }

    def _transform_team_classic(self, data: dict):
        return {
            'team': data.get('EQUIPO', '').title(),
            'matches_won': int(data.get('PG', '0')),
            'matches_lost': int(data.get('PP', '0')),
            'matches_drawn': int(data.get('PE', '0')),
            'yellow_cards': int(data.get('TA', '0')),
            'red_cards': int(data.get('TR', '0')),
            'second_yellows': int(data.get('SA', '0')),
            'goals_scored': int(data.get('G', '0')),
            'penalties_won': int(data.get('PR', '0')),
            'own_goals': int(data.get('GPP', '0')),
            'goals_conceded': int(data.get('GE', '0')),
        }

    def _transform_team_defensive(self, data: dict):
        return {
            'team': data.get('EQUIPO', '').title(),
            'blocks': int(data.get('BLOQ', '0')),
            'interceptions': int(data.get('INTER', '0')),
            'recoveries': int(data.get('R', '0')),
            'clearances': int(data.get('D', '0')),
            'successful_tackles': int(data.get('EE', '0')),
            'failed_tackles': int(data.get('EF', '0')),
            'last_man_tackles': int(data.get('JUH', '0')),
            'successful_duels': int(data.get('DE', '0')),
            'failed_duels': int(data.get('DF', '0')),
            'successful_aerial_duels': int(data.get('DAE', '0')),
            'failed_aerial_duels': int(data.get('DAF', '0')),
        }

    def _transform_team_efficiency(self, data: dict):
        return {
            'team': data.get('EQUIPO', '').title(),
            'corners_taken': int(data.get('C L', '0')),
            'tackles': int(data.get('ENT', '0')),
            'duels': int(data.get('DUE', '0')),
            'body_duels': int(data.get('D', '0')),
            'aerial_duels': int(data.get('DA', '0')),
            'passes': int(data.get('PC', '0')),
            'short_passes': int(data.get('PCC', '0')),
            'long_passes': int(data.get('PLC', '0')),
            'through_passes': int(data.get('PH', '0')),
            'goals_per_shot': float(data.get('GPT', '0.00')),
            'goals_per_shot_outside_box': float(data.get('GPTFA', '0.00')),
            'goals_per_shot_inside_box': float(data.get('GPTDA', '0.00')),
            'left_foot_goals': float(data.get('GCPI', '0.00')),
            'right_foot_goals': float(data.get('GCPD', '0.00')),
            'header_goals': float(data.get('CG', '0.00')),
            'set_piece_goals': float(data.get('GABP', '0.00')),
        }

    # Player Transformations
    def _transform_player_attack(self, data: dict):
        return {
            'name': data.get('NOMBRE', '').title(),
            'team': data.get('EQUIPO', '').title(),
            'shots': int(data.get('T', '0')),
            'shots_on_target': int(data.get('DAP', '0')),
            'assists': int(data.get('ASI', '0')),
            'successful_dribbles': int(data.get('RE', '0')),
            'failed_dribbles': int(data.get('RF', '0')),
            'goals': int(data.get('G', '0')),
            'goals_inside_box': int(data.get('GDDA', '0')),
            'goals_outside_box': int(data.get('GFDA', '0')),
            'left_foot_goals': float(data.get('GCPI', '0.00')),
            'right_foot_goals': float(data.get('GCPD', '0.00')),
            'penalty_goals': int(data.get('GDP', '0')),
            'header_goals': float(data.get('CG', '0.00')),
            'set_piece_goals': float(data.get('GBP', '0.00')),
            'own_goals': int(data.get('GPP', '0')),
        }

    def _transform_player_discipline(self, data: dict):
        return {
            'name': data.get('NOMBRE', '').title(),
            'team': data.get('EQUIPO', '').title(),
            'yellow_cards': int(data.get('TA', '0')),
            'red_cards': int(data.get('TR', '0')),
            'second_yellows': int(data.get('SA', '0')),
            'offsides': int(data.get('FDJ', '0')),
            'fouls_suffered': int(data.get('FR', '0')),
            'fouls_committed': int(data.get('FC', '0')),
            'penalties_won': int(data.get('PR', '0')),
            'penalties_committed': int(data.get('PCOM', '0')),
            'handballs': int(data.get('FPM', '0')),
            'fouls_per_card': float(data.get('FPT', '0.00')),
        }

    def _transform_player_classic(self, data: dict):
        return {
            'name': data.get('NOMBRE', '').title(),
            'team': data.get('EQUIPO', '').title(),
            'minutes_played': int(data.get('MJ', '0')),
            'matches_played': int(data.get('PJ', '0')),
            'complete_matches': int(data.get('PC', '0')),
            'starting_matches': int(data.get('PT', '0')),
            'substituted_matches': int(data.get('PS', '0')),
            'goals': int(data.get('G', '0')),
            'penalties_won': int(data.get('PR', '0')),
            'own_goals': int(data.get('GPP', '0')),
            'goals_conceded': int(data.get('GE', '0')),
        }

    def _transform_player_defensive(self, data: dict):
        return {
            'name': data.get('NOMBRE', '').title(),
            'team': data.get('EQUIPO', '').title(),
            'blocks': int(data.get('BLOQ', '0')),
            'interceptions': int(data.get('INTER', '0')),
            'recoveries': int(data.get('R', '0')),
            'clearances': int(data.get('D', '0')),
            'successful_tackles': int(data.get('EE', '0')),
            'failed_tackles': int(data.get('EF', '0')),
            'last_man_tackles': int(data.get('JUH', '0')),
            'successful_duels': int(data.get('DE', '0')),
            'failed_duels': int(data.get('DF', '0')),
            'successful_aerial_duels': int(data.get('DAE', '0')),
            'failed_aerial_duels': int(data.get('DAF', '0')),
        }

    def _transform_player_efficiency(self, data: dict):
        return {
            'name': data.get('NOMBRE', '').title(),
            'team': data.get('EQUIPO', '').title(),
            'corners_taken': int(data.get('C L', '0')),
            'tackles': int(data.get('ENT', '0')),
            'duels': int(data.get('DUE', '0')),
            'body_duels': int(data.get('D', '0')),
            'aerial_duels': int(data.get('DA', '0')),
            'passes': int(data.get('PC', '0')),
            'short_passes': int(data.get('PCC', '0')),
            'long_passes': int(data.get('PLC', '0')),
            'through_passes': int(data.get('PH', '0')),
            'goals_per_shot': float(data.get('GPT', '0.00')),
            'goals_per_shot_outside_box': float(data.get('GPTFA', '0.00')),
            'goals_per_shot_inside_box': float(data.get('GPTDA', '0.00')),
            'left_foot_goals': float(data.get('GCPI', '0.00')),
            'right_foot_goals': float(data.get('GCPD', '0.00')),
            'header_goals': float(data.get('CG', '0.00')),
            'set_piece_goals': float(data.get('GABP', '0.00')),
        }
