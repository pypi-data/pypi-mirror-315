class query_router_prompts:
    def __init__(self):
        self.examples = [
                        {"question": "What's in the signature burger at Big Smoke, and how much does it cost?", "output": "True"},
                        {"question": "Can you suggest vegan options under 20 pounds in The Evergreen?", "output": "True"},
                        {"question": "What all restaurants are available in Terminal 5?", "output": "False"},
                        {"question": "What are the best gluten-free options under 15 pounds at Leon?", "output": "True"},
                        {"question": "What vegan options are available?", "output": "False"},
                        {"question": "How do I get to terminal 5 from Big Smoke restaurant?","output":"False"},
                        {"question": "What are the breakfast options at Pret-a-Manger?", "output": "True"},
                        {"question": "Does Jones the Grocer offer gluten-free options?", "output": "True"},
                        {"question": "How many calories are in the salad at Itsu?", "output": "True"},
                        {"question": "Are there vegan meals available at Costa?", "output": "True"},
                        {"question": "Can I get decaf at Black Sheep Coffee?", "output": "True"},
                        {"question": "Does The Crown Rivers Wetherspoon have vegetarian food?", "output": "True"},
                        {"question": "What’s on the menu at Heston’s The Perfectionists’ Café?", "output": "True"},
                        {"question": "Where is the nearest Starbucks?", "output": "False"},
                        {"question": "Do any of the restaurants in Terminal 5 offer vegan options?", "output": "False"},
                        {"question": "Can I get a vegetarian meal under 10 pounds in the terminal?", "output": "False"},
                        {"question": "How much is the soup at The Queen's Arms?", "output": "True"},
                        {"question": "What time does Gordon Ramsay Plane Food close?", "output": "True"},
                        {"question": "What’s the best place for coffee near Gate 10?", "output": "False"},
                        {"question": "Can I make a reservation at The Oceanic?", "output": "True"},
                        {"question": "How do I get from Caviar House and Prunier Seafood Bar to Terminal 3?", "output": "False"},
                        {"question": "What is the signature dish at The Globe?", "output": "True"},
                        {"question": "Where can I find sushi at the airport?", "output": "False"},
                        {"question": "What are the kid’s menu options at Giraffe?", "output": "True"},
                        {"question": "Can I find a gluten-free burger at any restaurant?", "output": "False"},
                        {"question": "Does Spuntino have a dessert menu?", "output": "True"},
                        {"question": "Are there healthy options at Wagamama?", "output": "True"},
                        {"question": "Which restaurant offers free Wi-Fi?", "output": "False"},
                        {"question": "Is The Commission serving breakfast?", "output": "True"},
                        {"question": "What are the vegan offerings at the nearest restaurant?", "output": "False"},
                        {"question": "Do any restaurants near security serve coffee?", "output": "False"},
                        {"question": "How much does a sandwich cost at Fortnum & Mason Bar?", "output": "True"},
                        {"question": "Which restaurants in the terminal serve coffee?", "output": "False"},
                        {"question": "What sushi rolls are on the menu at YO!?", "output": "True"},
                        {"question": "Are there vegetarian options at The Prince of Wales?", "output": "True"},
                        {"question": "Does any restaurant in Terminal 5 serve Indian food?", "output": "False"},
                        {"question": "What time does Pilots Bar and Kitchen open?", "output": "True"},
                        {"question": "Can I get take-away from any restaurant in the terminal?", "output": "False"},
                        {"question": "Does The Evergreen have low-carb options?", "output": "True"},
                        {"question": "What is the vegan option served in YO! in terminal 5?", "output": "True"}

                    ]
        
        # self.few_shot_prefix =  """
        #                         You are a question router designed to route user queries to two different models. One model is used for restaurant specific questions that can answer queries related to specific restuarants, and the other is used for answering rest type of questions.

        #                         Your job is to analyze the incoming questions and decide whether they are related to a particular restaurant or not:
        #                         --- Return `True` if the question is related to the following restaurant menu:
        #                             ['caffe-nero', 'shan-shui', 'jones-the-grocer', 'big-smoke', 'the-evergreen', 'joe-s-coffee-house', 'gordon-ramsay-plane-food', \
        #                             'black-sheep-coffee', 'londons-pride-by-fullers', 'the-crown-rivers-wetherspoon', 'leon', 'starbucks', 'yo', \
        #                             'co-pilots-bar-and-kitchen', 'caviar-house-and-prunier-seafood-bar', 'the-vinery', 'kids-eat-free', 'star-light', 'wagamama', \
        #                             'the-commission', 'costa', 'spuntino', 'itsu', 'fortnum-and-mason-bar', 'pre-order-food-and-drink', 'the-queens-arms', 'the-globe', \
        #                             'the-prince-of-wales', 'pret-a-manger', 'giraffe', 'hestons-the-perfectionists-cafe', 'the-oceanic', 'the-curator', 'pilots-bar-and-kitchen']
        #                         --- Return `False` otherwise (return False even if the query is about restaurants in general but not specifically about the restaurants listed above) """

        self.few_shot_prefix = """You are a question router designed to route user queries to two different models. One model is used for restaurant-specific questions that can answer queries related to specific restaurants, and the other is used for answering other types of questions.

                                Your job is to analyze the incoming questions and decide whether they are related to a particular restaurant **menu** (including queries about dishes, prices, ingredients, or availability of specific menu items):

                                --- Return `True` if the question is about the menu (or specific menu-related details like prices, available dishes, ingredients) of the following restaurants:
                                    ['caffe-nero', 'shan-shui', 'jones-the-grocer', 'big-smoke', 'the-evergreen', 'joe-s-coffee-house', 'gordon-ramsay-plane-food', 'black-sheep-coffee', 'londons-pride-by-fullers', \
                                        'the-crown-rivers-wetherspoon', 'leon', 'starbucks', 'yo', 'co-pilots-bar-and-kitchen', 'caviar-house-and-prunier-seafood-bar', 'the-vinery', 'kids-eat-free', 'star-light', 'wagamama', \
                                            'the-commission', 'costa', 'spuntino', 'itsu', 'fortnum-and-mason-bar', 'pre-order-food-and-drink', 'the-queens-arms', 'the-globe', 'the-prince-of-wales', 'pret-a-manger', 'giraffe', \
                                                'hestons-the-perfectionists-cafe', 'the-oceanic', 'the-curator', 'pilots-bar-and-kitchen']

                                --- Return `False` for any other type of question (even if the query mentions a restaurant, but is not specifically about its menu or menu-related details).
                                """

