import random

from repositories.player_repository import PlayerRepository
from repositories.team_repository import TeamRepository
from schemas.simulator import GroupStageResult, GroupStanding, MatchResult, SimulatorResponse
from schemas.simulator import MatchResult as MatchResultType
from services.simulation_cache import store as cache_store
from sqlalchemy.orm import Session


GROUP_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
TOURNAMENT_TEAM_COUNT = 48

WORLD_CUP_2026_TEAMS = [
    ("México", "MEX", "A"),
    ("Marruecos", "MAR", "A"),
    ("Corea del Sur", "KOR", "A"),
    ("Escocia", "SCO", "A"),
    ("Canadá", "CAN", "B"),
    ("Suiza", "SUI", "B"),
    ("Bosnia y Herzegovina", "BIH", "B"),
    ("Qatar", "QAT", "B"),
    ("Argentina", "ARG", "C"),
    ("Argelia", "ALG", "C"),
    ("Austria", "AUT", "C"),
    ("Haití", "HAI", "C"),
    ("Estados Unidos", "USA", "D"),
    ("Turquía", "TUR", "D"),
    ("Paraguay", "PAR", "D"),
    ("Australia", "AUS", "D"),
    ("Alemania", "GER", "E"),
    ("Ecuador", "ECU", "E"),
    ("Costa de Marfil", "CIV", "E"),
    ("Curazao", "CUW", "E"),
    ("Países Bajos", "NED", "F"),
    ("Japón", "JPN", "F"),
    ("Suecia", "SWE", "F"),
    ("Túnez", "TUN", "F"),
    ("Bélgica", "BEL", "G"),
    ("Egipto", "EGY", "G"),
    ("Irán", "IRN", "G"),
    ("Nueva Zelanda", "NZL", "G"),
    ("España", "ESP", "H"),
    ("Uruguay", "URU", "H"),
    ("Arabia Saudita", "KSA", "H"),
    ("Cabo Verde", "CPV", "H"),
    ("Francia", "FRA", "I"),
    ("Noruega", "NOR", "I"),
    ("Senegal", "SEN", "I"),
    ("Irak", "IRQ", "I"),
    ("Brasil", "BRA", "J"),
    ("Sudáfrica", "RSA", "J"),
    ("República Checa", "CZE", "J"),
    ("Jordania", "JOR", "J"),
    ("Portugal", "POR", "K"),
    ("Colombia", "COL", "K"),
    ("RD Congo", "COD", "K"),
    ("Uzbekistán", "UZB", "K"),
    ("Inglaterra", "ENG", "L"),
    ("Croacia", "CRO", "L"),
    ("Ghana", "GHA", "L"),
    ("Panamá", "PAN", "L"),
]

POSITIONS = ["GK", "DF", "MF", "FW"]
FIRST_NAMES = [
    "Liam", "Noah", "Oliver", "James", "Elijah", "Mateo", "Theo", "Henry",
    "Lucas", "Mason", "Ethan", "Logan", "Daniel", "Jack", "Gabriel", "Samuel",
    "David", "Leo", "Ezra", "Julian", "Aiden", "Tomas", "Santiago", "Bruno",
    "Juan", "Valentino", "Rafael", "Maximo", "Luciano", "Tadeo", "Simon", "Thiago",
]
POSITION_POOL = {
    "GK": ["Lopez", "Martinez", "Alvarez", "Di Stefano", "Zanetti", "Buffon", "Neuer", "Courtois"],
    "DF": ["Ramos", "Puyol", "Cafu", "Maldini", "Beckenbauer", "Moore", "Passarella", "Figueroa"],
    "MF": ["Maradona", "Zidane", "Iniesta", "Xavi", "Modric", "Pirlo", "Gerrard", "Zico"],
    "FW": ["Messi", "Ronaldo", "Neymar", "Mbappe", "Haaland", "Pele", "Cruyff", "Van Basten"],
}


