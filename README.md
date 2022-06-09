# Trivia App
## Introducton
The Trivia API contains resources and endpoints for managing questions, categories, answers and playing the Trivia game.


## Getting Started
### Base URL
`http://127.0.0.1:5000`
### API keys/Authentications
Not applicable


## Errors
### 404 - Not Foumd

```
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

### 422 - Unprocessable entity
```
{
    "success": false,
    "error": 422,
    "message": "unprocessable"
}
```

## Resource Endpoint Library
### Categories
`GET /categories`
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None

```
{
    "success": true,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "total_categories" 6
}
```

### Questions
`GET /questions?page=3`
* Fetches a paginated list of ten questions per page.
* Request Arguments: `page (int)`

```
{
    "categories": { 
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
    ],
    "success": true,
    "total_questions": 31
}
```

`GET /categories/1/questions`
* Fetches questions by category.
* Request Arguments: None

```
{
    "current_category": 1,
    "success": true,
    "total_questions: 12,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
        "question": "Who discovered penicillin?"
        },
    ]
}
```


`POST /questions/search`
* Returns a list of questions based on a search term
* Request Body Parameters: `searchTerm (str)`, `category (int)`
* `curl -d "searchTerm=lake&category=null" -X POST http://127.0.0.1/5000/questions/search`
```
{
    "current_category": null,
    "success": true,
    "total_questions": 1,
    "questions": [
        {
            answer: "Lake Victoria"
            category: 3
            difficulty: 2
            id: 13
            question: "What is the largest lake in Africa?"
        }
    ]
}
```

`POST /questions`
* Adds a question to the question library
* Request Body Parameters: `question (str)`, `answer (str)`, `category (int)`, `difficulty (int)`
* `curl -d "question=what is my name&answer=timothy&category=1&difficulty=3" -X POST http://127.0.0.1/5000/questions`

```
{
    "success": true,
    "created": 43 [id of the newly created question],
    "question": "what is my name",
    "answer": "timothy",
    "category": 1,
    "difficulty": 3
}
```

`DELETE /questions/1`
* Deletes a particular question
* Request Argument: None
```
{
    'success': true,
    'deleted': 1
}
```

`POST /quizzes`
* Gets questions to play the quiz
* Request Body Parameters: `previous_questions (list)`, `quiz_category (dict)`

* `curl -d "previous_questions=[41]&quiz_category={type: Science, id: 1}" -X POST http://127.0.0.1/5000/quizzes`

```
{
    "question": {
        "answer": "The Liver"
        "category: 1
        "difficulty": 4
        "id": 20
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}

