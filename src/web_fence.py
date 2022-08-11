import config
import upact.platforms
import upact.fences as fences
import upact.store as store


if __name__ == "__main__":
    fences.web.start_service(upact.platforms.current_platform(config), store.init_db(config.DATABASE_FILE), debug=True)
