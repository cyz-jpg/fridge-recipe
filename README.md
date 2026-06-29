# Fridge Recipe

Fridge Recipe is a mobile app that helps users decide what to cook based on the ingredients they already have.

Users can take a picture of their fridge, and the app uses AI to detect the available ingredients. The user can then confirm or edit the detected ingredients before the app recommends recipes that can be made with them.

---

# Tech Stack

| Category | Technology |
|---|---|
| Frontend / Mobile app | Flutter + Dart |
| Backend | Python + FastAPI |
| AI / Computer Vision | OpenAI Vision API |
| Recipe Matching | Local recipe database / Recipe API |
| Database | SQLite |
| Version Control | Git + GitHub |

---

# Backend REST API

The backend uses the root route `/` for the main functionality.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Check if the backend is running |
| `POST` | `/` | Upload a fridge image and get recommended recipes |
| `GET` | `/:recipeId` | returns the recipe from the backend |


### Example Response (GET /)

```json
{
  "message": "Fridge Recipe API is running"
}
```
### Example Response (POST /)
```json
{
  "detected_ingredients": [
    "eggs",
    "cheese",
    "tomato"
  ],
  "recipes": [
    {
      "id": 1,
      "name": "Cheese Omelette",
      "match_score": 0.95,
      "time_minutes": 15,
      "difficulty": "easy",
      "filters" : ["vegetarian"],
      "source" : "https://recipe1.com"
    },
    {
      "id": 2,
      "name": "Tomato Pasta",
      "match_score": 0.67,
      "time_minutes": 25,
      "difficulty": "easy",
      "filters" : [],
      "source" : "https://recipe2.com"
    }
  ]
}
```

---

# Design
## Main colors
| Gebruik         | Kleur         | Hex       |
| --------------- | ------------- | --------- |
| Primary color   | Fresh Green   | `#4CAF50` |
| Secondary color | Soft Orange   | `#FF9800` |
| Background      | Warm Cream    | `#FFF8E7` |
| Cards           | White         | `#FFFFFF` |
| Text            | Dark Charcoal | `#263238` |
| Light text      | Gray          | `#757575` |
| Error / warning | Red           | `#E53935` |

## Figma
https://www.figma.com/design/owuayff6ExAOQdGgezcnyk/Untitled?node-id=0-1&p=f&t=1aN2JI21907l4V8u-0