# prompt = """
# Given the following conversation history and a new question, please rephrase the question to be more specific and contextual based on the conversation history. The rephrased question should be a standalone question that captures the context of the conversation.

# Conversation History:
# {context}

# New Question: {question}

# Rephrased Question:

# ONLY GENERATE REPHRASED QUESTION, NOTHING ELSE.
# """


    
class Prompts: 
    def __init__(self):
        self.prompt = """
        Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question by using answers to the previous questions which can be understood without the chat history. Do NOT answer the question,just reformulate it based on the previous Question and Answers if needed and otherwise return it as is.

        chat History:
        {context}

        latest Question: {question}

        Rephrased Question:
        """

    
        # self.prompt = """Use the answer from Question1, and use that answer to reframe the Question 2
        # Question1: {question1}
        # Answer1: {answer1}
        # Question2: {question2}

        # Exanples: 
        # Question1: What is the destination airport for flight BA846?
        # Answer1: Warsaw Chopin Airport
        # Question2: Based on this, what other flights from Heathrow are headed to the same continent (Europe)?
        # Reframed Question2: What other flights from Heathrow are headed to Warsaw Chopin Airport?


        # Question1: What is the departure airport for flight BA410?
        # Answer1: Heathrow Airport (LHR)
        # Question2: What flights from that departure airport are heading to European destinations today?
        # Reframed Question2: Now that we know it's Heathrow, what flights from Heathrow are heading to European destinations today?


        # Question1: Flight LH923 departs for Frankfurt Airport (FRA). Which country is Frankfurt Airport located in?
        # Answer1: Germany
        # Question2: what other flights from the same country are departing today?
        # Reframed Question2: Now that we know Frankfurt is in Germany, what other flights from the same country (Germany) are departing today?


        # Question1: What is the scheduled departure time for flight BA762?
        # Answer1: 07:30
        # Question2: what is the estimated arrival time for flights departing within five minutes of flight's time?
        # Reframed Question2: Based on the departure time of 07:30, what is the estimated arrival time for flights departing within five minutes of this time?
        # """

        self.contextualize_q_system_prompt = """Given a chat history and the latest user question 
                                                which might reference context in the chat history, 
                                                formulate a standalone question which can be understood 
                                                without the chat history. Do NOT answer the question, 
                                                just reformulate it if needed and otherwise return it as is."""
                                            
        self.answer_prompt = """You are an AI assistant for the Heathrow Airport in United Kingdom
        Given the Question and Answer, frame an approriate answer to give back to the user
        if Answer is None or empty, reply that database don't contain the answer

        Question: {question}
        Answer: {answer}"""
        self.system_prompt = """You are an AI assistance for Heathrow Airport, you will be provided the schema of SQL tables for flight departures and flight arrivals.
        OBJECTIVE: 
            1. First decide whether the query is from flight_arrivals or flight_departures table. flight_arrivals table contains information for flights coming to Heathrow, 
               similarly, flight_departures contains information of flights departing from Heathrow airport. Be very clear that all the flight_arrivals have destination as 
               Heathrow and all flight_departures have origin Heathrow
            2. then accordingly generate an SQL query to fetch rows which can answer the provided question
        
        To better understand what kind of queries require flight_arrivals data and which require flight_departure data, please go through the following questions
        flight_arrivals = [
                "My friend is arriving from Dubai at 9:30, where should I wait for him?",
                "What is the gate for my flight arriving from Frankfurt?",
                "I’m landing from Tokyo at 11:40, where can I collect my baggage?",
                "Where will I land if I’m arriving from Madrid at 6:00?",
                "What terminal will I arrive at from my flight from Amsterdam?",
                "My partner is coming from Sydney, what is the status of their flight?",
                "I’m flying from Los Angeles, where will I collect my bags upon arrival?",
                "Which gate will I arrive at after flying from Bangkok?",
                "When will my flight from Toronto land?",
                "Where should I go to pick up my bags if I’m arriving from New York?",
                "What is the arrival time for my flight from London Heathrow?",
                "What is the status of the flight arriving from Paris at 8:50?",
                "Which terminal will I arrive at from my flight from Cape Town?",
                "What time does my flight from San Francisco land?",
                "I’m arriving from Berlin at 1:00 PM, where should I go to collect my luggage?",
                "What is the gate for my flight arriving from Athens?",
                "My flight from Dublin is landing soon, where can I collect my bags?",
                "When will my flight from Prague arrive at the gate?",
                "I’m coming from Chicago, where will I land?",
                "What is the status of the flight arriving from Milan at 10:15?"]

        flight_departures = [
                "I have to leave for London at 8:15, from where can I board my flight?",
                "I’m departing to Tokyo at 9:20, what is the status of my flight?",
                "I am scheduled to leave for Berlin at 5:50, where do I check in?",
                "Where is the gate for my flight to Paris departing at 12:30?",
                "I have a flight to Miami at 3:45, where will I collect my boarding pass?",
                "What time is the departure for my flight to Dubai at 6:00?",
                "I need to catch a flight to San Francisco at 11:10, which gate do I need to go to?",
                "I have to leave for Los Angeles at 10:45, from which terminal is my flight departing?",
                "What’s the gate number for my flight to Madrid at 2:30 PM?",
                "Where is my terminal for the flight to Sydney departing at 7:15?",
                "My flight to Rome leaves at 4:30, where do I check in?",
                "I am scheduled to depart for Athens at 8:00, where is the boarding gate?",
                "When is the final boarding call for my flight to Zurich at 9:00?",
                "Where do I board my flight to Barcelona leaving at 5:30 PM?",
                "I have a flight to Chicago at 6:15 AM, from where do I check in?",
                "What time does my flight to Istanbul leave from Terminal 2?",
                "I need to catch my flight to Hong Kong at 2:00 PM, where will I collect my luggage?",
                "Where do I check in for my flight to Singapore at 8:30?",
                "Which gate is my flight to Abu Dhabi departing from at 11:50?",
                "I have to fly to Moscow at 4:10, where will I board my flight?"]

        INSTRUCTIONS TO GENERATE SQL QUERY: 
            1: make all lowercase comparisions, for any string comparision use LOWER
            2: whenever there is any time mentioned in query, search in both flight_status and (scheduled_departure or scheduled_arrival) respectively
            3: Time stamps in scheduled_departure, scheduled_arrival, actual_departure, actual_arrival are in timestamp format i.e. 11-09-2024 06:25, so to make time comparisions, use EXTRACT() to extract respective time. 
            4: flight_status is of type varchar e.g "Estimated dep 06:20", so use CASE SQL query like:
                SUBSTRING(LOWER(flight_status) FROM '\\d{{{time_pattern}}}:\\d{{{time_pattern}}}') = '06:20', to check from flight status
            5: Whenever there is any abbreviation of country in query, make it in full form and search.
            6: Use only the the relations or tables mentioned in the database.
            7: While generating queries in SELECT use only the column names of the table, don't make queries apart from these column names.
            8: End each query with ;
            9: To handle string comparisons with apostrophes (single quotes) in them, be careful with the SQL syntax. Escape a single quote within a string by doubling it e.g: replace nice cote d'azur airport with nice cote d''azur airport
            10: In UNION, INTERSECT etc. operations use () for each SELECT query
            11: For each query give the full row, i.e use SELECT *

        Question: {question}

        DATABASE SCHEMAS:
        flight_arrivals =CREATE TABLE IF NOT EXISTS flight_arrivals (
            id SERIAL PRIMARY KEY,
            flight_id VARCHAR(255),
            flight_number VARCHAR(255),
            flight_alternate_number VARCHAR(255),
            call_sign VARCHAR(255),
            codeshare TEXT,
            flight_status VARCHAR(255),
            status_icon VARCHAR(255),
            status_type VARCHAR(255),
            diverted_status VARCHAR(255),
            aircraft_model VARCHAR(255),
            aircraft_registration VARCHAR(255),
            aircraft_country VARCHAR(255),
            aircraft_hex VARCHAR(255),
            aircraft_owner VARCHAR(255),
            airline_name VARCHAR(255),
            airline_iata_code VARCHAR(255),
            airline_icao_code VARCHAR(255),
            origin_country_name VARCHAR(255),
            origin_city VARCHAR(255),
            origin_airport VARCHAR(255),
            origin_airport_iata_code VARCHAR(255),
            origin_airport_icao_code VARCHAR(255),
            origin_terminal VARCHAR(255),
            origin_baggage VARCHAR(255),
            origin_gate VARCHAR(255),
            destination_airport VARCHAR(255),
            destination_airport_iata_code VARCHAR(255),
            destination_airport_icao_code VARCHAR(255),
            destination_terminal VARCHAR(255),
            destination_baggage VARCHAR(255),
            destination_gate VARCHAR(255),
            scheduled_departure TIMESTAMP,
            scheduled_arrival TIMESTAMP,
            actual_departure TIMESTAMP,
            actual_arrival TIMESTAMP
        );
        flight_departures = CREATE TABLE IF NOT EXISTS flight_departures (
            id SERIAL PRIMARY KEY,
            flight_id VARCHAR(255),
            flight_number VARCHAR(255),
            flight_alternate_number VARCHAR(255),
            call_sign VARCHAR(255),
            codeshare TEXT,
            flight_status VARCHAR(255),
            status_icon VARCHAR(255),
            status_type VARCHAR(255),
            diverted_status VARCHAR(255),
            aircraft_model VARCHAR(255),
            aircraft_registration VARCHAR(255),
            aircraft_country VARCHAR(255),
            aircraft_hex VARCHAR(255),
            aircraft_owner VARCHAR(255),
            airline_name VARCHAR(255),
            airline_iata_code VARCHAR(255),
            airline_icao_code VARCHAR(255),
            origin_country_name VARCHAR(255),
            origin_airport VARCHAR(255),
            origin_airport_iata_code VARCHAR(255),
            origin_airport_icao_code VARCHAR(255),
            origin_terminal VARCHAR(255),
            origin_baggage VARCHAR(255),
            origin_gate VARCHAR(255),
            destination_country_name VARCHAR(255),
            destination_city VARCHAR(255),
            destination_airport VARCHAR(255),
            destination_airport_iata_code VARCHAR(255),
            destination_airport_icao_code VARCHAR(255),
            destination_terminal VARCHAR(255),
            destination_baggage VARCHAR(255),
            destination_gate VARCHAR(255),
            scheduled_departure TIMESTAMP,
            scheduled_arrival TIMESTAMP,
            actual_departure TIMESTAMP,
            actual_arrival TIMESTAMP
        );
        
        ONLY GENERATE SQL QUERY, NOTHING ELSE.
        """
        self.triplet_prompt = """
                Task: Comprehensively extract ALL the triples (subject, relation, object) from below given paragraph. Ensure that the subject and objects in the triples are named entities (name of person, organization, dates etc) and not multiple in number. You will be HEAVILY PENALIZED if you violate this constraint. 

            Examples: Use the following examples to understand the task better. \n \
            
            paragraph: William Rast is an American clothing line founded by Justin Timberlake and Trace Ayala. 
            It is most known for their premium jeans.  On October 17, 2006, Justin Timberlake and Trace Ayala put on their 
            first fashion show to launch their new William Rast clothing line.  The label also produces other clothing items
            such as jackets and tops.  The company started first as a denim line, later evolving into a men's and women's clothing line.

            triples: 
            (i) subject: William Rast, relation: clothing line, object: American
            (ii) subject: William Rast, relation: founded by, object: Justin Timberlake
            (iii) subject: William Rast, relation: founded by, object: Trace Ayala
            (iv) subject: William Rast, relation: known for, object: premium jeans
            (v) subject: William Rast, relation: launched on , object: October 17, 2006
            (vi) subject: Justin Timberlake, relation: first fashion show, object: October 17, 2006
            (vii) subject: Trace Ayala, relation: first fashion show, object: October 17, 2006
            (viii) subject: William Rast, relation: produces, object: jackets
            (ix) subject: William Rast, relation: produces, object: tops
            (x) subject: William Rast, relation: started as, object: denim line
            (xi) subject: William Rast, relation: evolved into, object: men's and women's clothing line


            paragraph: The Glennwanis Hotel is a historic hotel in Glennville, Georgia, Tattnall County, Georgia,
            built on the site of the Hughes Hotel.  The hotel is located at 209-215 East Barnard Street.  The old Hughes Hotel was 
            built out of Georgia pine circa 1905 and burned in 1920.  The Glennwanis was built in brick in 1926.  The local Kiwanis 
            club led the effort to get the replacement hotel built, and organized a Glennville Hotel Company with directors being 
            local business leaders.  The wife of a local doctor won a naming contest with the name "Glennwanis Hotel", a suggestion
            combining "Glennville" and "Kiwanis"

            triples:
            (i) subject: Glennwanis Hotel, relation: is located in, object: 209-215 East Barnard Street, Glennville, Tattnall County, Georgia
            (ii) subject: Glennwanis Hotel, relation: was built on the site of, object: Hughes Hotel
            (iii) subject: Hughes Hotel, relation: was built out of, object: Georgia pine
            (iv) subject: Hughes Hotel, relation: was built circa, object: 1905
            (v) subject: Hughes Hotel, relation: burned in, object: 1920
            (vi) subject: Glennwanis Hotel, relation: was re-built in, object: 1926
            (vii) subject: Glennwanis Hotel, relation: was re-built using, object: brick
            (viii) subject: Kiwanis club, relation: led the effort to re-build, object: Glennwanis Hotel
            (viii) subject: Kiwanis club, relation: organized, object: Glennville Hotel Company
            (ix) subject: Glennville Hotel Company, relation: directors, object: local business leaders
            (x) subject: Glennwanis Hotel, relation: combines, object: "Glennville" and "Kiwanis"


            paragraph: Dr. Lisa K. Randall (June 18, 1962 - present) is an American theoretical physicist and\
            a leading expert in particle physics and cosmology at Harvard University, located in Cambridge, \
            Massachusetts. Her notable work includes research on dark matter and extra dimensions. Cambridge \
            is part of Middlesex County, where she has made significant contributions to the scientific community.

            Triples:
            (i) subject: Dr. Lisa K. Randall, relation: was born on, object: June 18, 1962
            (ii) subject: Dr. Lisa K. Randall, relation: expert in, object: particle physics and cosmology
            (iii) subject: Dr. Lisa K. Randall, relation: works at, object: Harvard University
            (iv) subject: Harvard University, relation: located in, object: Cambridge, Massachusetts
            (v) subject: Cambridge, Massachusetts, relation: part of, object: Middlesex County
            (vi) subject: Dr. Lisa K. Randall, relation: conducted research on, object: dark matter and extra dimensions
            (vii) subject: Dr. Lisa K. Randall, relation: contributed to, object: scientific community in Middlesex County
            
            paragraph: John C. Petersen (November 2, 1842 - July 10, 1887) was an American butcher and farmer from \
            Appleton, Wisconsin who served as a member of the Wisconsin State Assembly from Outagamie County.


            Triples:
            (i) subject: John C. Petersen, relation: born on, object: November 2, 1842
            (ii) subject: John C. Petersen, relation: died on, object: July 10, 1887
            (iii) subject: John C. Petersen, relation: occupation, object: American butcher and farmer
            (iv) subject: John C. Petersen, relation: belongs to, object: Appleton, Wisconsin
            (v) subject: John C. Petersen, relation: member of, object: Wisconsin State Assembly
            (vi) subject: John C. Petersen, relation: represents, object: Outagamie County
            (vi) subject: Appleton, Wisconsin, relation: located in, object: Outagamie County


            Final:
            paragraph:
            
            Triples:
        """
        self.system_prompt_arrival = """You are an AI assistance for Heathrow Airport, given the following SQL tables, your job is to complete the possible SQL query given a user’s Question.
        Instructions to generate SQL query: 
        1: make all lowercase comparisions
        2: whenever there is any time mentioned in query, search in both flight_status and (scheduled_departure or scheduled_arrival) respectively
        3: Time stamps in scheduled_departure, scheduled_arrival, actual_departure, actual_arrival are in timestamp format i.e. 11-09-2024 06:25, so to make time comparisions, use EXTRACT() to extract respective time. 
        4: flight_status is of type varchar e.g "Estimated dep 06:20", so use CASE SQL query like:
            SUBSTRING(LOWER(flight_status) FROM '\\d{{{time_pattern}}}:\\d{{{time_pattern}}}') = '06:20', to check from flight status
        5: Whenever there is any abbreviation of country in query, make it in full form and search.
        6: Use only the the relations or tables mentioned in the database.
        7: While generating queries in SELECT use only the column names of the table, don't make queries apart from these column names.
        8: End each query with ;
        9: To handle string comparisons with apostrophes (single quotes) in them, be careful with the SQL syntax. Escape a single quote within a string by doubling it e.g: replace nice cote d'azur airport with nice cote d''azur airport
        10: In UNION, INTERSECT etc. operations use () for each SELECT query
        11: For each query give the full row, i.e use SELECT *
        Question: {question}
        Database:
        flight_arrivals =CREATE TABLE IF NOT EXISTS flight_arrivals (
            id SERIAL PRIMARY KEY,
            flight_id VARCHAR(255),
            flight_number VARCHAR(255),
            flight_alternate_number VARCHAR(255),
            call_sign VARCHAR(255),
            codeshare TEXT,
            flight_status VARCHAR(255),
            status_icon VARCHAR(255),
            status_type VARCHAR(255),
            diverted_status VARCHAR(255),
            aircraft_model VARCHAR(255),
            aircraft_registration VARCHAR(255),
            aircraft_country VARCHAR(255),
            aircraft_hex VARCHAR(255),
            aircraft_owner VARCHAR(255),
            airline_name VARCHAR(255),
            airline_iata_code VARCHAR(255),
            airline_icao_code VARCHAR(255),
            origin_country_name VARCHAR(255),
            origin_city VARCHAR(255),
            origin_airport VARCHAR(255),
            origin_airport_iata_code VARCHAR(255),
            origin_airport_icao_code VARCHAR(255),
            origin_terminal VARCHAR(255),
            origin_baggage VARCHAR(255),
            origin_gate VARCHAR(255),
            destination_airport VARCHAR(255),
            destination_airport_iata_code VARCHAR(255),
            destination_airport_icao_code VARCHAR(255),
            destination_terminal VARCHAR(255),
            destination_baggage VARCHAR(255),
            destination_gate VARCHAR(255),
            scheduled_departure TIMESTAMP,
            scheduled_arrival TIMESTAMP,
            actual_departure TIMESTAMP,
            actual_arrival TIMESTAMP
        );
        ONLY GENERATE SQL QUERY, NOTHING ELSE.
        """
        self.system_prompt_departure = """You are an AI assistance for Heathrow Airport, given the following SQL tables, your job is to complete the possible SQL query given a user’s Question.
        Instructions to generate SQL query: 
        1: make all lowercase comparisions
        2: whenever there is any time mentioned in query, search in both flight_status and (scheduled_departure or scheduled_arrival) respectively
        3: Time stamps in scheduled_departure, scheduled_arrival, actual_departure, actual_arrival are in timestamp format i.e. 11-09-2024 06:25, so to make time comparisions, use EXTRACT() to extract respective time. 
        4: flight_status is of type varchar e.g "Estimated dep 06:20", so use CASE SQL query like:
            SUBSTRING(LOWER(flight_status) FROM '\\d{{{time_pattern}}}:\\d{{{time_pattern}}}') = '06:20', to check from flight status
        5: Whenever there is any abbreviation of country in query, make it in full form and search.
        6: Use only the the relations or tables mentioned in the database.
        7: While generating queries in SELECT use only the column names of the table, don't make queries apart from these column names.
        8: End each query with ;
        9: To handle string comparisons with apostrophes (single quotes) in them, be careful with the SQL syntax. Escape a single quote within a string by doubling it e.g: replace nice cote d'azur airport with nice cote d''azur airport
        10: In UNION, INTERSECT etc. operations use () for each SELECT query
        11: For each query give the full row, i.e use SELECT *
        Question: {question}
        Database: flight_departures = CREATE TABLE IF NOT EXISTS flight_departures (
            id SERIAL PRIMARY KEY,
            flight_id VARCHAR(255),
            flight_number VARCHAR(255),
            flight_alternate_number VARCHAR(255),
            call_sign VARCHAR(255),
            codeshare TEXT,
            flight_status VARCHAR(255),
            status_icon VARCHAR(255),
            status_type VARCHAR(255),
            diverted_status VARCHAR(255),
            aircraft_model VARCHAR(255),
            aircraft_registration VARCHAR(255),
            aircraft_country VARCHAR(255),
            aircraft_hex VARCHAR(255),
            aircraft_owner VARCHAR(255),
            airline_name VARCHAR(255),
            airline_iata_code VARCHAR(255),
            airline_icao_code VARCHAR(255),
            origin_country_name VARCHAR(255),
            origin_airport VARCHAR(255),
            origin_airport_iata_code VARCHAR(255),
            origin_airport_icao_code VARCHAR(255),
            origin_terminal VARCHAR(255),
            origin_baggage VARCHAR(255),
            origin_gate VARCHAR(255),
            destination_country_name VARCHAR(255),
            destination_city VARCHAR(255),
            destination_airport VARCHAR(255),
            destination_airport_iata_code VARCHAR(255),
            destination_airport_icao_code VARCHAR(255),
            destination_terminal VARCHAR(255),
            destination_baggage VARCHAR(255),
            destination_gate VARCHAR(255),
            scheduled_departure TIMESTAMP,
            scheduled_arrival TIMESTAMP,
            actual_departure TIMESTAMP,
            actual_arrival TIMESTAMP
        );
        
        ONLY GENERATE SQL QUERY, NOTHING ELSE.
        """
    
    def format_chat_history(self,chat_history):
        formatted_history = ""
        for i, (question, answer) in enumerate(chat_history, 1):
            formatted_history += f"Question/Answer {i}:\n"
            formatted_history += f"Question: {question}\n"
            formatted_history += f"Answer: {answer}\n\n"
        return formatted_history.strip()
    

















    # self.system_prompt = """You are an AI assistance for Heathrow Airport, given the following SQL tables, your job is to complete the possible SQL query given a user’s Question.
    #     Instructions to generate SQL query: 
    #     Before Making the query, first choose whether the query is from flight_arrivals or flight_departures, then accordingly generate the SQL query
    #     Be very clear that all the flight_arrivals have destination as Heathrow and all flight_departures have origin Heathrow
    #     flight_arrivals = [
    #             "My friend is arriving from Dubai at 9:30, where should I wait for him?",
    #             "What is the gate for my flight arriving from Frankfurt?",
    #             "I’m landing from Tokyo at 11:40, where can I collect my baggage?",
    #             "Where will I land if I’m arriving from Madrid at 6:00?",
    #             "What terminal will I arrive at from my flight from Amsterdam?",
    #             "My partner is coming from Sydney, what is the status of their flight?",
    #             "I’m flying from Los Angeles, where will I collect my bags upon arrival?",
    #             "Which gate will I arrive at after flying from Bangkok?",
    #             "When will my flight from Toronto land?",
    #             "Where should I go to pick up my bags if I’m arriving from New York?",
    #             "What is the arrival time for my flight from London Heathrow?",
    #             "What is the status of the flight arriving from Paris at 8:50?",
    #             "Which terminal will I arrive at from my flight from Cape Town?",
    #             "What time does my flight from San Francisco land?",
    #             "I’m arriving from Berlin at 1:00 PM, where should I go to collect my luggage?",
    #             "What is the gate for my flight arriving from Athens?",
    #             "My flight from Dublin is landing soon, where can I collect my bags?",
    #             "When will my flight from Prague arrive at the gate?",
    #             "I’m coming from Chicago, where will I land?",
    #             "What is the status of the flight arriving from Milan at 10:15?"]
    #     flight_departures = [
    #             "I have to leave for London at 8:15, from where can I board my flight?",
    #             "I’m departing to Tokyo at 9:20, what is the status of my flight?",
    #             "I am scheduled to leave for Berlin at 5:50, where do I check in?",
    #             "Where is the gate for my flight to Paris departing at 12:30?",
    #             "I have a flight to Miami at 3:45, where will I collect my boarding pass?",
    #             "What time is the departure for my flight to Dubai at 6:00?",
    #             "I need to catch a flight to San Francisco at 11:10, which gate do I need to go to?",
    #             "I have to leave for Los Angeles at 10:45, from which terminal is my flight departing?",
    #             "What’s the gate number for my flight to Madrid at 2:30 PM?",
    #             "Where is my terminal for the flight to Sydney departing at 7:15?",
    #             "My flight to Rome leaves at 4:30, where do I check in?",
    #             "I am scheduled to depart for Athens at 8:00, where is the boarding gate?",
    #             "When is the final boarding call for my flight to Zurich at 9:00?",
    #             "Where do I board my flight to Barcelona leaving at 5:30 PM?",
    #             "I have a flight to Chicago at 6:15 AM, from where do I check in?",
    #             "What time does my flight to Istanbul leave from Terminal 2?",
    #             "I need to catch my flight to Hong Kong at 2:00 PM, where will I collect my luggage?",
    #             "Where do I check in for my flight to Singapore at 8:30?",
    #             "Which gate is my flight to Abu Dhabi departing from at 11:50?",
    #             "I have to fly to Moscow at 4:10, where will I board my flight?"]
    #     1: make all lowercase comparisions
    #     2: whenever there is any time mentioned in query, search in both flight_status and (scheduled_departure or scheduled_arrival) respectively
    #     3: Time stamps in scheduled_departure, scheduled_arrival, actual_departure, actual_arrival are in timestamp format i.e. 11-09-2024 06:25, so to make time comparisions, use EXTRACT() to extract respective time. 
    #     4: flight_status is of type varchar e.g "Estimated dep 06:20", so use CASE SQL query like:
    #         SUBSTRING(LOWER(flight_status) FROM '\\d{{{time_pattern}}}:\\d{{{time_pattern}}}') = '06:20', to check from flight status
    #     5: Whenever there is any abbreviation of country in query, make it in full form and search.
    #     6: Use only the the relations or tables mentioned in the database.
    #     7: While generating queries in SELECT use only the column names of the table, don't make queries apart from these column names.
    #     8: End each query with ;
    #     9: To handle string comparisons with apostrophes (single quotes) in them, be careful with the SQL syntax. Escape a single quote within a string by doubling it e.g: replace nice cote d'azur airport with nice cote d''azur airport
    #     10: In UNION, INTERSECT etc. operations use () for each SELECT query
    #     11: For each query give the full row, i.e use SELECT *
    #     Question: {question}
    #     Database:
    #     flight_arrivals =CREATE TABLE IF NOT EXISTS flight_arrivals (
    #         id SERIAL PRIMARY KEY,
    #         flight_id VARCHAR(255),
    #         flight_number VARCHAR(255),
    #         flight_alternate_number VARCHAR(255),
    #         call_sign VARCHAR(255),
    #         codeshare TEXT,
    #         flight_status VARCHAR(255),
    #         status_icon VARCHAR(255),
    #         status_type VARCHAR(255),
    #         diverted_status VARCHAR(255),
    #         aircraft_model VARCHAR(255),
    #         aircraft_registration VARCHAR(255),
    #         aircraft_country VARCHAR(255),
    #         aircraft_hex VARCHAR(255),
    #         aircraft_owner VARCHAR(255),
    #         airline_name VARCHAR(255),
    #         airline_iata_code VARCHAR(255),
    #         airline_icao_code VARCHAR(255),
    #         origin_country_name VARCHAR(255),
    #         origin_city VARCHAR(255),
    #         origin_airport VARCHAR(255),
    #         origin_airport_iata_code VARCHAR(255),
    #         origin_airport_icao_code VARCHAR(255),
    #         origin_terminal VARCHAR(255),
    #         origin_baggage VARCHAR(255),
    #         origin_gate VARCHAR(255),
    #         destination_airport VARCHAR(255),
    #         destination_airport_iata_code VARCHAR(255),
    #         destination_airport_icao_code VARCHAR(255),
    #         destination_terminal VARCHAR(255),
    #         destination_baggage VARCHAR(255),
    #         destination_gate VARCHAR(255),
    #         scheduled_departure TIMESTAMP,
    #         scheduled_arrival TIMESTAMP,
    #         actual_departure TIMESTAMP,
    #         actual_arrival TIMESTAMP
    #     );
    #     flight_departures = CREATE TABLE IF NOT EXISTS flight_departures (
    #         id SERIAL PRIMARY KEY,
    #         flight_id VARCHAR(255),
    #         flight_number VARCHAR(255),
    #         flight_alternate_number VARCHAR(255),
    #         call_sign VARCHAR(255),
    #         codeshare TEXT,
    #         flight_status VARCHAR(255),
    #         status_icon VARCHAR(255),
    #         status_type VARCHAR(255),
    #         diverted_status VARCHAR(255),
    #         aircraft_model VARCHAR(255),
    #         aircraft_registration VARCHAR(255),
    #         aircraft_country VARCHAR(255),
    #         aircraft_hex VARCHAR(255),
    #         aircraft_owner VARCHAR(255),
    #         airline_name VARCHAR(255),
    #         airline_iata_code VARCHAR(255),
    #         airline_icao_code VARCHAR(255),
    #         origin_country_name VARCHAR(255),
    #         origin_airport VARCHAR(255),
    #         origin_airport_iata_code VARCHAR(255),
    #         origin_airport_icao_code VARCHAR(255),
    #         origin_terminal VARCHAR(255),
    #         origin_baggage VARCHAR(255),
    #         origin_gate VARCHAR(255),
    #         destination_country_name VARCHAR(255),
    #         destination_city VARCHAR(255),
    #         destination_airport VARCHAR(255),
    #         destination_airport_iata_code VARCHAR(255),
    #         destination_airport_icao_code VARCHAR(255),
    #         destination_terminal VARCHAR(255),
    #         destination_baggage VARCHAR(255),
    #         destination_gate VARCHAR(255),
    #         scheduled_departure TIMESTAMP,
    #         scheduled_arrival TIMESTAMP,
    #         actual_departure TIMESTAMP,
    #         actual_arrival TIMESTAMP
    #     );
    #     ONLY GENERATE SQL QUERY, NOTHING ELSE.
    #     """
