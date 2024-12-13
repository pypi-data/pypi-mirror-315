from flask import Flask, request, jsonify
import os
import pyspiel

def create_bot_server(bot_class, name):
    """Factory function to create a Flask server for any bot"""
    app = Flask(__name__)
    bot = bot_class(name)
    game = pyspiel.load_game("go", {"board_size": 19})

    @app.route('/get_move', methods=['POST'])
    def get_move():
        serialized_state = request.json['game_state']
        game_state = game.deserialize_state(serialized_state)
        move = bot.select_move(game_state)
        return jsonify({'move': move})
        
    @app.route('/setup', methods=['POST'])
    def setup():
        player_data = request.json
        bot.setup(player_data['player'])
        return jsonify({'status': 'ready'})

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200

    return app

def run_bot_server(bot_class, name="Bot"):
    """Convenience function to create and run a bot server"""
    app = create_bot_server(bot_class, name)
    port = int(os.environ.get('BOT_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
