from recetarioweb.models.mymodel import Base, engine

def main():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    main()
