from fetchBooks.handler.render import FetchBooks

if __name__ == "__main__":
    server = FetchBooks.makeServer()

    server.serve()
