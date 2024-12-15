import os
import logging
from typing import Dict, List
import pyspiel
import requests
import time
from datetime import datetime
from cs410_arena.matchmaker.elo import EloMatchmaker

class GoArena:
    def __init__(self, bot_urls: Dict[str, str], board_size, setupTimeout: int = 5, totalMoveTimeout: int = 15, grace_time_per_move: float = 0.05):
        """
        Args:
            bot_urls: Dictionary mapping bot names to their API URLs
            board_size: Size of the Go board
            setupTimeout: Timeout in seconds for bot setup
            totalMoveTimeout: Total timeout in seconds for all moves
            grace_time_per_move: Additional grace time added to the total time after each move
        """
        self.bot_urls = bot_urls
        self.board_size = board_size
        self.setupTimeout = setupTimeout
        self.totalMoveTimeout = totalMoveTimeout
        self.grace_time_per_move = grace_time_per_move
        self.game = pyspiel.load_game("go", {"board_size": board_size})

        # Setup logging with timestamped filenames
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"logs/tournament_{timestamp}.log"
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        
    def setup_bot(self, bot_url: str, player: int) -> bool:
        try:
            response = requests.post(
                f"{bot_url}/setup",
                json={'player': player},
                timeout=self.setupTimeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logging.error(f"Error setting up bot at {bot_url}: {e}")
            return False

    def get_bot_move(self, bot_url: str, game_state: pyspiel.State, time_remaining: float) -> int:
        try:
            start_time = time.time()
            response = requests.post(
                f"{bot_url}/get_move",
                json={
                    'game_state': game_state.serialize(),
                    'time_remaining': time_remaining  # Pass time remaining
                },
                timeout=min(self.totalMoveTimeout, time_remaining)
            )
            elapsed_time = time.time() - start_time
            move_data = response.json()['move']
            return move_data, elapsed_time
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting move from bot at {bot_url}: {e}")
            return -1, 0
        except Exception as e:
            logging.error(f"Bot at {bot_url} encountered an error: {e}")
            return -1, 0

    def get_bot_update(self, bot_url: str, game_state: pyspiel.State) -> None:
        try:
            response = requests.post(
                f"{bot_url}/update",
                json={'game_state': game_state.serialize()},
                timeout=self.setupTimeout
            )
            if response.status_code != 200:
                logging.warning(f"Failed to update bot at {bot_url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error updating bot at {bot_url}: {e}")
        except Exception as e:
            logging.error(f"Bot at {bot_url} encountered an error during update: {e}")

    def run_match(self, black_bot_url: str, white_bot_url: str) -> dict:
        """Run a single match between two bots"""
        state = self.game.new_initial_state()
        remaining_time = {black_bot_url: self.totalMoveTimeout, white_bot_url: self.totalMoveTimeout}
        move_counts = 0

        if not (self.setup_bot(black_bot_url, 0) and self.setup_bot(white_bot_url, 1)):
            return {'error': 'Failed to setup bots'}

        current_bot_url = black_bot_url
        while not state.is_terminal():
            move, elapsed_time = self.get_bot_move(current_bot_url, state, remaining_time[current_bot_url])

            if move == -1 or elapsed_time > remaining_time[current_bot_url]:
                logging.error(f"Bot at {current_bot_url} ran out of time or failed to provide a move.")
                return {
                    'winner': 'white' if current_bot_url == black_bot_url else 'black',
                    'resigned': True,
                    'moves': state.move_number(), 
                    'move_counts': move_counts
                }
            
            move_counts += 1

            # Update remaining time and add grace time
            remaining_time[current_bot_url] -= elapsed_time
            remaining_time[current_bot_url] = min(
                remaining_time[current_bot_url] + self.grace_time_per_move, self.totalMoveTimeout
            )

            state.apply_action(move)
            self.get_bot_update(current_bot_url, state)
            current_bot_url = white_bot_url if current_bot_url == black_bot_url else black_bot_url

        result = state.returns()
        return {
            'winner': 'black' if result[0] > 0 else 'white',
            'score': str(result),
            'moves': state.move_number(),
            'move_counts': move_counts
        }

    def run_tournament(self) -> List[dict]:
        """Run a round-robin tournament between all bots"""
        results = []
        bot_names = list(self.bot_urls.keys())
        bot_stats = {bot: {'wins': 0, 'losses': 0, 'total_score': 0.0, 'matches': 0, 'total_moves': 0} for bot in bot_names}

        matchmaker = EloMatchmaker(order_matters=True)
        matchmaker.add_new_bots(bot_names)
        matchups = matchmaker.generate_matches(bot_names)

        for black_bot, white_bot in matchups:
            print(f"\nStarting match: {black_bot} (B) vs {white_bot} (W)")
            result = self.run_match(self.bot_urls[black_bot], self.bot_urls[white_bot])
            print(result)

            if 'error' in result:
                logging.error(f"Error in match: {result['error']}")
                continue

            result.update({'black': black_bot, 'white': white_bot})
            results.append(result)
            logging.info(f"Match {black_bot} (B) vs {white_bot} (W) Result: {result}")

            # Update bot stats
            bot_stats[black_bot]['matches'] += 1
            bot_stats[white_bot]['matches'] += 1

            winner = result['winner']            
            loser = black_bot if winner == 'white' else white_bot
            winner = black_bot if winner == 'black' else white_bot
            bot_stats[winner]['wins'] += 1
            bot_stats[loser]['losses'] += 1
            
            matchmaker.update_elo(winner = winner, loser = loser)

            if 'score' in result:
                black_score, white_score = map(float, result['score'][1:-1].split(","))
                bot_stats[black_bot]['total_score'] += black_score
                bot_stats[white_bot]['total_score'] += white_score

            bot_stats[black_bot]['total_moves'] += result['move_counts']
            bot_stats[white_bot]['total_moves'] += result['move_counts']

        # Log detailed bot statistics
        for bot, stats in bot_stats.items():
            avg_score = stats['total_score'] / stats['matches'] if stats['matches'] > 0 else 0.0
            avg_moves = stats['total_moves'] / stats['matches'] if stats['matches'] > 0 else 0.0
            elo = matchmaker.get_elo(bot)
            logging.info(f"Bot {bot}: Wins: {stats['wins']}, Losses: {stats['losses']}, Average Score: {avg_score}, Average Moves per Game: {avg_moves}, Elo: {elo}")

        return results
