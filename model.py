from mapping import *
from DAO import *
from sqlalchemy import *
from datetime import datetime
from decimal import *
import requests
import time
from requests.exceptions import ConnectionError


class Database():
    def insert(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)
            session.commit()
            session.close()
            return 1
        except:
            return 0

    def selectMovie(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            movie = DAOMovies.select(session , id)
            session.commit()
            session.close()
            return movie
        except:
            return 0
    

    def selectCompany(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            company = DAOCompanies.select(session, id)
            session.commit()
            session.close()
            return company
        except:
            return 0


    def selectGenre(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            genre = DAOGenres.select(session, id)
            session.commit()
            session.close()
            return genre
        except:
            return 0
        

    def selectReview(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            review = DAOReviews.select(session, id)
            session.commit()
            session.close()
            return review
        except:
            return 0
        
    def selectCast(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            cast = DAOCast.select(session, id)
            session.commit()
            session.close()
            return cast
        except:
            return 0


    def selectCrew(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            crew = DAOCrew.select(session, id)
            session.commit()
            session.close()
            return crew
        except:
            return 0


    def selectPerson(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            person = DAOPeople.select(session, id)
            session.commit()
            session.close()
            return person
        except:
            return 0


# checar se uma string é vazia: s.strip() - remove os espaços vazios da string e verifica se ela é vazia
class API():
    def __init__(self):
        # Definição da api_key e headers
        self.api_key = "7ef680827a056a8e7e1bfcd5e5f92459"
        self.headers = {
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.36"
        }

    
    #função que recebe uma data no formato YYYY-MM-DD ou None e retorna um datetime ou None 
    def formatDate(self, date):
        if date is not None:
            year, month, day = map(int, date.split('-'))
            return datetime(year, month, day)
        else:
            return None

    #função que recebe um json e formata seus campos para inserir no banco de dados 
    def formatResponseValues(self, json):
        for value in json:
            if type(json[value]) is list or type(json[value]) is bool:
                continue
            if json[value] is not None:
                json[value] = str(json[value])
            if not(json[value] and json[value].strip()):
                json[value] = None
        return json


    #função que irá realizar a requisição para a api e irá tratar a exception ConnectionError que
    #estava acontecendo algumas vezes durante as requisições
    def requestHandler(self, url):
        i = 0
        found = False
        while i < 5 and not found:
            try:
                response = requests.get(url, headers = self.headers)
                found = True
            except ConnectionError:
                time.sleep(5)
                i += 1
    
        if not found:
            response = None

        return response

    # funcao que ira pegar todos os generos de filmes da api
    def getGenres(self):
        print("Requisitando os gêneros dos filmes...")
        
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + self.api_key + "&language=en-US"
            
        # pega o conteudo da resposta
        response = self.requestHandler(requestUrl)

        if response is not None:
            #separa os dados dos generos cadastrados
            genres = response.json().get("genres")

            # Itera sobre os generos verificando se já foram cadastrados e, caso não tenham sido, cadastra-os
            for genreJson in genres:
                self.formatResponseValues(genreJson)

                genreObj = Genre(id = int(genreJson.get("id")),
                            name = genreJson.get("name"))

                check = Database.selectGenre(genreObj.id)
                genreName = genreObj.name

                if not check:
                    Database.insert(genreObj)
                else:
                    print(f"Gênero {genreName} já cadastrado!")

        print('Gêneros dos filmes cadastrados!')

    # funcao que ira pegar os dados de uma companhia da api
    def getCompanies(self, companyId):

        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/company/" + str(companyId) + "?api_key=" + self.api_key
            
        # pega o conteudo da resposta
        response = self.requestHandler(requestUrl)

        if response is not None:
            # separa os dados dos generos cadastrados
            companyJson = response.json()
            
            self.formatResponseValues(companyJson)

            #chama a funcao para popular a tabela companies
            companyObj = Company(id = int(companyJson.get("id")),
                                name = companyJson.get("name"),
                                homepage = companyJson.get("homepage"),
                                origin_country = companyJson.get("origin_country"),
                                headquarters = companyJson.get("headquarters"))
                                        
            
            check = Database.selectCompany(companyObj.id)
            companyName = companyObj.name

            if not check:
                Database.insert(companyObj)
            else:
                print(f"Empresa {companyName} já cadastrada!")
    
    # funcao que ira pegar todos as reviews de um filme da api
    def getReviews(self, movieId):
        
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/movie/" + str(movieId) + "/reviews?api_key=" + self.api_key
            
        # pega o conteudo da resposta
        response = self.requestHandler(requestUrl)

        if response is not None:
            reviews = response.json().get("results")
                
            for reviewJson in reviews:
                
                if reviewJson.get("author_details").get("rating") is not None:
                    rating = int(reviewJson.get("author_details").get("rating"))
                else:
                    rating = None

                self.formatResponseValues(reviewJson)
            
                reviewObj = Review(id = reviewJson.get("id"),
                                author = reviewJson.get("author"),
                                content = reviewJson.get("content"),
                                rating = rating)

                check = Database.selectReview(reviewObj.id)
                reviewId = reviewObj.id

                if not check:
                    movieObj = Database.selectMovie(int(movieId))
                    reviewObj.movie = movieObj
                    Database.insert(reviewObj)
                else:
                    print(f"Review de id {reviewId} já cadastrada!")                
         

    def insertPerson(self, personJson): 
        personObj = Person(id = int(personJson.get("id")),
                            name = personJson.get("name"),
                            gender = int(personJson.get("gender")),
                            popularity = Decimal(personJson.get("popularity")))
                             
        check = Database.selectPerson(personObj.id)
        personName = personObj.name

        if not check:   
            Database.insert(personObj)
        else:
            print(f"Pessoa de nome {personName} já cadastrada!")                

     
    # funcao que ira pegar todo o elenco e a equipe técnica e também as pessoas de um filme da api e ira salvar no banco
    def getCastAndCrew(self, movieId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/movie/" + str(movieId) + "/credits?api_key=" + self.api_key
        
        # pega o conteudo da resposta
        response = self.requestHandler(requestUrl)
        
        if response is not None:
            cast = response.json().get("cast")
            crew = response.json().get("crew")
            
            for castJson in cast:

                self.formatResponseValues(castJson)
            
                self.insertPerson(castJson)
                
                castObj = Tcast(id = castJson.get("credit_id"),
                                character = castJson.get("character"),
                                department = castJson.get("known_for_department"))

                #Verifica se já foi inserido, se não foi, insere no banco
                check = Database.selectCast(castObj.id)
                castId = castObj.id
                
                if not check:   
                    movieObj = Database.selectMovie(int(movieId))
                    castObj.movie = movieObj
                    personObj = Database.selectPerson(int(castJson.get("id")))
                    castObj.person = personObj
                    Database.insert(castObj)
                else:
                    print(f"Elenco de id {castId} já cadastrado!")  
                
            for crewJson in crew:
                
                self.formatResponseValues(crewJson)

                self.insertPerson(crewJson)

                crewObj = Crew(id = crewJson.get("credit_id"),
                            job = crewJson.get("job"),
                            department = crewJson.get("department"))

                #Verifica se já foi inserido, se não foi, insere no banco
                check = Database.selectCrew(crewObj.id)      
                crewId = crewObj.id

                if not check:   
                    movieObj = Database.selectMovie(int(movieId))
                    crewObj.movie = movieObj
                    personObj = Database.selectPerson(int(crewJson.get("id")))
                    crewObj.person = personObj
                    Database.insert(crewObj)
                else:
                    print(f"Equipe técnica de id {crewId} já cadastrada!")  

    
    # funcao que ira consumir os ids de todos os filmes da api e chamar outras funções para consumir os outros dados
    # relacionados a um filme
    def getMovies(self):
        #numero de paginas da api que iremos utilizar
        maxPageNumber = 100

        for pageNumber in range(1, maxPageNumber + 1):
            # Monta a url da request que será feita
            requestUrl = "https://api.themoviedb.org/3/discover/movie?api_key=" + self.api_key + "&page=" + str(pageNumber)
            
            # pega o conteudo da resposta
            response = self.requestHandler(requestUrl)
            
            if response is not None:
                movies = response.json().get("results")
                
                for movie in movies:
                    #requisitando os dados da tabela filmes

                    # Monta a url da request que será feita
                    requestUrl = "https://api.themoviedb.org/3/movie/" + str(movie.get("id")) + "?api_key=" + self.api_key
                
                    # pega o conteudo da resposta
                    response = requests.get(requestUrl, headers = self.headers)

                    #separa os dados dos generos cadastrados
                    movieJson = response.json()

                    check = Database.selectMovie(int(movieJson.get("id")))
                    movieTitle = movie.get("title")

                    if check:
                        print(f"Filme {movieTitle} já cadastrado!")

                    else:
                        self.formatResponseValues(movieJson)

                        release_date = self.formatDate(movieJson.get("release_date"))

                        if int(movieJson.get("revenue")) == 0:
                            revenue = None
                        else:
                            revenue = int(movieJson.get("revenue"))

                        if int(movieJson.get("budget")) == 0:
                            budget = None
                        else:
                            budget = int(movieJson.get("budget"))

                        if int(movieJson.get("runtime")) == 0:
                            runtime = None
                        else:
                            runtime = int(movieJson.get("runtime"))

                        movieObject = Movie(id = int(movieJson.get("id")),
                                title = movieJson.get("title"),
                                status = movieJson.get("status"),
                                runtime = runtime,
                                revenue = revenue,
                                release_date = release_date,
                                popularity = Decimal(movieJson.get("popularity")),
                                overview = movieJson.get("overview"),
                                original_title = movieJson.get("original_title"),
                                original_language = movieJson.get("original_language"),
                                budget = budget,
                                adult = movieJson.get("adult"),
                                vote_count = int(movieJson.get("vote_count")),
                                vote_average = Decimal(movieJson.get("vote_average")))
                    
                        #iremos consultar no banco os genêros do filme para criar
                        #objetos do tipo genre e apendar na lista genres de cada objeto
                        #do tipo movie, e com isso iremos popular a tabela movies_genres
                        genres = movieJson.get("genres")

                        for genre in genres:
                            obj = Database.selectGenre(int(genre.get("id")))
                            movieObject.genres.append(obj)

                        print(f'\nRequisitando as empresas do filme {movieTitle}...')
                      
                        companies = movieJson.get("production_companies")
                            
                        for companie in companies:
                            self.getCompanies(companie.get("id"))
                            obj = Database.selectCompany(int(companie.get("id")))
                            movieObject.companies.append(obj)

                        print(f'Empresas do filme {movieTitle} cadastradas!')

                        Database.insert(movieObject)
                        print(f'\nFilme {movieTitle} cadastrado!')

                        print(f'\nRequisitando o elenco, a equipe técnica e as pessoas do filme {movieTitle}...')
                        self.getCastAndCrew(movie.get("id"))
                        print(f'Elenco, equipe técnica e as pessoas do filme {movieTitle} cadastrados!')

                        print(f'\nRequisitando as reviews do filme {movieTitle}...')
                        self.getReviews(movie.get("id"))
                        print(f'Reviews do filme {movieTitle} cadastradas!')