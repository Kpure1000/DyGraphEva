# Data Process Need-to-Know

## Graph File Example

```javascript
{
    "nodes": [
            {
                "id": 0,
                "group": 0
            },
            {
                "id": 1,
                "group": 0
            },
            {
                "id": 2,
                "group": 1
            },
            {
                "id": 3,
                "group": 1
            }
        ],
    "links": [
        [
        {
            "source": 0,
            "target": 3,
            "weight": 2,
        },
        {
            "source": 1,
            "target": 0,
            "weight": 1,
        },
        {
            "source": 2,
            "target": 3,
            "weight": 1,
        }
    ]
}
```

## Config Example

**If I have data files as:**

> **newcomb_1.json**
> **newcomb_2.json**
> **newcomb_3.json**

Config file shoud be:

```javascript
{
    "day_start": 1,
    "day_end": 3,
    "prefix": "newcomb_",
    "distance_scale": 12 // 
}
```
