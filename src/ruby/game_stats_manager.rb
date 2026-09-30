class GameStatsManager
    def initialize(db_connection)
        @db = db_connection
    end

    def fetch_user_stats
        query = "SELECT total_pages_collected, max_level_reached FROM player_progress WHERE id = 1;"
        result = @db.execute(query).first
        result ? { pages: result[0], level: result[1] } : { pages: 0, level: 0 }
    end

    def save_progress(new_pages, current_level)
        current_stats = fetch_user_stats
        updated_pages = current_stats[:pages] + new_pages
        updated_level = [current_stats[:level], current_level].max

        update_query = "UPDATE player_progress SET total_pages_collected = ?, max_level_reached = ?, last_updated = CURRENT_TIMESTAMP WHERE id = 1;"
        @db.execute(update_query, [updated_pages, updated_level])
    end
end