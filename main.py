from website import create_app

app = create_app()

if __name__ == '__main__':
    # Debug makes the Flask server auto reload after making changes
    app.run(debug=True)