class SimulatorService:
    def __init__(self, db: Session):
        self.team_repo = TeamRepository(db)
        self.player_repo = PlayerRepository(db)

    def _ensure_data(self):
        if self.team_repo.count() < TOURNAMENT_TEAM_COUNT:
            self._generate_world_cup_teams()

    def _generate_world_cup_teams(self):
        from schemas.player import PlayerCreate
        from schemas.team import TeamCreate

        existing_codes = {team.code.upper() for team in self.team_repo.get_all()}
        existing_names = {team.name for team in self.team_repo.get_all()}
        for name, code, group_name in WORLD_CUP_2026_TEAMS:
            if self.team_repo.count() >= TOURNAMENT_TEAM_COUNT:
                break
            if code in existing_codes or name in existing_names:
                continue

            team = self.team_repo.create(TeamCreate(name=name, code=code))
            self.team_repo.update(team, {"group_name": group_name})
            existing_codes.add(code)
            existing_names.add(name)
            for player_number in range(1, 3):
                fname = random.choice(FIRST_NAMES)
                lname = random.choice(POSITION_POOL[random.choice(POSITIONS)])
                self.player_repo.create(PlayerCreate(
                    name=f"{fname} {lname} {code}-{player_number}",
                    position=random.choice(POSITIONS),
                    team_id=team.id,
                ))

    def _tournament_teams(self):
        teams = self.team_repo.get_all()
        seeded_codes = {code for _, code, _ in WORLD_CUP_2026_TEAMS}
        seeded_order = {code: index for index, (_, code, _) in enumerate(WORLD_CUP_2026_TEAMS)}
        teams.sort(key=lambda team: (
            0 if team.code.upper() in seeded_codes else 1,
            seeded_order.get(team.code.upper(), 999),
            team.name,
        ))
        return teams[:TOURNAMENT_TEAM_COUNT]

    def _assign_groups(self):
        seeded_groups = {code: group for _, code, group in WORLD_CUP_2026_TEAMS}
        for index, team in enumerate(self._tournament_teams()):
            group_letter = seeded_groups.get(team.code.upper(), GROUP_NAMES[index // 4])
            self.team_repo.update(team, {"group_name": group_letter})

    def _ensure_players(self):
        from schemas.player import PlayerCreate

        for team in self._tournament_teams():
            count = self.player_repo.count_by_team(team.id)
            if count < 3:
                needed = 3 - count
                for offset in range(1, needed + 1):
                    fname = random.choice(FIRST_NAMES)
                    lname = random.choice(POSITION_POOL[random.choice(POSITIONS)])
                    player_number = count + offset
                    self.player_repo.create(PlayerCreate(
                        name=f"{fname} {lname} {team.code}-{player_number}",
                        position=random.choice(POSITIONS),
                        team_id=team.id,
                    ))

    def _play_match(self, a: str, b: str, allow_draw: bool = False) -> MatchResult:
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        winner = None
        if x > y:
            winner = a
        elif y > x:
            winner = b
        elif not allow_draw:
            winner = random.choice([a, b])
        return MatchResult(
            home_team=a,
            away_team=b,
            home_goals=x,
            away_goals=y,
            winner=winner,
        )

    def _simulate_group_stage(self) -> list[GroupStageResult]:
        results = []
        tournament_teams = self._tournament_teams()
        for group in GROUP_NAMES:
            teams_in_group = [t for t in tournament_teams if t.group_name == group]
            matches = []
            stats = {t.name: {"pts": 0, "gf": 0, "ga": 0} for t in teams_in_group}
            for i in range(len(teams_in_group)):
                for j in range(i + 1, len(teams_in_group)):
                    match = self._play_match(teams_in_group[i].name, teams_in_group[j].name, allow_draw=True)
                    matches.append(match)
                    stats[match.home_team]["gf"] += match.home_goals
                    stats[match.home_team]["ga"] += match.away_goals
                    stats[match.away_team]["gf"] += match.away_goals
                    stats[match.away_team]["ga"] += match.home_goals
                    if match.winner == match.home_team:
                        stats[match.home_team]["pts"] += 3
                    elif match.winner == match.away_team:
                        stats[match.away_team]["pts"] += 3
                    else:
                        stats[match.home_team]["pts"] += 1
                        stats[match.away_team]["pts"] += 1

            sorted_teams = sorted(
                stats.items(),
                key=lambda x: (x[1]["pts"], x[1]["gf"] - x[1]["ga"], x[1]["gf"]),
                reverse=True,
            )
            standings = [
                GroupStanding(
                    team=team_name,
                    pts=s["pts"],
                    gf=s["gf"],
                    ga=s["ga"],
                    gd=s["gf"] - s["ga"],
                    position=pos,
                )
                for pos, (team_name, s) in enumerate(sorted_teams, 1)
            ]
            results.append(GroupStageResult(group=group, standings=standings, matches=matches))
        return results

    def _get_qualified(self, group_results: list[GroupStageResult]) -> list[str]:
        top_two = []
        third_placed = []
        for group_result in group_results:
            standings = sorted(
                group_result.standings,
                key=lambda x: (x.pts, x.gd, x.gf),
                reverse=True,
            )
            top_two.extend(team.team for team in standings[:2])
            third_placed.append(standings[2])

        best_thirds = sorted(third_placed, key=lambda x: (x.pts, x.gd, x.gf), reverse=True)[:8]
        return top_two + [team.team for team in best_thirds]

    def _simulate_knockout(self, matches: list[tuple]) -> tuple[list[MatchResult], list[str]]:
        results = []
        winners = []
        for home, away in matches:
            match = self._play_match(home, away)
            results.append(match)
            winners.append(match.winner)
        return results, winners

    def _pair_round(self, teams: list[str]) -> list[tuple]:
        return [(teams[i], teams[-(i + 1)]) for i in range(len(teams) // 2)]

    def _cache_metrics(self, response: SimulatorResponse):
        teams = self._tournament_teams()
        team_players = {team.name: [p.name for p in team.players] for team in teams}

        player_goals = {}
        all_matches: list[MatchResultType] = []
        for group_result in response.groups:
            all_matches.extend(group_result.matches)
        all_matches.extend(response.round_of_32)
        all_matches.extend(response.round_of_16)
        all_matches.extend(response.quarterfinals)
        all_matches.extend(response.semifinals)
        if response.third_place:
            all_matches.append(response.third_place)
        all_matches.append(response.final)

        total_goals = 0
        for match in all_matches:
            for _ in range(match.home_goals):
                players = team_players.get(match.home_team, [])
                if players:
                    player = random.choice(players)
                    key = (match.home_team, player)
                    player_goals[key] = player_goals.get(key, 0) + 1
            for _ in range(match.away_goals):
                players = team_players.get(match.away_team, [])
                if players:
                    player = random.choice(players)
                    key = (match.away_team, player)
                    player_goals[key] = player_goals.get(key, 0) + 1
            total_goals += match.home_goals + match.away_goals

        total_matches = (
            sum(len(group.matches) for group in response.groups)
            + len(response.round_of_32)
            + len(response.round_of_16)
            + len(response.quarterfinals)
            + len(response.semifinals)
            + (1 if response.third_place else 0)
            + 1
        )

        top_scorer_name = ""
        top_scorer_team = ""
        top_scorer_goals = 0
        if player_goals:
            top_scorer_team, top_scorer_name = max(player_goals, key=player_goals.get)
            top_scorer_goals = player_goals[(top_scorer_team, top_scorer_name)]

        team_scorers = []
        for team_name, players in team_players.items():
            player_rows = [
                {
                    "player_name": player_name,
                    "goals": player_goals.get((team_name, player_name), 0),
                }
                for player_name in players
            ]
            player_rows.sort(key=lambda row: (row["goals"], row["player_name"]), reverse=True)
            team_scorers.append({
                "team_name": team_name,
                "total_goals": sum(row["goals"] for row in player_rows),
                "players": player_rows,
            })
        team_scorers.sort(key=lambda row: (row["total_goals"], row["team_name"]), reverse=True)

        cache_store(
            champion=response.champion,
            top_scorer_name=top_scorer_name,
            top_scorer_team=top_scorer_team,
            top_scorer_goals=top_scorer_goals,
            total_goals=total_goals,
            total_matches=total_matches,
            team_scorers=team_scorers,
        )

    def run(self) -> SimulatorResponse:
        self._ensure_data()
        self._assign_groups()
        self._ensure_players()

        group_results = self._simulate_group_stage()
        qualified = self._get_qualified(group_results)

        r32_matches = self._pair_round(qualified)
        r32_results, r32_winners = self._simulate_knockout(r32_matches)

        r16_matches = [(r32_winners[i], r32_winners[i + 1]) for i in range(0, 16, 2)]
        r16_results, r16_winners = self._simulate_knockout(r16_matches)

        qf_matches = [(r16_winners[i], r16_winners[i + 1]) for i in range(0, 8, 2)]
        qf_results, qf_winners = self._simulate_knockout(qf_matches)

        sf_matches = [(qf_winners[i], qf_winners[i + 1]) for i in range(0, 4, 2)]
        sf_results, sf_winners = self._simulate_knockout(sf_matches)

        sf1_loser = sf_results[0].away_team if sf_results[0].winner == sf_results[0].home_team else sf_results[0].home_team
        sf2_loser = sf_results[1].away_team if sf_results[1].winner == sf_results[1].home_team else sf_results[1].home_team
        third_place = self._play_match(sf1_loser, sf2_loser)

        final_match = self._play_match(sf_winners[0], sf_winners[1])

        response = SimulatorResponse(
            groups=group_results,
            round_of_32=r32_results,
            round_of_16=r16_results,
            quarterfinals=qf_results,
            semifinals=sf_results,
            third_place=third_place,
            final=final_match,
            champion=final_match.winner,
        )
        self._cache_metrics(response)
        return response
