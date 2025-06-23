from app import crear_aplicacion


def main():
    app = crear_aplicacion()
    app.run(debug=True)


if __name__ == "__main__":
    main()
