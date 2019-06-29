from slack_resurrect.web import app

if __name__ == "__main__":
    from slack_resurrect.settings import CONFIG

    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(
        debug=True,
        port=int(CONFIG.PORT),
        host="0.0.0.0"
    )
